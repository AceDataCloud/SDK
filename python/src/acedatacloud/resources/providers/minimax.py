"""MiniMax H3 video generation provider."""

from __future__ import annotations

from typing import Any, Literal

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MinimaxModel = Literal["MiniMax-H3"]
MinimaxResolution = Literal["768P", "2K"]
MinimaxRatio = Literal["adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
MinimaxContentType = Literal["text", "image_url", "video_url", "audio_url"]
MinimaxContentRole = Literal[
    "first_frame",
    "last_frame",
    "reference_image",
    "reference_video",
    "reference_audio",
]


def _task_id(result: Any) -> str:
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


def _validate(content: list[dict[str, Any]], duration: int) -> None:
    if not 4 <= duration <= 15:
        raise ValueError("duration must be between 4 and 15 seconds")
    if not content:
        raise ValueError("content must contain at least one item")
    for item in content:
        if item.get("type") not in ("text", "image_url", "video_url", "audio_url"):
            raise ValueError("each content item must have a valid type")


class Minimax:
    """Synchronous MiniMax client."""

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
        aigc_watermark: bool = False,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
    ) -> TaskHandle:
        """Generate a MiniMax H3 video."""
        _validate(content, duration)
        body: dict[str, Any] = {
            "model": model,
            "content": content,
            "resolution": resolution,
            "duration": duration,
            "aigc_watermark": aigc_watermark,
        }
        if ratio is not None:
            body["ratio"] = ratio
        if callback_url is not None:
            body["callback_url"] = callback_url
        result = self._transport.request("POST", "/minimax/videos", json=body)
        handle = TaskHandle(_task_id(result), "/minimax/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncMinimax:
    """Asynchronous MiniMax client."""

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
        aigc_watermark: bool = False,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
    ) -> AsyncTaskHandle:
        """Generate a MiniMax H3 video."""
        _validate(content, duration)
        body: dict[str, Any] = {
            "model": model,
            "content": content,
            "resolution": resolution,
            "duration": duration,
            "aigc_watermark": aigc_watermark,
        }
        if ratio is not None:
            body["ratio"] = ratio
        if callback_url is not None:
            body["callback_url"] = callback_url
        result = await self._transport.request("POST", "/minimax/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/minimax/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
