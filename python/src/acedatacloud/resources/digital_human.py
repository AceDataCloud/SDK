"""Digital Human generation resources (``/digital-human/*``)."""

from __future__ import annotations

from typing import Any

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle


class DigitalHuman:
    """Synchronous digital human generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def videos(
        self,
        *,
        video_url: str | None = None,
        image_url: str | None = None,
        audio_url: str | None = None,
        text: str | None = None,
        voice_id: str | None = None,
        engine: str | None = None,
        guidance: float | None = None,
        steps: int | None = None,
        seam_fix: bool | None = None,
        speed: float | None = None,
        resolution: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {**kwargs}
        if video_url is not None:
            body["video_url"] = video_url
        if image_url is not None:
            body["image_url"] = image_url
        if audio_url is not None:
            body["audio_url"] = audio_url
        if text is not None:
            body["text"] = text
        if voice_id is not None:
            body["voice_id"] = voice_id
        if engine is not None:
            body["engine"] = engine
        if guidance is not None:
            body["guidance"] = guidance
        if steps is not None:
            body["steps"] = steps
        if seam_fix is not None:
            body["seam_fix"] = seam_fix
        if speed is not None:
            body["speed"] = speed
        if resolution is not None:
            body["resolution"] = resolution
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        result = self._transport.request("POST", "/digital-human/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("video_url") and not wait):
            return result

        handle = TaskHandle(task_id, "/digital-human/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def voices(
        self,
        *,
        audio_url: str,
        lang: str | None = None,
        name: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        if lang is not None:
            body["lang"] = lang
        if name is not None:
            body["name"] = name
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/digital-human/voices", json=body)


class AsyncDigitalHuman:
    """Async digital human generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def videos(
        self,
        *,
        video_url: str | None = None,
        image_url: str | None = None,
        audio_url: str | None = None,
        text: str | None = None,
        voice_id: str | None = None,
        engine: str | None = None,
        guidance: float | None = None,
        steps: int | None = None,
        seam_fix: bool | None = None,
        speed: float | None = None,
        resolution: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {**kwargs}
        if video_url is not None:
            body["video_url"] = video_url
        if image_url is not None:
            body["image_url"] = image_url
        if audio_url is not None:
            body["audio_url"] = audio_url
        if text is not None:
            body["text"] = text
        if voice_id is not None:
            body["voice_id"] = voice_id
        if engine is not None:
            body["engine"] = engine
        if guidance is not None:
            body["guidance"] = guidance
        if steps is not None:
            body["steps"] = steps
        if seam_fix is not None:
            body["seam_fix"] = seam_fix
        if speed is not None:
            body["speed"] = speed
        if resolution is not None:
            body["resolution"] = resolution
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        result = await self._transport.request("POST", "/digital-human/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("video_url") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, "/digital-human/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def voices(
        self,
        *,
        audio_url: str,
        lang: str | None = None,
        name: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        if lang is not None:
            body["lang"] = lang
        if name is not None:
            body["name"] = name
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/digital-human/voices", json=body)
