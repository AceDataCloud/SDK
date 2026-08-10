"""QRArt resources (``/qrart/*``)."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle
from acedatacloud.resources.midjourney import _task_id


class Qrart:
    """Synchronous QRArt client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        type: Literal["link", "text", "email", "phone", "sms"],
        prompt: str,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> TaskHandle:
        body = {"type": type, "prompt": prompt, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/qrart/generate", json=body)
        handle = TaskHandle(_task_id(result), "/qrart/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def tasks(self, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/qrart/tasks", json=kwargs)


class AsyncQrart:
    """Async QRArt client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        type: Literal["link", "text", "email", "phone", "sms"],
        prompt: str,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> AsyncTaskHandle:
        body = {"type": type, "prompt": prompt, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/qrart/generate", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/qrart/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def tasks(self, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/qrart/tasks", json=kwargs)
