"""Captcha resources (``/captcha/*``)."""

from __future__ import annotations

from typing import Any

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle


def _task_id(result: Any) -> str:
    if not isinstance(result, dict):
        return ""
    return str(result.get("task_id") or result.get("id") or "")


class CaptchaRecognition:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def hcaptcha(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        async_: bool = False,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **extra: Any,
    ) -> dict[str, Any] | TaskHandle:
        body = _hcaptcha_recognition_body(queries=queries, question=question, async_=async_, extra=extra)
        result = self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)
        if not async_:
            return result
        handle = TaskHandle(
            _task_id(result),
            "/captcha/tasks",
            self._transport,
            submitted=result,
            poll_id_field="task_id",
            poll_action=None,
        )
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class CaptchaToken:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        rqdata: str | None = None,
        proxy: str | None = None,
        async_: bool = False,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **extra: Any,
    ) -> dict[str, Any] | TaskHandle:
        body = _hcaptcha_token_body(
            website_key=website_key,
            website_url=website_url,
            rqdata=rqdata,
            proxy=proxy,
            async_=async_,
            extra=extra,
        )
        result = self._transport.request("POST", "/captcha/token/hcaptcha", json=body)
        if not async_:
            return result
        handle = TaskHandle(
            _task_id(result),
            "/captcha/tasks",
            self._transport,
            submitted=result,
            poll_id_field="task_id",
            poll_action=None,
        )
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class Captcha:
    """Synchronous captcha client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = CaptchaRecognition(transport)
        self.token = CaptchaToken(transport)


class AsyncCaptchaRecognition:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def hcaptcha(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        async_: bool = False,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **extra: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body = _hcaptcha_recognition_body(queries=queries, question=question, async_=async_, extra=extra)
        result = await self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)
        if not async_:
            return result
        handle = AsyncTaskHandle(
            _task_id(result),
            "/captcha/tasks",
            self._transport,
            submitted=result,
            poll_id_field="task_id",
            poll_action=None,
        )
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncCaptchaToken:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        rqdata: str | None = None,
        proxy: str | None = None,
        async_: bool = False,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **extra: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body = _hcaptcha_token_body(
            website_key=website_key,
            website_url=website_url,
            rqdata=rqdata,
            proxy=proxy,
            async_=async_,
            extra=extra,
        )
        result = await self._transport.request("POST", "/captcha/token/hcaptcha", json=body)
        if not async_:
            return result
        handle = AsyncTaskHandle(
            _task_id(result),
            "/captcha/tasks",
            self._transport,
            submitted=result,
            poll_id_field="task_id",
            poll_action=None,
        )
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncCaptcha:
    """Async captcha client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = AsyncCaptchaRecognition(transport)
        self.token = AsyncCaptchaToken(transport)


def _hcaptcha_recognition_body(
    *,
    queries: list[str] | None,
    question: str | None,
    async_: bool,
    extra: dict[str, Any],
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if queries is not None:
        body["queries"] = queries
    if question is not None:
        body["question"] = question
    body.update(extra)
    body["async"] = async_
    return body


def _hcaptcha_token_body(
    *,
    website_key: str,
    website_url: str,
    rqdata: str | None,
    proxy: str | None,
    async_: bool,
    extra: dict[str, Any],
) -> dict[str, Any]:
    body: dict[str, Any] = {"website_key": website_key, "website_url": website_url}
    if rqdata is not None:
        body["rqdata"] = rqdata
    if proxy is not None:
        body["proxy"] = proxy
    body.update(extra)
    body["async"] = async_
    return body
