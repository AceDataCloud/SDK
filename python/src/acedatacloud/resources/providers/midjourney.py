"""Midjourney (midjourney) — synced from the platform OpenAPI spec."""

from __future__ import annotations

from typing import Any, Literal

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MidjourneyMode = Literal["fast", "relax", "turbo"]
MidjourneyVideoAction = Literal["generate", "extend"]
MidjourneyVideoMode = Literal["fast", "turbo"]
MidjourneyVideoResolution = Literal["480p", "720p"]


def _task_id(result: Any) -> str:
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
        mode: MidjourneyMode | None = None,
        action: str | None = None,
        prompt: str | None = None,
        timeout: float | None = None,
        image_id: str | None = None,
        translation: bool | None = None,
        split_images: bool | None = None,
        version: str | None = None,
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
        body: dict[str, Any] = {}
        optional_fields = {
            "mask": mask,
            "mode": mode,
            "action": action,
            "prompt": prompt,
            "timeout": timeout,
            "image_id": image_id,
            "translation": translation,
            "split_images": split_images,
            "version": version,
            "hd": hd,
            "quality": quality,
            "style_reference": style_reference,
            "moodboard": moodboard,
        }
        body.update({key: value for key, value in optional_fields.items() if value is not None})
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/midjourney/imagine", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def seed(self, *, image_id: str, callback_url: str | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"image_id": image_id}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/seed", json=body)

    def edits(
        self,
        *,
        mask: str | None = None,
        mode: MidjourneyMode | None = None,
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
        body: dict[str, Any] = {}
        optional_fields = {
            "mask": mask,
            "mode": mode,
            "action": action,
            "prompt": prompt,
            "image_url": image_url,
            "split_images": split_images,
        }
        body.update({key: value for key, value in optional_fields.items() if value is not None})
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/midjourney/edits", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def videos(
        self,
        *,
        action: MidjourneyVideoAction | None = None,
        mode: MidjourneyVideoMode | None = None,
        resolution: MidjourneyVideoResolution | None = None,
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
        body: dict[str, Any] = {}
        optional_fields = {
            "action": action,
            "mode": mode,
            "resolution": resolution,
            "prompt": prompt,
            "video_id": video_id,
            "video_index": video_index,
            "loop": loop,
            "image_url": image_url,
            "end_image_url": end_image_url,
        }
        body.update({key: value for key, value in optional_fields.items() if value is not None})
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/midjourney/videos", json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def describe(self, *, image_url: str, callback_url: str | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"image_url": image_url}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/describe", json=body)

    def shorten(self, *, prompt: str, callback_url: str | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/shorten", json=body)

    def translate(self, *, content: str, callback_url: str | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"content": content}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/midjourney/translate", json=body)


class AsyncMidjourney:
    """Asynchronous midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def imagine(
        self,
        *,
        mask: str | None = None,
        mode: MidjourneyMode | None = None,
        action: str | None = None,
        prompt: str | None = None,
        timeout: float | None = None,
        image_id: str | None = None,
        translation: bool | None = None,
        split_images: bool | None = None,
        version: str | None = None,
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
        body: dict[str, Any] = {}
        optional_fields = {
            "mask": mask,
            "mode": mode,
            "action": action,
            "prompt": prompt,
            "timeout": timeout,
            "image_id": image_id,
            "translation": translation,
            "split_images": split_images,
            "version": version,
            "hd": hd,
            "quality": quality,
            "style_reference": style_reference,
            "moodboard": moodboard,
        }
        body.update({key: value for key, value in optional_fields.items() if value is not None})
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/midjourney/imagine", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def seed(self, *, image_id: str, callback_url: str | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"image_id": image_id}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/seed", json=body)

    async def edits(
        self,
        *,
        mask: str | None = None,
        mode: MidjourneyMode | None = None,
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
        body: dict[str, Any] = {}
        optional_fields = {
            "mask": mask,
            "mode": mode,
            "action": action,
            "prompt": prompt,
            "image_url": image_url,
            "split_images": split_images,
        }
        body.update({key: value for key, value in optional_fields.items() if value is not None})
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/midjourney/edits", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def videos(
        self,
        *,
        action: MidjourneyVideoAction | None = None,
        mode: MidjourneyVideoMode | None = None,
        resolution: MidjourneyVideoResolution | None = None,
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
        body: dict[str, Any] = {}
        optional_fields = {
            "action": action,
            "mode": mode,
            "resolution": resolution,
            "prompt": prompt,
            "video_id": video_id,
            "video_index": video_index,
            "loop": loop,
            "image_url": image_url,
            "end_image_url": end_image_url,
        }
        body.update({key: value for key, value in optional_fields.items() if value is not None})
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/midjourney/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def describe(self, *, image_url: str, callback_url: str | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"image_url": image_url}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/describe", json=body)

    async def shorten(self, *, prompt: str, callback_url: str | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/shorten", json=body)

    async def translate(self, *, content: str, callback_url: str | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"content": content}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/midjourney/translate", json=body)
