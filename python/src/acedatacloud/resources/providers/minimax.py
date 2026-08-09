"""Minimax (minimax) — provider-axis client."""

from __future__ import annotations

from typing import Any, Literal

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MinimaxModel = Literal["MiniMax-H3"]
MinimaxContentType = Literal["text", "image_url", "video_url", "audio_url"]
MinimaxContentRole = Literal[
    "first_frame",
    "last_frame",
    "reference_image",
    "reference_video",
    "reference_audio",
]
MinimaxResolution = Literal["768P", "2K"]
MinimaxRatio = Literal["adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]


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
        model: MinimaxModel,
        content: list[dict[str, Any]],
        resolution: MinimaxResolution,
        duration: int,
        ratio: MinimaxRatio | None = None,
        callback_url: str | None = None,
        aigc_watermark: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> TaskHandle:
        """Minimax Videos."""
        body: dict[str, Any] = {
            "model": model,
            "content": content,
            "resolution": resolution,
            "duration": duration,
        }
        if ratio is not None:
            body["ratio"] = ratio
        if callback_url is not None:
            body["callback_url"] = callback_url
        if aigc_watermark is not None:
            body["aigc_watermark"] = aigc_watermark
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
        model: MinimaxModel,
        content: list[dict[str, Any]],
        resolution: MinimaxResolution,
        duration: int,
        ratio: MinimaxRatio | None = None,
        callback_url: str | None = None,
        aigc_watermark: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> AsyncTaskHandle:
        """Minimax Videos."""
        body: dict[str, Any] = {
            "model": model,
            "content": content,
            "resolution": resolution,
            "duration": duration,
        }
        if ratio is not None:
            body["ratio"] = ratio
        if callback_url is not None:
            body["callback_url"] = callback_url
        if aigc_watermark is not None:
            body["aigc_watermark"] = aigc_watermark
        result = await self._transport.request("POST", "/minimax/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/minimax/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
