"""Midjourney (midjourney) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MidjourneyVersion = Literal[
    "8.2",
    "8.1",
    "8",
    "7",
    "6.1",
    "6",
    "5.2",
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


class Midjourney:
    """Synchronous midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def imagine(
        self,
        *,
        mask: str | None = None,
        mode: Literal["fast", "relax", "turbo"] | None = None,
        action: str | None = None,
        prompt: str | None = None,
        timeout: float | None = None,
        image_id: str | None = None,
        translation: bool | None = None,
        split_images: bool | None = None,
        version: MidjourneyVersion | None = None,
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
        """Midjourney Imagine"""
        body: dict[str, Any] = {}
        if mask is not None:
            body["mask"] = mask
        body["mode"] = mode if mode is not None else "fast"
        body["action"] = action if action is not None else "generate"
        if prompt is not None:
            body["prompt"] = prompt
        body["timeout"] = timeout if timeout is not None else 480
        if image_id is not None:
            body["image_id"] = image_id
        body["translation"] = translation if translation is not None else False
        body["split_images"] = split_images if split_images is not None else False
        if version is not None:
            body["version"] = version
        body["hd"] = hd if hd is not None else False
        body["quality"] = quality if quality is not None else "1"
        body["style_reference"] = style_reference if style_reference is not None else False
        body["moodboard"] = moodboard if moodboard is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/midjourney/imagine", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def seed(
        self,
        *,
        image_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Seed"""
        body: dict[str, Any] = {}
        body["image_id"] = image_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/seed", json=body)

    def edits(
        self,
        *,
        mask: str | None = None,
        mode: Literal["fast", "relax", "turbo"] | None = None,
        action: str | None = None,
        prompt: str | None = None,
        image_url: str | None = None,
        split_images: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Midjourney Edits"""
        body: dict[str, Any] = {}
        if mask is not None:
            body["mask"] = mask
        if mode is not None:
            body["mode"] = mode
        body["action"] = action if action is not None else "generate"
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        body["split_images"] = split_images if split_images is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/midjourney/edits", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def generate(
        self,
        *,
        action: Literal["generate", "extend"] | None = None,
        mode: Literal["fast", "turbo"] | None = None,
        resolution: Literal["480p", "720p"] | None = None,
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
        """Midjourney Videos"""
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

    def describe(
        self,
        *,
        image_url: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Describe"""
        body: dict[str, Any] = {}
        body["image_url"] = image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/describe", json=body)

    def shorten(
        self,
        *,
        prompt: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Shorten"""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/shorten", json=body)

    def translate(
        self,
        *,
        content: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Translate"""
        body: dict[str, Any] = {}
        body["content"] = content
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/translate", json=body)

    def tasks(
        self,
        *,
        action: Literal["retrieve", "retrieve_batch"] | None = None,
        id: str | None = None,
        trace_id: str | None = None,
        ids: list[str] | None = None,
        trace_ids: list[str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Tasks"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "retrieve"
        if id is not None:
            body["id"] = id
        if trace_id is not None:
            body["trace_id"] = trace_id
        if ids is not None:
            body["ids"] = ids
        if trace_ids is not None:
            body["trace_ids"] = trace_ids
        body["offset"] = offset if offset is not None else 0
        body["limit"] = limit if limit is not None else 12
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/tasks", json=body)


class AsyncMidjourney:
    """Asynchronous midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def imagine(
        self,
        *,
        mask: str | None = None,
        mode: Literal["fast", "relax", "turbo"] | None = None,
        action: str | None = None,
        prompt: str | None = None,
        timeout: float | None = None,
        image_id: str | None = None,
        translation: bool | None = None,
        split_images: bool | None = None,
        version: MidjourneyVersion | None = None,
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
        """Midjourney Imagine"""
        body: dict[str, Any] = {}
        if mask is not None:
            body["mask"] = mask
        body["mode"] = mode if mode is not None else "fast"
        body["action"] = action if action is not None else "generate"
        if prompt is not None:
            body["prompt"] = prompt
        body["timeout"] = timeout if timeout is not None else 480
        if image_id is not None:
            body["image_id"] = image_id
        body["translation"] = translation if translation is not None else False
        body["split_images"] = split_images if split_images is not None else False
        if version is not None:
            body["version"] = version
        body["hd"] = hd if hd is not None else False
        body["quality"] = quality if quality is not None else "1"
        body["style_reference"] = style_reference if style_reference is not None else False
        body["moodboard"] = moodboard if moodboard is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/midjourney/imagine", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def seed(
        self,
        *,
        image_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Seed"""
        body: dict[str, Any] = {}
        body["image_id"] = image_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/seed", json=body)

    async def edits(
        self,
        *,
        mask: str | None = None,
        mode: Literal["fast", "relax", "turbo"] | None = None,
        action: str | None = None,
        prompt: str | None = None,
        image_url: str | None = None,
        split_images: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Midjourney Edits"""
        body: dict[str, Any] = {}
        if mask is not None:
            body["mask"] = mask
        if mode is not None:
            body["mode"] = mode
        body["action"] = action if action is not None else "generate"
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        body["split_images"] = split_images if split_images is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/midjourney/edits", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def generate(
        self,
        *,
        action: Literal["generate", "extend"] | None = None,
        mode: Literal["fast", "turbo"] | None = None,
        resolution: Literal["480p", "720p"] | None = None,
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
        """Midjourney Videos"""
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

    async def describe(
        self,
        *,
        image_url: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Describe"""
        body: dict[str, Any] = {}
        body["image_url"] = image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/describe", json=body)

    async def shorten(
        self,
        *,
        prompt: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Shorten"""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/shorten", json=body)

    async def translate(
        self,
        *,
        content: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Translate"""
        body: dict[str, Any] = {}
        body["content"] = content
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/translate", json=body)

    async def tasks(
        self,
        *,
        action: Literal["retrieve", "retrieve_batch"] | None = None,
        id: str | None = None,
        trace_id: str | None = None,
        ids: list[str] | None = None,
        trace_ids: list[str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Midjourney Tasks"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "retrieve"
        if id is not None:
            body["id"] = id
        if trace_id is not None:
            body["trace_id"] = trace_id
        if ids is not None:
            body["ids"] = ids
        if trace_ids is not None:
            body["trace_ids"] = trace_ids
        body["offset"] = offset if offset is not None else 0
        body["limit"] = limit if limit is not None else 12
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/tasks", json=body)
