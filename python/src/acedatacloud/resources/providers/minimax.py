"""Minimax (minimax) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict  # noqa: F401

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


class MinimaxMediaUrl(TypedDict):
    url: str


class MinimaxTextContent(TypedDict):
    type: Literal["text"]
    text: str


class _MinimaxImageContentRequired(TypedDict):
    type: Literal["image_url"]
    image_url: MinimaxMediaUrl


class MinimaxImageContent(_MinimaxImageContentRequired, total=False):
    role: Literal["first_frame", "last_frame", "reference_image"]


class MinimaxVideoContent(TypedDict):
    type: Literal["video_url"]
    video_url: MinimaxMediaUrl
    role: Literal["reference_video"]


class MinimaxAudioContent(TypedDict):
    type: Literal["audio_url"]
    audio_url: MinimaxMediaUrl
    role: Literal["reference_audio"]


MinimaxContentItem = MinimaxTextContent | MinimaxImageContent | MinimaxVideoContent | MinimaxAudioContent


def _validate_content_item(item: dict[str, Any]) -> None:
    kind = item.get("type")
    if kind == "text":
        text = item.get("text")
        if not isinstance(text, str) or not text:
            raise ValueError("minimax.content item with type='text' requires non-empty text")
        return
    if kind == "image_url":
        if not isinstance(item.get("image_url"), dict) or not isinstance(item["image_url"].get("url"), str):
            raise ValueError("minimax.content item with type='image_url' requires image_url.url")
        role = item.get("role")
        if role is not None and role not in {"first_frame", "last_frame", "reference_image"}:
            raise ValueError(
                "minimax.content item with type='image_url' role must be first_frame, last_frame, or reference_image"
            )
        return
    if kind == "video_url":
        if not isinstance(item.get("video_url"), dict) or not isinstance(item["video_url"].get("url"), str):
            raise ValueError("minimax.content item with type='video_url' requires video_url.url")
        if item.get("role") != "reference_video":
            raise ValueError("minimax.content item with type='video_url' requires role='reference_video'")
        return
    if kind == "audio_url":
        if not isinstance(item.get("audio_url"), dict) or not isinstance(item["audio_url"].get("url"), str):
            raise ValueError("minimax.content item with type='audio_url' requires audio_url.url")
        if item.get("role") != "reference_audio":
            raise ValueError("minimax.content item with type='audio_url' requires role='reference_audio'")
        return
    raise ValueError("minimax.content item type must be one of: text, image_url, video_url, audio_url")


def _validate_generate_args(content: list[dict[str, Any]], duration: int) -> None:
    if not content:
        raise ValueError("minimax.content must contain at least one item")
    for item in content:
        if not isinstance(item, dict):
            raise ValueError("minimax.content items must be objects")
        _validate_content_item(item)
    if duration < 4 or duration > 15:
        raise ValueError("minimax.duration must be between 4 and 15 seconds")


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
        content: list[MinimaxContentItem],
        resolution: Literal["768P", "2K"],
        duration: int,
        ratio: MinimaxRatio | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Minimax Videos"""
        _validate_generate_args(content, duration)
        body: dict[str, Any] = {}
        body["model"] = model
        body["content"] = content
        body["resolution"] = resolution
        body["duration"] = duration
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
        content: list[MinimaxContentItem],
        resolution: Literal["768P", "2K"],
        duration: int,
        ratio: MinimaxRatio | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Minimax Videos"""
        _validate_generate_args(content, duration)
        body: dict[str, Any] = {}
        body["model"] = model
        body["content"] = content
        body["resolution"] = resolution
        body["duration"] = duration
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
