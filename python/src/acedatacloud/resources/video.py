"""Video generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

VideoProvider = Literal["sora", "luma", "veo", "kling", "hailuo", "seedance", "wan", "pika", "pixverse", "midjourney"]


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
        content: list[dict[str, Any]] | None = None,
        image_url: str | None = None,
        resolution: Literal["480p", "720p", "1080p"] | None = None,
        ratio: Literal["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"] | None = None,
        duration: int | float | None = None,
        frames: int | None = None,
        seed: int | None = None,
        camera_fixed: bool | None = None,
        watermark: bool | None = None,
        generate_audio: bool | None = None,
        callback_url: str | None = None,
        return_last_frame: bool | None = None,
        service_tier: Literal["default", "flex"] | None = None,
        execution_expires_after: int | None = None,
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
        if content is not None:
            body["content"] = content
        if image_url is not None:
            body["image_url"] = image_url
        if resolution is not None:
            body["resolution"] = resolution
        if ratio is not None:
            body["ratio"] = ratio
        if duration is not None:
            body["duration"] = duration
        if frames is not None:
            body["frames"] = frames
        if seed is not None:
            body["seed"] = seed
        if camera_fixed is not None:
            body["camerafixed"] = camera_fixed
        if watermark is not None:
            body["watermark"] = watermark
        if generate_audio is not None:
            body["generate_audio"] = generate_audio
        if callback_url is not None:
            body["callback_url"] = callback_url
        if return_last_frame is not None:
            body["return_last_frame"] = return_last_frame
        if service_tier is not None:
            body["service_tier"] = service_tier
        if execution_expires_after is not None:
            body["execution_expires_after"] = execution_expires_after

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
        content: list[dict[str, Any]] | None = None,
        image_url: str | None = None,
        resolution: Literal["480p", "720p", "1080p"] | None = None,
        ratio: Literal["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"] | None = None,
        duration: int | float | None = None,
        frames: int | None = None,
        seed: int | None = None,
        camera_fixed: bool | None = None,
        watermark: bool | None = None,
        generate_audio: bool | None = None,
        callback_url: str | None = None,
        return_last_frame: bool | None = None,
        service_tier: Literal["default", "flex"] | None = None,
        execution_expires_after: int | None = None,
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
        if content is not None:
            body["content"] = content
        if image_url is not None:
            body["image_url"] = image_url
        if resolution is not None:
            body["resolution"] = resolution
        if ratio is not None:
            body["ratio"] = ratio
        if duration is not None:
            body["duration"] = duration
        if frames is not None:
            body["frames"] = frames
        if seed is not None:
            body["seed"] = seed
        if camera_fixed is not None:
            body["camerafixed"] = camera_fixed
        if watermark is not None:
            body["watermark"] = watermark
        if generate_audio is not None:
            body["generate_audio"] = generate_audio
        if callback_url is not None:
            body["callback_url"] = callback_url
        if return_last_frame is not None:
            body["return_last_frame"] = return_last_frame
        if service_tier is not None:
            body["service_tier"] = service_tier
        if execution_expires_after is not None:
            body["execution_expires_after"] = execution_expires_after

        result = await self._transport.request("POST", f"/{provider}/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
