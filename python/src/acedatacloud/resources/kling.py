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
        async_: bool | None = None,
        end_image_url: str | None = None,
        camera_control: str | None = None,
        element_list: list[Any] | None = None,
        image_list: list[dict[str, Any]] | None = None,
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
        if async_ is not None:
            body["async"] = async_
        if end_image_url is not None:
            body["end_image_url"] = end_image_url
        if camera_control is not None:
            body["camera_control"] = camera_control
        if element_list is not None:
            body["element_list"] = element_list
        if image_list is not None:
            body["image_list"] = image_list
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
        model_name: Literal["kling-v2-6", "kling-v3"] | None = None,
        mode: Literal["std", "pro"],
        watermark_info: dict[str, Any] | None = None,
        image_url: str,
        video_url: str,
        character_orientation: Literal["image", "video"],
        keep_original_sound: Literal["yes", "no"] | None = None,
        prompt: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "mode": mode,
            "image_url": image_url,
            "video_url": video_url,
            "character_orientation": character_orientation,
            **kwargs,
        }
        if model_name is not None:
            body["model_name"] = model_name
        if watermark_info is not None:
            body["watermark_info"] = watermark_info
        if keep_original_sound is not None:
            body["keep_original_sound"] = keep_original_sound
        if prompt is not None:
            body["prompt"] = prompt
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/kling/motion", json=body)

    def lip_sync(
        self,
        *,
        mode: Literal["audio2video", "text2video"],
        video_id: str | None = None,
        video_url: str | None = None,
        audio_url: str | None = None,
        audio_type: Literal["url", "file"] | None = None,
        audio_file: str | None = None,
        text: str | None = None,
        voice_id: str | None = None,
        voice_language: Literal["zh", "en"] | None = None,
        voice_speed: float | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"mode": mode, **kwargs}
        if video_id is not None:
            body["video_id"] = video_id
        if video_url is not None:
            body["video_url"] = video_url
        if audio_url is not None:
            body["audio_url"] = audio_url
        if audio_type is not None:
            body["audio_type"] = audio_type
        if audio_file is not None:
            body["audio_file"] = audio_file
        if text is not None:
            body["text"] = text
        if voice_id is not None:
            body["voice_id"] = voice_id
        if voice_language is not None:
            body["voice_language"] = voice_language
        if voice_speed is not None:
            body["voice_speed"] = voice_speed
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/kling/lip-sync", json=body)

    def talking_photo(
        self,
        *,
        image_url: str,
        audio_url: str,
        prompt: str | None = None,
        model: Literal[
            "kling-v1",
            "kling-v1-6",
            "kling-v2-master",
            "kling-v2-1-master",
            "kling-v2-5-turbo",
            "kling-v2-6",
        ]
        | None = None,
        duration: Literal[5, 10] | None = None,
        mode: Literal["std", "pro"] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image_url": image_url, "audio_url": audio_url, **kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if model is not None:
            body["model"] = model
        if duration is not None:
            body["duration"] = duration
        if mode is not None:
            body["mode"] = mode
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/kling/talking-photo", json=body)


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
        async_: bool | None = None,
        end_image_url: str | None = None,
        camera_control: str | None = None,
        element_list: list[Any] | None = None,
        image_list: list[dict[str, Any]] | None = None,
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
        if async_ is not None:
            body["async"] = async_
        if end_image_url is not None:
            body["end_image_url"] = end_image_url
        if camera_control is not None:
            body["camera_control"] = camera_control
        if element_list is not None:
            body["element_list"] = element_list
        if image_list is not None:
            body["image_list"] = image_list
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
        model_name: Literal["kling-v2-6", "kling-v3"] | None = None,
        mode: Literal["std", "pro"],
        watermark_info: dict[str, Any] | None = None,
        image_url: str,
        video_url: str,
        character_orientation: Literal["image", "video"],
        keep_original_sound: Literal["yes", "no"] | None = None,
        prompt: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "mode": mode,
            "image_url": image_url,
            "video_url": video_url,
            "character_orientation": character_orientation,
            **kwargs,
        }
        if model_name is not None:
            body["model_name"] = model_name
        if watermark_info is not None:
            body["watermark_info"] = watermark_info
        if keep_original_sound is not None:
            body["keep_original_sound"] = keep_original_sound
        if prompt is not None:
            body["prompt"] = prompt
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/kling/motion", json=body)

    async def lip_sync(
        self,
        *,
        mode: Literal["audio2video", "text2video"],
        video_id: str | None = None,
        video_url: str | None = None,
        audio_url: str | None = None,
        audio_type: Literal["url", "file"] | None = None,
        audio_file: str | None = None,
        text: str | None = None,
        voice_id: str | None = None,
        voice_language: Literal["zh", "en"] | None = None,
        voice_speed: float | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"mode": mode, **kwargs}
        if video_id is not None:
            body["video_id"] = video_id
        if video_url is not None:
            body["video_url"] = video_url
        if audio_url is not None:
            body["audio_url"] = audio_url
        if audio_type is not None:
            body["audio_type"] = audio_type
        if audio_file is not None:
            body["audio_file"] = audio_file
        if text is not None:
            body["text"] = text
        if voice_id is not None:
            body["voice_id"] = voice_id
        if voice_language is not None:
            body["voice_language"] = voice_language
        if voice_speed is not None:
            body["voice_speed"] = voice_speed
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/kling/lip-sync", json=body)

    async def talking_photo(
        self,
        *,
        image_url: str,
        audio_url: str,
        prompt: str | None = None,
        model: Literal[
            "kling-v1",
            "kling-v1-6",
            "kling-v2-master",
            "kling-v2-1-master",
            "kling-v2-5-turbo",
            "kling-v2-6",
        ]
        | None = None,
        duration: Literal[5, 10] | None = None,
        mode: Literal["std", "pro"] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image_url": image_url, "audio_url": audio_url, **kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if model is not None:
            body["model"] = model
        if duration is not None:
            body["duration"] = duration
        if mode is not None:
            body["mode"] = mode
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/kling/talking-photo", json=body)
