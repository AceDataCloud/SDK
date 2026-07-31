"""Captcha resources — hCaptcha, reCAPTCHA, Turnstile, and image2text."""

from __future__ import annotations

from typing import Any


class _Recognition:
    """Captcha recognition namespace."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def hcaptcha(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Solve an hCaptcha image challenge."""
        body: dict[str, Any] = {**kwargs}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)

    def recaptcha2(
        self,
        *,
        image: str,
        question: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Solve a reCAPTCHA v2 image challenge."""
        body: dict[str, Any] = {"image": image, "question": question, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/recognition/recaptcha2", json=body)

    def image2text(
        self,
        *,
        image: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Recognize text in a captcha image."""
        body: dict[str, Any] = {"image": image, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/recognition/image2text", json=body)


class _Token:
    """Captcha token namespace."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Obtain an hCaptcha bypass token."""
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/hcaptcha", json=body)

    def recaptcha2(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Obtain a reCAPTCHA v2 bypass token."""
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/recaptcha2", json=body)

    def recaptcha3(
        self,
        *,
        page_action: str,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Obtain a reCAPTCHA v3 bypass token."""
        body: dict[str, Any] = {
            "page_action": page_action,
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/recaptcha3", json=body)

    def turnstile(
        self,
        *,
        website_key: str,
        website_url: str,
        action: str | None = None,
        cdata: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Obtain a Cloudflare Turnstile bypass token."""
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if action is not None:
            body["action"] = action
        if cdata is not None:
            body["cdata"] = cdata
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/turnstile", json=body)


class _Tasks:
    """Captcha tasks namespace."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def retrieve(self, *, task_id: str, **kwargs: Any) -> dict[str, Any]:
        """Retrieve a captcha task by ID."""
        body: dict[str, Any] = {"task_id": task_id, **kwargs}
        return self._transport.request("POST", "/captcha/tasks", json=body)


class Captcha:
    """Synchronous captcha client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = _Recognition(transport)
        self.token = _Token(transport)
        self.tasks = _Tasks(transport)


class _AsyncRecognition:
    """Async captcha recognition namespace."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def hcaptcha(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Solve an hCaptcha image challenge."""
        body: dict[str, Any] = {**kwargs}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)

    async def recaptcha2(
        self,
        *,
        image: str,
        question: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Solve a reCAPTCHA v2 image challenge."""
        body: dict[str, Any] = {"image": image, "question": question, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/recognition/recaptcha2", json=body)

    async def image2text(
        self,
        *,
        image: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Recognize text in a captcha image."""
        body: dict[str, Any] = {"image": image, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/recognition/image2text", json=body)


class _AsyncToken:
    """Async captcha token namespace."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Obtain an hCaptcha bypass token."""
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/hcaptcha", json=body)

    async def recaptcha2(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Obtain a reCAPTCHA v2 bypass token."""
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/recaptcha2", json=body)

    async def recaptcha3(
        self,
        *,
        page_action: str,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Obtain a reCAPTCHA v3 bypass token."""
        body: dict[str, Any] = {
            "page_action": page_action,
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/recaptcha3", json=body)

    async def turnstile(
        self,
        *,
        website_key: str,
        website_url: str,
        action: str | None = None,
        cdata: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Obtain a Cloudflare Turnstile bypass token."""
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if action is not None:
            body["action"] = action
        if cdata is not None:
            body["cdata"] = cdata
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/turnstile", json=body)


class _AsyncTasks:
    """Async captcha tasks namespace."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def retrieve(self, *, task_id: str, **kwargs: Any) -> dict[str, Any]:
        """Retrieve a captcha task by ID."""
        body: dict[str, Any] = {"task_id": task_id, **kwargs}
        return await self._transport.request("POST", "/captcha/tasks", json=body)


class AsyncCaptcha:
    """Async captcha client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = _AsyncRecognition(transport)
        self.token = _AsyncToken(transport)
        self.tasks = _AsyncTasks(transport)
