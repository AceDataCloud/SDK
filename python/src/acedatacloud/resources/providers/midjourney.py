"""Midjourney (midjourney) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MidjourneyMode = Literal["fast", "relax", "turbo"]
MidjourneyVideoMode = Literal["fast", "turbo"]
MidjourneyVideoResolution = Literal["480p", "720p"]
MidjourneyVideoAction = Literal["generate", "extend"]


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


class Midjourney:
    """Synchronous midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def imagine(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: MidjourneyMode | None = None,
        image_id: str | None = None,
        mask: str | None = None,
        timeout: float | None = None,
        translation: bool | None = None,
        split_images: bool | None = None,
        version: str | None = None,
        hd: bool | None = None,
        quality: str | None = None,
        style_reference: bool | None = None,
        moodboard: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Midjourney image generation."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if image_id is not None:
            body["image_id"] = image_id
        if mask is not None:
            body["mask"] = mask
        if timeout is not None:
            body["timeout"] = timeout
        if translation is not None:
            body["translation"] = translation
        if split_images is not None:
            body["split_images"] = split_images
        if version is not None:
            body["version"] = version
        if hd is not None:
            body["hd"] = hd
        if quality is not None:
            body["quality"] = quality
        if style_reference is not None:
            body["style_reference"] = style_reference
        if moodboard is not None:
            body["moodboard"] = moodboard
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/midjourney/imagine", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def edits(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: MidjourneyMode | None = None,
        image_url: str | None = None,
        mask: str | None = None,
        split_images: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Midjourney image editing."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if image_url is not None:
            body["image_url"] = image_url
        if mask is not None:
            body["mask"] = mask
        if split_images is not None:
            body["split_images"] = split_images
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/midjourney/edits", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def videos(
        self,
        *,
        action: MidjourneyVideoAction | None = None,
        mode: MidjourneyVideoMode | None = None,
        resolution: MidjourneyVideoResolution | None = None,
        prompt: str | None = None,
        video_id: str | None = None,
        video_index: float | None = None,
        loop: bool | None = None,
        image_url: str | None = None,
        end_image_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Midjourney video generation."""
        body: dict[str, Any] = {}
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if resolution is not None:
            body["resolution"] = resolution
        if prompt is not None:
            body["prompt"] = prompt
        if video_id is not None:
            body["video_id"] = video_id
        if video_index is not None:
            body["video_index"] = video_index
        if loop is not None:
            body["loop"] = loop
        if image_url is not None:
            body["image_url"] = image_url
        if end_image_url is not None:
            body["end_image_url"] = end_image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/midjourney/videos", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def seed(self, *, image_id: str, **extra: Any) -> dict[str, Any]:
        """Get the seed of a Midjourney image."""
        body: dict[str, Any] = {"image_id": image_id, **extra}
        return self._transport.request("POST", "/midjourney/seed", json=body)

    def describe(self, *, image_url: str, **extra: Any) -> dict[str, Any]:
        """Describe a Midjourney image."""
        body: dict[str, Any] = {"image_url": image_url, **extra}
        return self._transport.request("POST", "/midjourney/describe", json=body)

    def shorten(self, *, prompt: str, **extra: Any) -> dict[str, Any]:
        """Shorten a Midjourney prompt."""
        body: dict[str, Any] = {"prompt": prompt, **extra}
        return self._transport.request("POST", "/midjourney/shorten", json=body)

    def translate(self, *, content: str, **extra: Any) -> dict[str, Any]:
        """Translate text for Midjourney."""
        body: dict[str, Any] = {"content": content, **extra}
        return self._transport.request("POST", "/midjourney/translate", json=body)


class AsyncMidjourney:
    """Asynchronous midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def imagine(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: MidjourneyMode | None = None,
        image_id: str | None = None,
        mask: str | None = None,
        timeout: float | None = None,
        translation: bool | None = None,
        split_images: bool | None = None,
        version: str | None = None,
        hd: bool | None = None,
        quality: str | None = None,
        style_reference: bool | None = None,
        moodboard: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Midjourney image generation."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if image_id is not None:
            body["image_id"] = image_id
        if mask is not None:
            body["mask"] = mask
        if timeout is not None:
            body["timeout"] = timeout
        if translation is not None:
            body["translation"] = translation
        if split_images is not None:
            body["split_images"] = split_images
        if version is not None:
            body["version"] = version
        if hd is not None:
            body["hd"] = hd
        if quality is not None:
            body["quality"] = quality
        if style_reference is not None:
            body["style_reference"] = style_reference
        if moodboard is not None:
            body["moodboard"] = moodboard
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/midjourney/imagine", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def edits(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: MidjourneyMode | None = None,
        image_url: str | None = None,
        mask: str | None = None,
        split_images: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Midjourney image editing."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if image_url is not None:
            body["image_url"] = image_url
        if mask is not None:
            body["mask"] = mask
        if split_images is not None:
            body["split_images"] = split_images
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/midjourney/edits", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def videos(
        self,
        *,
        action: MidjourneyVideoAction | None = None,
        mode: MidjourneyVideoMode | None = None,
        resolution: MidjourneyVideoResolution | None = None,
        prompt: str | None = None,
        video_id: str | None = None,
        video_index: float | None = None,
        loop: bool | None = None,
        image_url: str | None = None,
        end_image_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Midjourney video generation."""
        body: dict[str, Any] = {}
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if resolution is not None:
            body["resolution"] = resolution
        if prompt is not None:
            body["prompt"] = prompt
        if video_id is not None:
            body["video_id"] = video_id
        if video_index is not None:
            body["video_index"] = video_index
        if loop is not None:
            body["loop"] = loop
        if image_url is not None:
            body["image_url"] = image_url
        if end_image_url is not None:
            body["end_image_url"] = end_image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/midjourney/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def seed(self, *, image_id: str, **extra: Any) -> dict[str, Any]:
        """Get the seed of a Midjourney image."""
        body: dict[str, Any] = {"image_id": image_id, **extra}
        return await self._transport.request("POST", "/midjourney/seed", json=body)

    async def describe(self, *, image_url: str, **extra: Any) -> dict[str, Any]:
        """Describe a Midjourney image."""
        body: dict[str, Any] = {"image_url": image_url, **extra}
        return await self._transport.request("POST", "/midjourney/describe", json=body)

    async def shorten(self, *, prompt: str, **extra: Any) -> dict[str, Any]:
        """Shorten a Midjourney prompt."""
        body: dict[str, Any] = {"prompt": prompt, **extra}
        return await self._transport.request("POST", "/midjourney/shorten", json=body)

    async def translate(self, *, content: str, **extra: Any) -> dict[str, Any]:
        """Translate text for Midjourney."""
        body: dict[str, Any] = {"content": content, **extra}
        return await self._transport.request("POST", "/midjourney/translate", json=body)
