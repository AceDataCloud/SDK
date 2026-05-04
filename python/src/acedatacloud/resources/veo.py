"""Veo-specific video generation and editing resources."""

from __future__ import annotations

from typing import Any, Literal

VeoModel = Literal["veo2", "veo2-fast", "veo3", "veo3-fast", "veo31-fast", "veo31", "veo31-fast-ingredients"]


class Veo:
    """Synchronous Veo video client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: Literal["text2video", "image2video", "ingredients2video", "get1080p"],
        prompt: str | None = None,
        model: str | None = None,
        resolution: Literal["4k", "1080p", "gif"] | None = None,
        video_id: str | None = None,
        translation: str | None = None,
        aspect_ratio: Literal["9:16", "1:1", "3:4", "4:3", "16:9"] | None = None,
        image_urls: list[str] | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": action, **kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if model is not None:
            body["model"] = model
        if resolution is not None:
            body["resolution"] = resolution
        if video_id is not None:
            body["video_id"] = video_id
        if translation is not None:
            body["translation"] = translation
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if image_urls is not None:
            body["image_urls"] = image_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/veo/videos", json=body)

    def upsample(
        self,
        *,
        video_id: str,
        action: Literal["1080p", "4k", "gif"],
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"video_id": video_id, "action": action, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/veo/upsample", json=body)

    def extend(
        self,
        *,
        video_id: str,
        model: str,
        prompt: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"video_id": video_id, "model": model, **kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/veo/extend", json=body)

    def reshoot(
        self,
        *,
        video_id: str,
        motion_type: str,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"video_id": video_id, "motion_type": motion_type, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/veo/reshoot", json=body)

    def objects(
        self,
        *,
        video_id: str,
        action: Literal["insert", "remove"],
        prompt: str | None = None,
        image_mask: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"video_id": video_id, "action": action, **kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if image_mask is not None:
            body["image_mask"] = image_mask
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/veo/objects", json=body)


class AsyncVeo:
    """Async Veo video client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: Literal["text2video", "image2video", "ingredients2video", "get1080p"],
        prompt: str | None = None,
        model: str | None = None,
        resolution: Literal["4k", "1080p", "gif"] | None = None,
        video_id: str | None = None,
        translation: str | None = None,
        aspect_ratio: Literal["9:16", "1:1", "3:4", "4:3", "16:9"] | None = None,
        image_urls: list[str] | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": action, **kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if model is not None:
            body["model"] = model
        if resolution is not None:
            body["resolution"] = resolution
        if video_id is not None:
            body["video_id"] = video_id
        if translation is not None:
            body["translation"] = translation
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if image_urls is not None:
            body["image_urls"] = image_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/veo/videos", json=body)

    async def upsample(
        self,
        *,
        video_id: str,
        action: Literal["1080p", "4k", "gif"],
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"video_id": video_id, "action": action, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/veo/upsample", json=body)

    async def extend(
        self,
        *,
        video_id: str,
        model: str,
        prompt: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"video_id": video_id, "model": model, **kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/veo/extend", json=body)

    async def reshoot(
        self,
        *,
        video_id: str,
        motion_type: str,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"video_id": video_id, "motion_type": motion_type, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/veo/reshoot", json=body)

    async def objects(
        self,
        *,
        video_id: str,
        action: Literal["insert", "remove"],
        prompt: str | None = None,
        image_mask: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"video_id": video_id, "action": action, **kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if image_mask is not None:
            body["image_mask"] = image_mask
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/veo/objects", json=body)
