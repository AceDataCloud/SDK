"""Midjourney (midjourney) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MidjourneyMode = Literal["fast", "relax", "turbo"]
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
        image_id: str | None = None,
        mask: str | None = None,
        mode: MidjourneyMode | None = None,
        action: str | None = None,
        timeout: float | None = None,
        translation: bool | None = None,
        split_images: bool | None = None,
        version: str | None = None,
        hd: bool | None = None,
        quality: str | None = None,
        style_reference: bool | None = None,
        moodboard: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Midjourney image generation API."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if image_id is not None:
            body["image_id"] = image_id
        if mask is not None:
            body["mask"] = mask
        if mode is not None:
            body["mode"] = mode
        if action is not None:
            body["action"] = action
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
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/midjourney/imagine", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        return handle

    def edits(
        self,
        *,
        prompt: str | None = None,
        image_url: str | None = None,
        mask: str | None = None,
        mode: MidjourneyMode | None = None,
        action: str | None = None,
        split_images: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Midjourney image editing API."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if mask is not None:
            body["mask"] = mask
        if mode is not None:
            body["mode"] = mode
        if action is not None:
            body["action"] = action
        if split_images is not None:
            body["split_images"] = split_images
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/midjourney/edits", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        return handle

    def videos(
        self,
        *,
        action: MidjourneyVideoAction | None = None,
        mode: Literal["fast", "turbo"] | None = None,
        resolution: MidjourneyVideoResolution | None = None,
        prompt: str | None = None,
        video_id: str | None = None,
        video_index: float | None = None,
        loop: bool | None = None,
        image_url: str | None = None,
        end_image_url: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Midjourney video generation API."""
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
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/midjourney/videos", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        return handle

    def seed(self, *, image_id: str) -> dict[str, Any]:
        """Get the seed for a Midjourney image."""
        return self._transport.request("POST", "/midjourney/seed", json={"image_id": image_id})

    def describe(self, *, image_url: str) -> dict[str, Any]:
        """Describe a Midjourney image."""
        return self._transport.request("POST", "/midjourney/describe", json={"image_url": image_url})

    def shorten(self, *, prompt: str) -> dict[str, Any]:
        """Shorten a Midjourney prompt."""
        return self._transport.request("POST", "/midjourney/shorten", json={"prompt": prompt})

    def translate(self, *, content: str) -> dict[str, Any]:
        """Translate content for Midjourney."""
        return self._transport.request("POST", "/midjourney/translate", json={"content": content})


class AsyncMidjourney:
    """Asynchronous midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def imagine(
        self,
        *,
        prompt: str | None = None,
        image_id: str | None = None,
        mask: str | None = None,
        mode: MidjourneyMode | None = None,
        action: str | None = None,
        timeout: float | None = None,
        translation: bool | None = None,
        split_images: bool | None = None,
        version: str | None = None,
        hd: bool | None = None,
        quality: str | None = None,
        style_reference: bool | None = None,
        moodboard: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Midjourney image generation API."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if image_id is not None:
            body["image_id"] = image_id
        if mask is not None:
            body["mask"] = mask
        if mode is not None:
            body["mode"] = mode
        if action is not None:
            body["action"] = action
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
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/midjourney/imagine", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        return handle

    async def edits(
        self,
        *,
        prompt: str | None = None,
        image_url: str | None = None,
        mask: str | None = None,
        mode: MidjourneyMode | None = None,
        action: str | None = None,
        split_images: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Midjourney image editing API."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if mask is not None:
            body["mask"] = mask
        if mode is not None:
            body["mode"] = mode
        if action is not None:
            body["action"] = action
        if split_images is not None:
            body["split_images"] = split_images
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/midjourney/edits", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        return handle

    async def videos(
        self,
        *,
        action: MidjourneyVideoAction | None = None,
        mode: Literal["fast", "turbo"] | None = None,
        resolution: MidjourneyVideoResolution | None = None,
        prompt: str | None = None,
        video_id: str | None = None,
        video_index: float | None = None,
        loop: bool | None = None,
        image_url: str | None = None,
        end_image_url: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Midjourney video generation API."""
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
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/midjourney/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        return handle

    async def seed(self, *, image_id: str) -> dict[str, Any]:
        """Get the seed for a Midjourney image."""
        return await self._transport.request("POST", "/midjourney/seed", json={"image_id": image_id})

    async def describe(self, *, image_url: str) -> dict[str, Any]:
        """Describe a Midjourney image."""
        return await self._transport.request("POST", "/midjourney/describe", json={"image_url": image_url})

    async def shorten(self, *, prompt: str) -> dict[str, Any]:
        """Shorten a Midjourney prompt."""
        return await self._transport.request("POST", "/midjourney/shorten", json={"prompt": prompt})

    async def translate(self, *, content: str) -> dict[str, Any]:
        """Translate content for Midjourney."""
        return await self._transport.request("POST", "/midjourney/translate", json={"content": content})
