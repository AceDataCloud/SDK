"""Task polling for long-running operations.

A generation call always returns a handle, never sometimes a handle and
sometimes a dict — the caller decides whether to wait. When the server happens
to answer synchronously (some endpoints do for fast or cached results), the
handle is born already complete and ``wait()`` returns immediately rather than
polling for something that has already arrived.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

_DONE = {"succeed", "succeeded", "success", "completed", "complete", "finished"}
_FAILED = {"failed", "failure", "error", "cancelled", "canceled", "rejected"}


def _status_words(node: Any, depth: int = 0) -> list[str]:
    out: list[str] = []
    if depth > 6:
        return out
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("state", "status") and isinstance(value, str):
                out.append(value.lower())
            else:
                out.extend(_status_words(value, depth + 1))
    elif isinstance(node, list):
        for item in node:
            out.extend(_status_words(item, depth + 1))
    return out


def _collect_urls(node: Any, out: list[str], depth: int = 0) -> None:
    if depth > 6:
        return
    if isinstance(node, dict):
        for key, value in node.items():
            if (
                isinstance(value, str)
                and value.startswith("http")
                and (key.endswith("_url") or key == "url" or key.endswith("_urls"))
            ):
                out.append(value)
            else:
                _collect_urls(value, out, depth + 1)
    elif isinstance(node, list):
        for item in node:
            _collect_urls(item, out, depth + 1)


def artifact_urls(state: dict[str, Any]) -> list[str]:
    """Every artifact URL in a task response, outermost first.

    Where the artifact lives is not derivable from the OpenAPI spec — ``response``
    is typed as a bare object and the key differs per service (``video_url``,
    ``image_url``, ``data[].image_url``, ``data.video_url``). Rather than keep a
    per-service table that goes stale, collect anything URL-shaped.
    """
    if not isinstance(state, dict):
        return []
    found: list[str] = []
    _collect_urls(state.get("response", state), found)
    seen: set[str] = set()
    ordered: list[str] = []
    for url in found:
        if url not in seen:
            seen.add(url)
            ordered.append(url)
    return ordered


def task_status(state: dict[str, Any]) -> str:
    """Reduce a poll response to ``succeeded`` | ``failed`` | ``""`` (running).

    Services report completion inconsistently — a ``status`` word, a ``state``
    word spelled differently, only a ``finished_at`` timestamp, or merely the
    artifact URL appearing. This normaliser is deliberately broad; narrowing it
    silently hangs whichever service it drops.
    """
    response = state.get("response")
    if response is None:
        response = state
    if not isinstance(response, dict):
        return ""

    # A status word is the strongest signal and outranks the `success` flag:
    # a response can carry `success: false` for a retryable hiccup while the task
    # itself is still running, and `status: processing` alongside a finished_at.
    words = _status_words(response)
    if any(w in _FAILED for w in words):
        return "failed"
    if any(w in _DONE for w in words):
        # A terminal word with no artifact means the job ended without output.
        return "succeeded" if artifact_urls(state) else "failed"
    if words:
        # A non-terminal word (queued, processing, …) means keep waiting.
        return ""

    # No status word at all. `success: false` alone is ambiguous: some services
    # set it for a transient hiccup mid-run, alongside a bare string like
    # "temporary", and keep going. A *structured* error — a dict carrying a code
    # — is different: that is the upstream's final answer. hailuo reports an
    # unavailable model exactly so, with no finished_at, and reading it as
    # "still running" makes the caller poll until timeout instead of telling the
    # user "no channel available for this model".
    if response.get("success") is False:
        error = response.get("error")
        if artifact_urls(state) or (isinstance(error, dict) and error.get("code")):
            return "failed"

    finished = response.get("finished_at") is not None or state.get("finished_at") is not None
    if finished:
        if response.get("success") is True:
            return "succeeded"
        if response.get("success") is False:
            # Finished and explicitly unsuccessful — terminal, not retryable.
            return "failed"
        if artifact_urls(state):
            return "succeeded"

    if artifact_urls(state):
        return "succeeded"
    return ""


def progress(state: dict[str, Any]) -> int | None:
    """Percent complete when the service reports it, else ``None``.

    ``None`` rather than 0 so a caller renders "working" instead of a bar stuck
    at zero, which reads as broken.
    """
    if not isinstance(state, dict):
        return None
    for value in _find(state.get("response", state), ("progress", "percent", "percentage")):
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            pct = int(value * 100) if 0 < value <= 1 else int(value)
            return max(0, min(100, pct))
        if isinstance(value, str):
            try:
                pct = int(float(value.strip().rstrip("%")))
            except ValueError:
                continue
            return max(0, min(100, pct))
    return None


def _find(node: Any, names: tuple[str, ...], depth: int = 0):
    if depth > 6:
        return
    if isinstance(node, dict):
        for key, value in node.items():
            if key in names:
                yield value
            else:
                yield from _find(value, names, depth + 1)
    elif isinstance(node, list):
        for item in node:
            yield from _find(item, names, depth + 1)


def failure_reason(state: dict[str, Any]) -> str:
    """The upstream's own words for why a task failed."""
    response = state.get("response") if isinstance(state, dict) else None
    if not isinstance(response, dict):
        response = state if isinstance(state, dict) else {}
    error = response.get("error")
    if isinstance(error, dict):
        message = error.get("message") or error.get("detail")
        if isinstance(message, str) and message:
            return message
    elif isinstance(error, str) and error:
        return error
    for key in ("message", "failure_reason", "fail_reason"):
        value = response.get(key)
        if isinstance(value, str) and value:
            return value
    return "Task failed."


class _HandleBase:
    def __init__(
        self,
        task_id: str,
        poll_endpoint: str,
        transport: Any,
        submitted: dict[str, Any] | None = None,
    ) -> None:
        self.id = task_id
        self._poll_endpoint = poll_endpoint
        self._transport = transport
        self._result: dict[str, Any] | None = None
        # A submission that already carried the artifact is a finished task. The
        # caller should not have to detect that and skip .wait() themselves.
        if submitted is not None and artifact_urls({"response": submitted}):
            self._result = {"response": submitted}

    @property
    def done(self) -> bool:
        return self._result is not None

    def urls(self) -> list[str]:
        """Artifact URLs, once completed."""
        return artifact_urls(self._result) if self._result else []

    def progress(self) -> int | None:
        return progress(self._result) if self._result else None

    def _accept(self, state: dict[str, Any]) -> str:
        status = task_status(state)
        if status in ("succeeded", "failed"):
            self._result = state
        return status


class TaskHandle(_HandleBase):
    """Synchronous handle for a long-running task."""

    def get(self) -> dict[str, Any]:
        """Fetch current task state, remembering it once terminal.

        A caller that drives its own poll loop — checking status between polls so
        it can report progress — only ever calls this. If a terminal response
        were not recorded here, `urls()` and `result()` would stay empty after
        the task had plainly finished.
        """
        state = self._transport.request(
            "POST",
            self._poll_endpoint,
            json={"id": self.id, "action": "retrieve"},
        )
        self._accept(state)
        return state

    def is_completed(self) -> bool:
        if self.done:
            return True
        self.get()  # records a terminal state as a side effect
        return self.done

    def wait(
        self,
        *,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any]:
        """Poll until the task completes or ``max_wait`` elapses."""
        if self._result is not None:
            return self._result
        start = time.monotonic()
        while time.monotonic() - start < max_wait:
            state = self.get()
            if self.done:
                return state
            time.sleep(poll_interval)
        raise TimeoutError(f"Task {self.id} did not complete within {max_wait}s")

    def result(self) -> dict[str, Any] | None:
        return self._result


class AsyncTaskHandle(_HandleBase):
    """Asynchronous handle for a long-running task."""

    async def get(self) -> dict[str, Any]:
        """Fetch current task state, remembering it once terminal."""
        state = await self._transport.request(
            "POST",
            self._poll_endpoint,
            json={"id": self.id, "action": "retrieve"},
        )
        self._accept(state)
        return state

    async def is_completed(self) -> bool:
        if self.done:
            return True
        await self.get()  # records a terminal state as a side effect
        return self.done

    async def wait(
        self,
        *,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any]:
        if self._result is not None:
            return self._result
        start = time.monotonic()
        while time.monotonic() - start < max_wait:
            state = await self.get()
            if self.done:
                return state
            await asyncio.sleep(poll_interval)
        raise TimeoutError(f"Task {self.id} did not complete within {max_wait}s")

    async def result(self) -> dict[str, Any] | None:
        return self._result


class TimeoutError(Exception):  # noqa: A001 - kept for backwards compatibility
    """Task polling timeout."""


# Kept as a private alias: the original name is referenced by existing callers.
_task_status = task_status
