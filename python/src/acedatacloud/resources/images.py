"""Image generation resources."""

from __future__ import annotations

from typing import Any

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle


class Images:
    """Synchronous image generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        model: str | None = None,
        negative_prompt: str | None = None,
        image_url: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if image_url is not None:
            body["image_url"] = image_url
        if callback_url is not None:
            body["callback_url"] = callback_url

        result = self._transport.request("POST", "/nano-banana/images", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = TaskHandle(task_id, "/nano-banana/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncImages:
    """Async image generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        model: str | None = None,
        negative_prompt: str | None = None,
        image_url: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if image_url is not None:
            body["image_url"] = image_url
        if callback_url is not None:
            body["callback_url"] = callback_url

        result = await self._transport.request("POST", "/nano-banana/images", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, "/nano-banana/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
