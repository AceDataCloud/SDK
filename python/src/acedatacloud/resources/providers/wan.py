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
        action: Literal["text2video", "image2video"],
        prompt: str,
        size: str | None = None,
        audio: bool | None = None,
        duration: float | None = None,
        audio_url: str | None = None,
        image_url: str | None = None,
        shot_type: Literal["single", "multi"] | None = None,
        resolution: Literal["480P", "720P", "1080P"] | None = None,
        prompt_extend: bool | None = None,
        negative_prompt: str | None = None,
        reference_video_urls: list[str] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Generate videos based on prompt and image frames"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["action"] = action
        body["prompt"] = prompt
        if size is not None:
            body["size"] = size
        body["audio"] = audio if audio is not None else False
        if duration is not None:
            body["duration"] = duration
        if audio_url is not None:
            body["audio_url"] = audio_url
        body["image_url"] = image_url if image_url is not None else "https://cdn.acedata.cloud/r9vsv9.png"
        if shot_type is not None:
            body["shot_type"] = shot_type
        if resolution is not None:
            body["resolution"] = resolution
        body["prompt_extend"] = prompt_extend if prompt_extend is not None else False
        body["negative_prompt"] = (
            negative_prompt if negative_prompt is not None else "Astronauts shuttle from space to volcano"
        )
        if reference_video_urls is not None:
            body["reference_video_urls"] = reference_video_urls
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
        action: Literal["text2video", "image2video"],
        prompt: str,
        size: str | None = None,
        audio: bool | None = None,
        duration: float | None = None,
        audio_url: str | None = None,
        image_url: str | None = None,
        shot_type: Literal["single", "multi"] | None = None,
        resolution: Literal["480P", "720P", "1080P"] | None = None,
        prompt_extend: bool | None = None,
        negative_prompt: str | None = None,
        reference_video_urls: list[str] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Generate videos based on prompt and image frames"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["action"] = action
        body["prompt"] = prompt
        if size is not None:
            body["size"] = size
        body["audio"] = audio if audio is not None else False
        if duration is not None:
            body["duration"] = duration
        if audio_url is not None:
            body["audio_url"] = audio_url
        body["image_url"] = image_url if image_url is not None else "https://cdn.acedata.cloud/r9vsv9.png"
        if shot_type is not None:
            body["shot_type"] = shot_type
        if resolution is not None:
            body["resolution"] = resolution
        body["prompt_extend"] = prompt_extend if prompt_extend is not None else False
        body["negative_prompt"] = (
            negative_prompt if negative_prompt is not None else "Astronauts shuttle from space to volcano"
        )
        if reference_video_urls is not None:
            body["reference_video_urls"] = reference_video_urls
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/wan/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/wan/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
