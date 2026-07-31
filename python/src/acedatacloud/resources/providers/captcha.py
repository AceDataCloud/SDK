"""Captcha (captcha) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any  # noqa: F401


class _CaptchaRecognition:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def hcaptcha(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Solve an hCaptcha image recognition challenge."""
        body: dict[str, Any] = {}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        if async_ is not None:
            body["async"] = async_
        body.update(extra)
        return self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)


class _CaptchaToken:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Solve an hCaptcha token challenge."""
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        body.update(extra)
        return self._transport.request("POST", "/captcha/token/hcaptcha", json=body)


class Captcha:
    """Synchronous captcha client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.recognition = _CaptchaRecognition(transport)
        self.token = _CaptchaToken(transport)

    def tasks(self, *, task_id: str, **extra: Any) -> dict[str, Any]:
        """Retrieve a captcha task result."""
        body: dict[str, Any] = {"task_id": task_id}
        body.update(extra)
        return self._transport.request("POST", "/captcha/tasks", json=body)


class _AsyncCaptchaRecognition:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def hcaptcha(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Solve an hCaptcha image recognition challenge."""
        body: dict[str, Any] = {}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        if async_ is not None:
            body["async"] = async_
        body.update(extra)
        return await self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)


class _AsyncCaptchaToken:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Solve an hCaptcha token challenge."""
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        body.update(extra)
        return await self._transport.request("POST", "/captcha/token/hcaptcha", json=body)


class AsyncCaptcha:
    """Asynchronous captcha client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.recognition = _AsyncCaptchaRecognition(transport)
        self.token = _AsyncCaptchaToken(transport)

    async def tasks(self, *, task_id: str, **extra: Any) -> dict[str, Any]:
        """Retrieve a captcha task result."""
        body: dict[str, Any] = {"task_id": task_id}
        body.update(extra)
        return await self._transport.request("POST", "/captcha/tasks", json=body)
