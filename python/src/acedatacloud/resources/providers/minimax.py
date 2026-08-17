"""Minimax (minimax) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MinimaxRatio = Literal[
    "adaptive",
    "21:9",
    "16:9",
    "4:3",
    "1:1",
    "3:4",
    "9:16",
]


def _task_id(result: Any) -> str:
    """Task ids appear at the top level or nested under `data`."""
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


class Minimax:
    """Synchronous minimax client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        model: Literal["MiniMax-H3"],
        content: list[dict[str, Any]],
        duration: int,
        resolution: Literal["768P", "2K"],
        ratio: MinimaxRatio | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Call /minimax/videos."""
        body: dict[str, Any] = {}
        body["model"] = model
        body["content"] = content
        body["duration"] = duration
        body["resolution"] = resolution
        if ratio is not None:
            body["ratio"] = ratio
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/minimax/videos", json=body)
        handle = TaskHandle(_task_id(result), "/minimax/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncMinimax:
    """Asynchronous minimax client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        model: Literal["MiniMax-H3"],
        content: list[dict[str, Any]],
        duration: int,
        resolution: Literal["768P", "2K"],
        ratio: MinimaxRatio | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Call /minimax/videos."""
        body: dict[str, Any] = {}
        body["model"] = model
        body["content"] = content
        body["duration"] = duration
        body["resolution"] = resolution
        if ratio is not None:
            body["ratio"] = ratio
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/minimax/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/minimax/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
