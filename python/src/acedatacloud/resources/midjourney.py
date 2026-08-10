"""Midjourney resources (``/midjourney/*``)."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle


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
    """Synchronous Midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def _submit(
        self,
        path: str,
        body: dict[str, Any],
        *,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> TaskHandle:
        result = self._transport.request("POST", path, json=body)
        handle = TaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def imagine(
        self,
        *,
        prompt: str | None = None,
        mode: Literal["fast", "relax", "turbo"] | None = None,
        action: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> TaskHandle:
        body = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if mode is not None:
            body["mode"] = mode
        if action is not None:
            body["action"] = action
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        return self._submit(
            "/midjourney/imagine",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    def edits(
        self,
        *,
        prompt: str | None = None,
        image_url: str | None = None,
        mode: Literal["fast", "relax", "turbo"] | None = None,
        action: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> TaskHandle:
        body = {**kwargs}
        if prompt is not None:
            body["prompt"] = prompt
        if image_url is not None:
            body["image_url"] = image_url
        if mode is not None:
            body["mode"] = mode
        if action is not None:
            body["action"] = action
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        return self._submit(
            "/midjourney/edits",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    def videos(
        self,
        *,
        action: Literal["generate", "extend"] | None = None,
        mode: Literal["fast", "turbo"] | None = None,
        resolution: Literal["480p", "720p"] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> TaskHandle:
        body = {**kwargs}
        if action is not None:
            body["action"] = action
        if mode is not None:
            body["mode"] = mode
        if resolution is not None:
            body["resolution"] = resolution
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        return self._submit(
            "/midjourney/videos",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    def seed(self, *, image_id: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/midjourney/seed", json={"image_id": image_id, **kwargs})

    def describe(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/midjourney/describe", json={"image_url": image_url, **kwargs})

    def shorten(self, *, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/midjourney/shorten", json={"prompt": prompt, **kwargs})

    def translate(self, *, content: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/midjourney/translate", json={"content": content, **kwargs})

    def tasks(self, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/midjourney/tasks", json=kwargs)


class AsyncMidjourney:
    """Async Midjourney client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def _submit(
        self,
        path: str,
        body: dict[str, Any],
        *,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> AsyncTaskHandle:
        result = await self._transport.request("POST", path, json=body)
        handle = AsyncTaskHandle(_task_id(result), "/midjourney/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def imagine(self, **kwargs: Any) -> AsyncTaskHandle:
        body = dict(kwargs)
        wait = bool(body.pop("wait", False))
        poll_interval = float(body.pop("poll_interval", 3.0))
        max_wait = float(body.pop("max_wait", 600.0))
        async_value = body.pop("async_", None)
        body["async"] = True if async_value is None else async_value
        return await self._submit(
            "/midjourney/imagine", body, wait=wait, poll_interval=poll_interval, max_wait=max_wait
        )

    async def edits(self, **kwargs: Any) -> AsyncTaskHandle:
        body = dict(kwargs)
        wait = bool(body.pop("wait", False))
        poll_interval = float(body.pop("poll_interval", 3.0))
        max_wait = float(body.pop("max_wait", 600.0))
        async_value = body.pop("async_", None)
        body["async"] = True if async_value is None else async_value
        return await self._submit("/midjourney/edits", body, wait=wait, poll_interval=poll_interval, max_wait=max_wait)

    async def videos(self, **kwargs: Any) -> AsyncTaskHandle:
        body = dict(kwargs)
        wait = bool(body.pop("wait", False))
        poll_interval = float(body.pop("poll_interval", 3.0))
        max_wait = float(body.pop("max_wait", 600.0))
        async_value = body.pop("async_", None)
        body["async"] = True if async_value is None else async_value
        return await self._submit(
            "/midjourney/videos", body, wait=wait, poll_interval=poll_interval, max_wait=max_wait
        )

    async def seed(self, *, image_id: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/midjourney/seed", json={"image_id": image_id, **kwargs})

    async def describe(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/midjourney/describe", json={"image_url": image_url, **kwargs})

    async def shorten(self, *, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/midjourney/shorten", json={"prompt": prompt, **kwargs})

    async def translate(self, *, content: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/midjourney/translate", json={"content": content, **kwargs})

    async def tasks(self, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/midjourney/tasks", json=kwargs)
