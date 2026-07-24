"""Kickart e-commerce video resources."""

from __future__ import annotations

from typing import Any, Literal


class Kickart:
    """Synchronous Kickart client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def videos(
        self,
        *,
        duration: Literal[15, 30, 45, 60],
        mode: Literal["fast", "pro"] | None = None,
        type: Literal["intro", "main"] | None = None,
        template_id: str | None = None,
        product_url: str | None = None,
        product_id: str | None = None,
        user_images: list[str] | None = None,
        user_videos: list[str] | None = None,
        aspect_ratio: Literal["9:16", "16:9", "3:4", "4:3", "1:1"] | None = None,
        language: Literal["zh", "en", "en-us", "pt-br", "ja", "es-mx", "id", "ms", "tl"] | None = None,
        purpose: str | None = None,
        prompt: str | None = None,
        nle_subtitle_enabled: bool | None = None,
        use_subtitle_erasure: bool | None = None,
        watermark: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"duration": duration, **kwargs}
        if mode is not None:
            body["mode"] = mode
        if type is not None:
            body["type"] = type
        if template_id is not None:
            body["template_id"] = template_id
        if product_url is not None:
            body["product_url"] = product_url
        if product_id is not None:
            body["product_id"] = product_id
        if user_images is not None:
            body["user_images"] = user_images
        if user_videos is not None:
            body["user_videos"] = user_videos
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if language is not None:
            body["language"] = language
        if purpose is not None:
            body["purpose"] = purpose
        if prompt is not None:
            body["prompt"] = prompt
        if nle_subtitle_enabled is not None:
            body["nle_subtitle_enabled"] = nle_subtitle_enabled
        if use_subtitle_erasure is not None:
            body["use_subtitle_erasure"] = use_subtitle_erasure
        if watermark is not None:
            body["watermark"] = watermark
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/kickart/videos", json=body)

    def viral_videos(
        self,
        *,
        ref_video: str,
        language: Literal["zh", "en", "en-us", "pt-br", "ja", "es-mx", "id", "ms", "tl"],
        mode: Literal["pro", "advanced"] | None = None,
        template_id: str | None = None,
        product_url: str | None = None,
        product_id: str | None = None,
        product_images: list[str] | None = None,
        model_images: list[str] | None = None,
        ai_product_analysis: bool | None = None,
        similarity: Literal["high", "medium"] | None = None,
        nle_subtitle_enabled: bool | None = None,
        use_subtitle_erasure: bool | None = None,
        prompt: str | None = None,
        location_images: list[str] | None = None,
        watermark: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"ref_video": ref_video, "language": language, **kwargs}
        if mode is not None:
            body["mode"] = mode
        if template_id is not None:
            body["template_id"] = template_id
        if product_url is not None:
            body["product_url"] = product_url
        if product_id is not None:
            body["product_id"] = product_id
        if product_images is not None:
            body["product_images"] = product_images
        if model_images is not None:
            body["model_images"] = model_images
        if ai_product_analysis is not None:
            body["ai_product_analysis"] = ai_product_analysis
        if similarity is not None:
            body["similarity"] = similarity
        if nle_subtitle_enabled is not None:
            body["nle_subtitle_enabled"] = nle_subtitle_enabled
        if use_subtitle_erasure is not None:
            body["use_subtitle_erasure"] = use_subtitle_erasure
        if prompt is not None:
            body["prompt"] = prompt
        if location_images is not None:
            body["location_images"] = location_images
        if watermark is not None:
            body["watermark"] = watermark
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/kickart/viral-videos", json=body)

    def template_videos(
        self,
        *,
        template_id: str,
        resource_list: list[dict[str, Any]],
        resolution: str | None = None,
        watermark: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"template_id": template_id, "resource_list": resource_list, **kwargs}
        if resolution is not None:
            body["resolution"] = resolution
        if watermark is not None:
            body["watermark"] = watermark
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/kickart/template-videos", json=body)


class AsyncKickart:
    """Async Kickart client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def videos(
        self,
        *,
        duration: Literal[15, 30, 45, 60],
        mode: Literal["fast", "pro"] | None = None,
        type: Literal["intro", "main"] | None = None,
        template_id: str | None = None,
        product_url: str | None = None,
        product_id: str | None = None,
        user_images: list[str] | None = None,
        user_videos: list[str] | None = None,
        aspect_ratio: Literal["9:16", "16:9", "3:4", "4:3", "1:1"] | None = None,
        language: Literal["zh", "en", "en-us", "pt-br", "ja", "es-mx", "id", "ms", "tl"] | None = None,
        purpose: str | None = None,
        prompt: str | None = None,
        nle_subtitle_enabled: bool | None = None,
        use_subtitle_erasure: bool | None = None,
        watermark: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"duration": duration, **kwargs}
        if mode is not None:
            body["mode"] = mode
        if type is not None:
            body["type"] = type
        if template_id is not None:
            body["template_id"] = template_id
        if product_url is not None:
            body["product_url"] = product_url
        if product_id is not None:
            body["product_id"] = product_id
        if user_images is not None:
            body["user_images"] = user_images
        if user_videos is not None:
            body["user_videos"] = user_videos
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if language is not None:
            body["language"] = language
        if purpose is not None:
            body["purpose"] = purpose
        if prompt is not None:
            body["prompt"] = prompt
        if nle_subtitle_enabled is not None:
            body["nle_subtitle_enabled"] = nle_subtitle_enabled
        if use_subtitle_erasure is not None:
            body["use_subtitle_erasure"] = use_subtitle_erasure
        if watermark is not None:
            body["watermark"] = watermark
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/kickart/videos", json=body)

    async def viral_videos(
        self,
        *,
        ref_video: str,
        language: Literal["zh", "en", "en-us", "pt-br", "ja", "es-mx", "id", "ms", "tl"],
        mode: Literal["pro", "advanced"] | None = None,
        template_id: str | None = None,
        product_url: str | None = None,
        product_id: str | None = None,
        product_images: list[str] | None = None,
        model_images: list[str] | None = None,
        ai_product_analysis: bool | None = None,
        similarity: Literal["high", "medium"] | None = None,
        nle_subtitle_enabled: bool | None = None,
        use_subtitle_erasure: bool | None = None,
        prompt: str | None = None,
        location_images: list[str] | None = None,
        watermark: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"ref_video": ref_video, "language": language, **kwargs}
        if mode is not None:
            body["mode"] = mode
        if template_id is not None:
            body["template_id"] = template_id
        if product_url is not None:
            body["product_url"] = product_url
        if product_id is not None:
            body["product_id"] = product_id
        if product_images is not None:
            body["product_images"] = product_images
        if model_images is not None:
            body["model_images"] = model_images
        if ai_product_analysis is not None:
            body["ai_product_analysis"] = ai_product_analysis
        if similarity is not None:
            body["similarity"] = similarity
        if nle_subtitle_enabled is not None:
            body["nle_subtitle_enabled"] = nle_subtitle_enabled
        if use_subtitle_erasure is not None:
            body["use_subtitle_erasure"] = use_subtitle_erasure
        if prompt is not None:
            body["prompt"] = prompt
        if location_images is not None:
            body["location_images"] = location_images
        if watermark is not None:
            body["watermark"] = watermark
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/kickart/viral-videos", json=body)

    async def template_videos(
        self,
        *,
        template_id: str,
        resource_list: list[dict[str, Any]],
        resolution: str | None = None,
        watermark: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"template_id": template_id, "resource_list": resource_list, **kwargs}
        if resolution is not None:
            body["resolution"] = resolution
        if watermark is not None:
            body["watermark"] = watermark
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/kickart/template-videos", json=body)
