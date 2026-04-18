"""Video generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

VideoProvider = Literal["sora", "luma", "veo", "kling", "hailuo", "seedance", "wan", "pika", "pixverse"]


class Video:
    """Synchronous video generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        provider: VideoProvider | str = "sora",
        model: str | None = None,
        image_url: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if image_url is not None:
            body["image_url"] = image_url
        if callback_url is not None:
            body["callback_url"] = callback_url

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
        prompt: str,
        provider: VideoProvider | str = "sora",
        model: str | None = None,
        image_url: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if image_url is not None:
            body["image_url"] = image_url
        if callback_url is not None:
            body["callback_url"] = callback_url

        result = await self._transport.request("POST", f"/{provider}/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
