"""Kling-specific video generation resources."""

from __future__ import annotations

from typing import Any, Literal

KlingModel = Literal[
    "kling-v1",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
    "kling-v3",
    "kling-v3-omni",
    "kling-video-o1",
]


class Kling:
    """Synchronous Kling video client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: Literal["text2video", "image2video", "extend"],
        mode: Literal["std", "pro", "4k"] | None = None,
        model: str | None = None,
        prompt: str | None = None,
        duration: Literal[5, 10] | None = None,
        generate_audio: bool | None = None,
        video_id: str | None = None,
        cfg_scale: float | None = None,
        aspect_ratio: Literal["16:9", "9:16", "1:1"] | None = None,
        callback_url: str | None = None,
        end_image_url: str | None = None,
        camera_control: str | None = None,
        element_list: list[Any] | None = None,
        video_list: list[Any] | None = None,
        negative_prompt: str | None = None,
        start_image_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": action, **kwargs}
        if mode is not None:
            body["mode"] = mode
        if model is not None:
            body["model"] = model
        if prompt is not None:
            body["prompt"] = prompt
        if duration is not None:
            body["duration"] = duration
        if generate_audio is not None:
            body["generate_audio"] = generate_audio
        if video_id is not None:
            body["video_id"] = video_id
        if cfg_scale is not None:
            body["cfg_scale"] = cfg_scale
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if callback_url is not None:
            body["callback_url"] = callback_url
        if end_image_url is not None:
            body["end_image_url"] = end_image_url
        if camera_control is not None:
            body["camera_control"] = camera_control
        if element_list is not None:
            body["element_list"] = element_list
        if video_list is not None:
            body["video_list"] = video_list
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if start_image_url is not None:
            body["start_image_url"] = start_image_url
        return self._transport.request("POST", "/kling/videos", json=body)

    def motion(
        self,
        *,
        mode: Literal["std", "pro"],
        image_url: str,
        video_url: str,
        character_orientation: Literal["image", "video"],
        keep_original_sound: Literal["yes", "no"] | None = None,
        prompt: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "mode": mode,
            "image_url": image_url,
            "video_url": video_url,
            "character_orientation": character_orientation,
            **kwargs,
        }
        if keep_original_sound is not None:
            body["keep_original_sound"] = keep_original_sound
        if prompt is not None:
            body["prompt"] = prompt
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/kling/motion", json=body)


class AsyncKling:
    """Async Kling video client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: Literal["text2video", "image2video", "extend"],
        mode: Literal["std", "pro", "4k"] | None = None,
        model: str | None = None,
        prompt: str | None = None,
        duration: Literal[5, 10] | None = None,
        generate_audio: bool | None = None,
        video_id: str | None = None,
        cfg_scale: float | None = None,
        aspect_ratio: Literal["16:9", "9:16", "1:1"] | None = None,
        callback_url: str | None = None,
        end_image_url: str | None = None,
        camera_control: str | None = None,
        element_list: list[Any] | None = None,
        video_list: list[Any] | None = None,
        negative_prompt: str | None = None,
        start_image_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": action, **kwargs}
        if mode is not None:
            body["mode"] = mode
        if model is not None:
            body["model"] = model
        if prompt is not None:
            body["prompt"] = prompt
        if duration is not None:
            body["duration"] = duration
        if generate_audio is not None:
            body["generate_audio"] = generate_audio
        if video_id is not None:
            body["video_id"] = video_id
        if cfg_scale is not None:
            body["cfg_scale"] = cfg_scale
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if callback_url is not None:
            body["callback_url"] = callback_url
        if end_image_url is not None:
            body["end_image_url"] = end_image_url
        if camera_control is not None:
            body["camera_control"] = camera_control
        if element_list is not None:
            body["element_list"] = element_list
        if video_list is not None:
            body["video_list"] = video_list
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if start_image_url is not None:
            body["start_image_url"] = start_image_url
        return await self._transport.request("POST", "/kling/videos", json=body)

    async def motion(
        self,
        *,
        mode: Literal["std", "pro"],
        image_url: str,
        video_url: str,
        character_orientation: Literal["image", "video"],
        keep_original_sound: Literal["yes", "no"] | None = None,
        prompt: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "mode": mode,
            "image_url": image_url,
            "video_url": video_url,
            "character_orientation": character_orientation,
            **kwargs,
        }
        if keep_original_sound is not None:
            body["keep_original_sound"] = keep_original_sound
        if prompt is not None:
            body["prompt"] = prompt
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/kling/motion", json=body)
