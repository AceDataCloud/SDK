"""Task polling abstractions for long-running operations."""

from __future__ import annotations

import asyncio
import time
from typing import Any


def _task_status(state: dict[str, Any]) -> str:
    response = state.get("response")
    if response is None:
        response = state
    if not isinstance(response, dict):
        return ""
    status = response.get("status")
    if status in ("succeeded", "failed"):
        return status
    if status is not None:
        return ""
    finished = response.get("finished_at") is not None or state.get("finished_at") is not None
    if not finished:
        return ""
    if response.get("success") is True:
        return "succeeded"
    if response.get("success") is False:
        return "failed"
    return ""


class TaskHandle:
    """Synchronous task handle for polling long-running operations."""

    def __init__(self, task_id: str, poll_endpoint: str, transport: Any) -> None:
        self.id = task_id
        self._poll_endpoint = poll_endpoint
        self._transport = transport
        self._result: dict[str, Any] | None = None

    def get(self) -> dict[str, Any]:
        """Fetch current task state."""
        return self._transport.request(
            "POST",
            self._poll_endpoint,
            json={"id": self.id, "action": "retrieve"},
        )

    def is_completed(self) -> bool:
        state = self.get()
        return _task_status(state) in ("succeeded", "failed")

    def wait(
        self,
        *,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any]:
        """Poll until the task completes or max_wait is reached."""
        start = time.monotonic()
        while time.monotonic() - start < max_wait:
            state = self.get()
            status = _task_status(state)
            if status in ("succeeded", "failed"):
                self._result = state
                return state
            time.sleep(poll_interval)
        raise TimeoutError(f"Task {self.id} did not complete within {max_wait}s")

    def result(self) -> dict[str, Any] | None:
        return self._result


class AsyncTaskHandle:
    """Async task handle for polling long-running operations."""

    def __init__(self, task_id: str, poll_endpoint: str, transport: Any) -> None:
        self.id = task_id
        self._poll_endpoint = poll_endpoint
        self._transport = transport
        self._result: dict[str, Any] | None = None

    async def get(self) -> dict[str, Any]:
        return await self._transport.request(
            "POST",
            self._poll_endpoint,
            json={"id": self.id, "action": "retrieve"},
        )

    async def is_completed(self) -> bool:
        state = await self.get()
        return _task_status(state) in ("succeeded", "failed")

    async def wait(
        self,
        *,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any]:
        start = time.monotonic()
        while time.monotonic() - start < max_wait:
            state = await self.get()
            status = _task_status(state)
            if status in ("succeeded", "failed"):
                self._result = state
                return state
            await asyncio.sleep(poll_interval)
        raise TimeoutError(f"Task {self.id} did not complete within {max_wait}s")

    async def result(self) -> dict[str, Any] | None:
        return self._result


class TimeoutError(Exception):
    """Task polling timeout."""
