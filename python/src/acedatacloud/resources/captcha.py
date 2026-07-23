"""Captcha recognition and solving resources."""

from __future__ import annotations

from typing import Any

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle


class Captcha:
    """Synchronous captcha client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def recognize(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        return self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)

    def token(
        self,
        *,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/captcha/token/hcaptcha", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = TaskHandle(task_id, "/captcha/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncCaptcha:
    """Async captcha client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def recognize(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        return await self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)

    async def token(
        self,
        *,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/captcha/token/hcaptcha", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, "/captcha/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
