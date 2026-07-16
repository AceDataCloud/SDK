"""Kling-specific video generation resources."""

from __future__ import annotations

from typing import Any, Literal, TypedDict
from urllib.parse import urlparse

KLING_MODELS = (
    "kling-v1",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
    "kling-v3",
    "kling-v3-omni",
    "kling-o1",
)
KlingModel = Literal[
    "kling-v1",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
    "kling-v3",
    "kling-v3-omni",
    "kling-o1",
]
KlingAction = Literal["text2video", "image2video", "extend"]
KlingMode = Literal["std", "pro", "4k"]


class KlingCameraConfig(TypedDict, total=False):
    horizontal: float
    vertical: float
    pan: float
    tilt: float
    roll: float
    zoom: float


class KlingCameraControl(TypedDict, total=False):
    type: Literal["simple", "down_back", "forward_up", "left_turn_forward", "right_turn_forward"]
    config: KlingCameraConfig


class KlingReferenceImage(TypedDict, total=False):
    image_url: str
    type: Literal["first_frame", "end_frame"]


class KlingReferenceVideo(TypedDict, total=False):
    video_url: str
    refer_type: Literal["base", "feature"]
    keep_original_sound: Literal["yes", "no"]


def _is_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _build_generate_body(
    *,
    action: KlingAction,
    model: KlingModel,
    mode: KlingMode | None,
    prompt: str | None,
    duration: int | None,
    generate_audio: bool | None,
    video_id: str | None,
    cfg_scale: float | None,
    aspect_ratio: Literal["16:9", "9:16", "1:1"] | None,
    callback_url: str | None,
    async_: bool | None,
    timeout: int | None,
    end_image_url: str | None,
    camera_control: KlingCameraControl | None,
    image_list: list[KlingReferenceImage] | None,
    video_list: list[KlingReferenceVideo] | None,
    negative_prompt: str | None,
    start_image_url: str | None,
) -> dict[str, Any]:
    if model not in KLING_MODELS:
        raise ValueError(f"model must be one of: {', '.join(KLING_MODELS)}")
    if action not in {"text2video", "image2video", "extend"}:
        raise ValueError("action must be text2video, image2video, or extend")
    if image_list is not None and not image_list:
        raise ValueError("image_list must be non-empty or omitted")
    if video_list is not None and not video_list:
        raise ValueError("video_list must be non-empty or omitted")

    is_v3 = model in {"kling-v3", "kling-v3-omni"}
    has_references = bool(image_list or video_list)
    if action in {"text2video", "image2video"} and not prompt:
        raise ValueError("prompt is required for text2video and image2video")
    if action == "image2video" and not start_image_url:
        raise ValueError("start_image_url is required for image2video")
    if action == "extend" and not video_id:
        raise ValueError("video_id is required for extend")
    if action == "extend" and model not in {"kling-v1", "kling-v1-6", "kling-v2-5-turbo"}:
        raise ValueError("extend requires kling-v1, kling-v1-6, or kling-v2-5-turbo")
    if action == "extend" and has_references:
        raise ValueError("image_list and video_list are not supported with extend")
    if end_image_url and not start_image_url:
        raise ValueError("start_image_url is required with end_image_url")
    if start_image_url and not _is_http_url(start_image_url):
        raise ValueError("start_image_url must be an HTTP URL")
    if end_image_url and not _is_http_url(end_image_url):
        raise ValueError("end_image_url must be an HTTP URL")
    if callback_url and not _is_http_url(callback_url):
        raise ValueError("callback_url must be an HTTP URL")
    if cfg_scale is not None and (isinstance(cfg_scale, bool) or not 0 <= cfg_scale <= 1):
        raise ValueError("cfg_scale must be between 0 and 1")
    if duration is not None and (isinstance(duration, bool) or not isinstance(duration, int)):
        raise ValueError("duration must be an integer")
    if is_v3 and duration is not None and not 3 <= duration <= 15:
        raise ValueError("Kling V3 duration must be between 3 and 15 seconds")
    if not is_v3 and model != "kling-o1" and duration is not None and duration not in {5, 10}:
        raise ValueError("This Kling model supports only 5- or 10-second generation")
    if model == "kling-o1" and duration is not None and duration != 5:
        raise ValueError("kling-o1 supports only 5-second generation")
    if model == "kling-o1" and mode is not None and mode not in {"std", "pro"}:
        raise ValueError("kling-o1 supports only std and pro modes")
    if mode == "4k" and not is_v3:
        raise ValueError("4k mode requires kling-v3 or kling-v3-omni")
    if has_references and model not in {"kling-o1", "kling-v3-omni"}:
        raise ValueError("Omni references require kling-o1 or kling-v3-omni")
    if has_references and mode == "4k":
        raise ValueError("4k cannot be combined with Omni references")
    if (model == "kling-o1" or has_references) and any(
        value is not None for value in (negative_prompt, camera_control, cfg_scale)
    ):
        raise ValueError("Kling O1 and Omni references do not support negative_prompt, camera_control, or cfg_scale")
    if model == "kling-o1" and generate_audio:
        raise ValueError("kling-o1 does not support generate_audio")
    if generate_audio and not is_v3 and model != "kling-v2-6":
        raise ValueError("generate_audio requires a V3 model or kling-v2-6 pro mode")
    if generate_audio and model == "kling-v2-6" and mode != "pro":
        raise ValueError("kling-v2-6 supports generate_audio only in pro mode")
    if generate_audio and video_list:
        raise ValueError("generate_audio cannot be used with video_list")
    if video_list is not None and len(video_list) != 1:
        raise ValueError("video_list must contain exactly one reference video")

    for image in image_list or []:
        if not isinstance(image, dict) or not _is_http_url(image.get("image_url")):
            raise ValueError("Every reference image requires an HTTP image_url")
        if image.get("type") is not None and image["type"] not in {"first_frame", "end_frame"}:
            raise ValueError("Reference image type must be first_frame or end_frame")
    for video in video_list or []:
        if not isinstance(video, dict) or not _is_http_url(video.get("video_url")):
            raise ValueError("Every reference video requires an HTTP video_url")
        if video.get("refer_type") is not None and video["refer_type"] not in {"base", "feature"}:
            raise ValueError("Reference video refer_type must be base or feature")
        if video.get("keep_original_sound") is not None and video["keep_original_sound"] not in {"yes", "no"}:
            raise ValueError("Reference video keep_original_sound must be yes or no")

    first_frames = int(bool(start_image_url)) + sum(image.get("type") == "first_frame" for image in image_list or [])
    end_frames = int(bool(end_image_url)) + sum(image.get("type") == "end_frame" for image in image_list or [])
    if first_frames > 1 or end_frames > 1:
        raise ValueError("Only one first frame and one end frame are allowed")
    if end_frames and not first_frames:
        raise ValueError("A first frame is required with an end frame")
    if video_list and (video_list[0].get("refer_type") or "base") == "base" and (first_frames or end_frames):
        raise ValueError("A base reference video cannot be combined with first or end frames")
    image_count = len(image_list or []) + int(bool(start_image_url)) + int(bool(end_image_url))
    image_limit = 4 if video_list else 7
    if image_count > image_limit:
        raise ValueError(f"Reference images cannot exceed {image_limit} for this request")

    body: dict[str, Any] = {"action": action, "model": model}
    optional_fields = {
        "mode": mode,
        "prompt": prompt,
        "duration": duration,
        "generate_audio": generate_audio,
        "video_id": video_id,
        "cfg_scale": cfg_scale,
        "aspect_ratio": aspect_ratio,
        "callback_url": callback_url,
        "async": async_,
        "timeout": timeout,
        "end_image_url": end_image_url,
        "camera_control": camera_control,
        "negative_prompt": negative_prompt,
        "start_image_url": start_image_url,
    }
    body.update({key: value for key, value in optional_fields.items() if value is not None})
    if image_list is not None:
        body["image_list"] = [
            {"image_url": image["image_url"], **({"type": image["type"]} if image.get("type") else {})}
            for image in image_list
        ]
    if video_list is not None:
        body["video_list"] = [
            {
                "video_url": video["video_url"],
                **({"refer_type": video["refer_type"]} if video.get("refer_type") else {}),
                **({"keep_original_sound": video["keep_original_sound"]} if video.get("keep_original_sound") else {}),
            }
            for video in video_list
        ]
    return body


def _build_motion_body(
    *,
    mode: Literal["std", "pro"],
    image_url: str,
    video_url: str,
    character_orientation: Literal["image", "video"],
    keep_original_sound: Literal["yes", "no"] | None,
    prompt: str | None,
    callback_url: str | None,
    async_: bool | None,
) -> dict[str, Any]:
    if mode not in {"std", "pro"}:
        raise ValueError("mode must be std or pro")
    if not _is_http_url(image_url):
        raise ValueError("image_url must be an HTTP URL")
    if not _is_http_url(video_url):
        raise ValueError("video_url must be an HTTP URL")
    if character_orientation not in {"image", "video"}:
        raise ValueError("character_orientation must be image or video")
    if keep_original_sound is not None and keep_original_sound not in {"yes", "no"}:
        raise ValueError("keep_original_sound must be yes or no")
    if callback_url and not _is_http_url(callback_url):
        raise ValueError("callback_url must be an HTTP URL")

    body: dict[str, Any] = {
        "mode": mode,
        "image_url": image_url,
        "video_url": video_url,
        "character_orientation": character_orientation,
    }
    optional_fields = {
        "keep_original_sound": keep_original_sound,
        "prompt": prompt,
        "callback_url": callback_url,
        "async": async_,
    }
    body.update({key: value for key, value in optional_fields.items() if value is not None})
    return body


class Kling:
    """Synchronous Kling video client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: KlingAction,
        model: KlingModel,
        mode: KlingMode | None = None,
        prompt: str | None = None,
        duration: int | None = None,
        generate_audio: bool | None = None,
        video_id: str | None = None,
        cfg_scale: float | None = None,
        aspect_ratio: Literal["16:9", "9:16", "1:1"] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        timeout: int | None = None,
        end_image_url: str | None = None,
        camera_control: KlingCameraControl | None = None,
        image_list: list[KlingReferenceImage] | None = None,
        video_list: list[KlingReferenceVideo] | None = None,
        negative_prompt: str | None = None,
        start_image_url: str | None = None,
    ) -> dict[str, Any]:
        body = _build_generate_body(
            action=action,
            model=model,
            mode=mode,
            prompt=prompt,
            duration=duration,
            generate_audio=generate_audio,
            video_id=video_id,
            cfg_scale=cfg_scale,
            aspect_ratio=aspect_ratio,
            callback_url=callback_url,
            async_=async_,
            timeout=timeout,
            end_image_url=end_image_url,
            camera_control=camera_control,
            image_list=image_list,
            video_list=video_list,
            negative_prompt=negative_prompt,
            start_image_url=start_image_url,
        )
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
        async_: bool | None = None,
    ) -> dict[str, Any]:
        body = _build_motion_body(
            mode=mode,
            image_url=image_url,
            video_url=video_url,
            character_orientation=character_orientation,
            keep_original_sound=keep_original_sound,
            prompt=prompt,
            callback_url=callback_url,
            async_=async_,
        )
        return self._transport.request("POST", "/kling/motion", json=body)


class AsyncKling:
    """Async Kling video client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: KlingAction,
        model: KlingModel,
        mode: KlingMode | None = None,
        prompt: str | None = None,
        duration: int | None = None,
        generate_audio: bool | None = None,
        video_id: str | None = None,
        cfg_scale: float | None = None,
        aspect_ratio: Literal["16:9", "9:16", "1:1"] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        timeout: int | None = None,
        end_image_url: str | None = None,
        camera_control: KlingCameraControl | None = None,
        image_list: list[KlingReferenceImage] | None = None,
        video_list: list[KlingReferenceVideo] | None = None,
        negative_prompt: str | None = None,
        start_image_url: str | None = None,
    ) -> dict[str, Any]:
        body = _build_generate_body(
            action=action,
            model=model,
            mode=mode,
            prompt=prompt,
            duration=duration,
            generate_audio=generate_audio,
            video_id=video_id,
            cfg_scale=cfg_scale,
            aspect_ratio=aspect_ratio,
            callback_url=callback_url,
            async_=async_,
            timeout=timeout,
            end_image_url=end_image_url,
            camera_control=camera_control,
            image_list=image_list,
            video_list=video_list,
            negative_prompt=negative_prompt,
            start_image_url=start_image_url,
        )
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
        async_: bool | None = None,
    ) -> dict[str, Any]:
        body = _build_motion_body(
            mode=mode,
            image_url=image_url,
            video_url=video_url,
            character_orientation=character_orientation,
            keep_original_sound=keep_original_sound,
            prompt=prompt,
            callback_url=callback_url,
            async_=async_,
        )
        return await self._transport.request("POST", "/kling/motion", json=body)
