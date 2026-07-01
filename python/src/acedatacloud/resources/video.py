"""Video generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

VideoProvider = Literal[
    "sora",
    "luma",
    "veo",
    "kling",
    "hailuo",
    "seedance",
    "wan",
    "pika",
    "pixverse",
    "gemini",
    "grok",
    "dreamina",
]


class Video:
    """Synchronous video generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str | None = None,
        provider: VideoProvider | str = "sora",
        model: str | None = None,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        reference_image_urls: list[str] | None = None,
        audio_url: str | None = None,
        mask_url: list[str] | None = None,
        aspect_ratio: str | None = None,
        duration: str | int | None = None,
        resolution: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if model is not None:
            body["model"] = model
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if reference_image_urls is not None:
            body["reference_image_urls"] = reference_image_urls
        if audio_url is not None:
            body["audio_url"] = audio_url
        if mask_url is not None:
            body["mask_url"] = mask_url
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if duration is not None:
            body["duration"] = duration
        if resolution is not None:
            body["resolution"] = resolution
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        result = self._transport.request("POST", f"/{provider}/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = TaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncVideo:
    """Async video generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str | None = None,
        provider: VideoProvider | str = "sora",
        model: str | None = None,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        reference_image_urls: list[str] | None = None,
        audio_url: str | None = None,
        mask_url: list[str] | None = None,
        aspect_ratio: str | None = None,
        duration: str | int | None = None,
        resolution: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if model is not None:
            body["model"] = model
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if reference_image_urls is not None:
            body["reference_image_urls"] = reference_image_urls
        if audio_url is not None:
            body["audio_url"] = audio_url
        if mask_url is not None:
            body["mask_url"] = mask_url
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if duration is not None:
            body["duration"] = duration
        if resolution is not None:
            body["resolution"] = resolution
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        result = await self._transport.request("POST", f"/{provider}/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
