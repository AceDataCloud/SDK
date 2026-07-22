"""Midjourney image/video generation resources."""

from __future__ import annotations

from typing import Any


class Midjourney:
    """Synchronous Midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def imagine(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: str | None = None,
        mask: str | None = None,
        image_id: str | None = None,
        translation: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        split_images: bool | None = None,
        version: str | None = None,
        hd: bool | None = None,
        quality: str | None = None,
        style_reference: bool | None = None,
        moodboard: bool | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if mask is not None:
            body["mask"] = mask
        if image_id is not None:
            body["image_id"] = image_id
        if translation is not None:
            body["translation"] = translation
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
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
        if timeout is not None:
            body["timeout"] = timeout
        return self._transport.request("POST", "/midjourney/imagine", json=body)

    def seed(
        self,
        *,
        image_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image_id": image_id, **kwargs}
        return self._transport.request("POST", "/midjourney/seed", json=body)

    def edits(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: str | None = None,
        mask: str | None = None,
        image_url: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        split_images: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if mask is not None:
            body["mask"] = mask
        if image_url is not None:
            body["image_url"] = image_url
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        if split_images is not None:
            body["split_images"] = split_images
        return self._transport.request("POST", "/midjourney/edits", json=body)

    def videos(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: str | None = None,
        resolution: str | None = None,
        video_id: str | None = None,
        video_index: int | None = None,
        loop: bool | None = None,
        image_url: str | None = None,
        end_image_url: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if resolution is not None:
            body["resolution"] = resolution
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
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/midjourney/videos", json=body)

    def describe(
        self,
        *,
        image_url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image_url": image_url, **kwargs}
        return self._transport.request("POST", "/midjourney/describe", json=body)

    def shorten(
        self,
        *,
        prompt: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return self._transport.request("POST", "/midjourney/shorten", json=body)

    def translate(
        self,
        *,
        content: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"content": content, **kwargs}
        return self._transport.request("POST", "/midjourney/translate", json=body)


class AsyncMidjourney:
    """Async Midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def imagine(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: str | None = None,
        mask: str | None = None,
        image_id: str | None = None,
        translation: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        split_images: bool | None = None,
        version: str | None = None,
        hd: bool | None = None,
        quality: str | None = None,
        style_reference: bool | None = None,
        moodboard: bool | None = None,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if mask is not None:
            body["mask"] = mask
        if image_id is not None:
            body["image_id"] = image_id
        if translation is not None:
            body["translation"] = translation
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
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
        if timeout is not None:
            body["timeout"] = timeout
        return await self._transport.request("POST", "/midjourney/imagine", json=body)

    async def seed(
        self,
        *,
        image_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image_id": image_id, **kwargs}
        return await self._transport.request("POST", "/midjourney/seed", json=body)

    async def edits(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: str | None = None,
        mask: str | None = None,
        image_url: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        split_images: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if mask is not None:
            body["mask"] = mask
        if image_url is not None:
            body["image_url"] = image_url
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        if split_images is not None:
            body["split_images"] = split_images
        return await self._transport.request("POST", "/midjourney/edits", json=body)

    async def videos(
        self,
        *,
        prompt: str | None = None,
        action: str | None = None,
        mode: str | None = None,
        resolution: str | None = None,
        video_id: str | None = None,
        video_index: int | None = None,
        loop: bool | None = None,
        image_url: str | None = None,
        end_image_url: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if resolution is not None:
            body["resolution"] = resolution
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
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/midjourney/videos", json=body)

    async def describe(
        self,
        *,
        image_url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image_url": image_url, **kwargs}
        return await self._transport.request("POST", "/midjourney/describe", json=body)

    async def shorten(
        self,
        *,
        prompt: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return await self._transport.request("POST", "/midjourney/shorten", json=body)

    async def translate(
        self,
        *,
        content: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"content": content, **kwargs}
        return await self._transport.request("POST", "/midjourney/translate", json=body)
