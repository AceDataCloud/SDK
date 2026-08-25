"""Wan (wan) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

WanModel = Literal[
    "wan2.6-i2v",
    "wan2.6-r2v",
    "wan2.6-i2v-flash",
    "wan2.6-t2v",
    "wan3.0-video",
]
WanRatio = Literal[
    "adaptive",
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


class Wan:
    """Synchronous wan client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        model: WanModel,
        audio: bool | None = None,
        prompt_extend: bool | None = None,
        action: Literal["text2video", "image2video"] | None = None,
        resolution: Literal["480P", "720P", "1080P"] | None = None,
        shot_type: Literal["single", "multi"] | None = None,
        duration: float | None = None,
        prompt: str | None = None,
        negative_prompt: str | None = None,
        size: str | None = None,
        audio_url: str | None = None,
        reference_video_urls: list[str] | None = None,
        image_url: str | None = None,
        media: list[dict[str, Any]] | None = None,
        ratio: WanRatio | None = None,
        seed: int | None = None,
        watermark: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Wan Videos"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["audio"] = audio if audio is not None else False
        body["prompt_extend"] = prompt_extend if prompt_extend is not None else False
        body["action"] = action if action is not None else "text2video"
        if resolution is not None:
            body["resolution"] = resolution
        if shot_type is not None:
            body["shot_type"] = shot_type
        if duration is not None:
            body["duration"] = duration
        if prompt is not None:
            body["prompt"] = prompt
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if size is not None:
            body["size"] = size
        if audio_url is not None:
            body["audio_url"] = audio_url
        if reference_video_urls is not None:
            body["reference_video_urls"] = reference_video_urls
        if image_url is not None:
            body["image_url"] = image_url
        if media is not None:
            body["media"] = media
        if ratio is not None:
            body["ratio"] = ratio
        if seed is not None:
            body["seed"] = seed
        body["watermark"] = watermark if watermark is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/wan/videos", json=body)
        handle = TaskHandle(_task_id(result), "/wan/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncWan:
    """Asynchronous wan client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        model: WanModel,
        audio: bool | None = None,
        prompt_extend: bool | None = None,
        action: Literal["text2video", "image2video"] | None = None,
        resolution: Literal["480P", "720P", "1080P"] | None = None,
        shot_type: Literal["single", "multi"] | None = None,
        duration: float | None = None,
        prompt: str | None = None,
        negative_prompt: str | None = None,
        size: str | None = None,
        audio_url: str | None = None,
        reference_video_urls: list[str] | None = None,
        image_url: str | None = None,
        media: list[dict[str, Any]] | None = None,
        ratio: WanRatio | None = None,
        seed: int | None = None,
        watermark: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Wan Videos"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["audio"] = audio if audio is not None else False
        body["prompt_extend"] = prompt_extend if prompt_extend is not None else False
        body["action"] = action if action is not None else "text2video"
        if resolution is not None:
            body["resolution"] = resolution
        if shot_type is not None:
            body["shot_type"] = shot_type
        if duration is not None:
            body["duration"] = duration
        if prompt is not None:
            body["prompt"] = prompt
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if size is not None:
            body["size"] = size
        if audio_url is not None:
            body["audio_url"] = audio_url
        if reference_video_urls is not None:
            body["reference_video_urls"] = reference_video_urls
        if image_url is not None:
            body["image_url"] = image_url
        if media is not None:
            body["media"] = media
        if ratio is not None:
            body["ratio"] = ratio
        if seed is not None:
            body["seed"] = seed
        body["watermark"] = watermark if watermark is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/wan/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/wan/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
