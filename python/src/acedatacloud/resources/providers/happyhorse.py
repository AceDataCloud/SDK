"""Happyhorse (happyhorse) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

HappyhorseAction = Literal[
    "generate",
    "image_to_video",
    "reference_to_video",
    "video_edit",
]
HappyhorseModel = Literal[
    "happyhorse-1.0-t2v",
    "happyhorse-1.1-t2v",
    "happyhorse-1.0-i2v",
    "happyhorse-1.1-i2v",
    "happyhorse-1.0-r2v",
    "happyhorse-1.1-r2v",
    "happyhorse-1.0-video-edit",
]
HappyhorseRatio = Literal[
    "16:9",
    "9:16",
    "1:1",
    "4:3",
    "3:4",
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


class Happyhorse:
    """Synchronous happyhorse client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: HappyhorseAction | None = None,
        model: HappyhorseModel | None = None,
        prompt: str | None = None,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        video_url: str | None = None,
        resolution: Literal["720P", "1080P"] | None = None,
        ratio: HappyhorseRatio | None = None,
        duration: int | None = None,
        watermark: bool | None = None,
        audio_setting: Literal["auto", "origin"] | None = None,
        seed: int | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Happyhorse Videos"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "generate"
        body["model"] = model if model is not None else "happyhorse-1.1-t2v"
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_url is not None:
            body["video_url"] = video_url
        body["resolution"] = resolution if resolution is not None else "1080P"
        body["ratio"] = ratio if ratio is not None else "16:9"
        body["duration"] = duration if duration is not None else 5
        body["watermark"] = watermark if watermark is not None else False
        body["audio_setting"] = audio_setting if audio_setting is not None else "auto"
        if seed is not None:
            body["seed"] = seed
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/happyhorse/videos", json=body)
        handle = TaskHandle(_task_id(result), "/happyhorse/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncHappyhorse:
    """Asynchronous happyhorse client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: HappyhorseAction | None = None,
        model: HappyhorseModel | None = None,
        prompt: str | None = None,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        video_url: str | None = None,
        resolution: Literal["720P", "1080P"] | None = None,
        ratio: HappyhorseRatio | None = None,
        duration: int | None = None,
        watermark: bool | None = None,
        audio_setting: Literal["auto", "origin"] | None = None,
        seed: int | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Happyhorse Videos"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "generate"
        body["model"] = model if model is not None else "happyhorse-1.1-t2v"
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_url is not None:
            body["video_url"] = video_url
        body["resolution"] = resolution if resolution is not None else "1080P"
        body["ratio"] = ratio if ratio is not None else "16:9"
        body["duration"] = duration if duration is not None else 5
        body["watermark"] = watermark if watermark is not None else False
        body["audio_setting"] = audio_setting if audio_setting is not None else "auto"
        if seed is not None:
            body["seed"] = seed
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/happyhorse/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/happyhorse/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
