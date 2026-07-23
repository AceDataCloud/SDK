"""Captcha resources (``/captcha/*``)."""

from __future__ import annotations

from typing import Any


class _Recognition:
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
        body: dict[str, Any] = {**kwargs}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)

    def image2text(
        self,
        *,
        image: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image": image, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/recognition/image2text", json=body)

    def recaptcha2(
        self,
        *,
        image: str,
        question: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image": image, "question": question, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/recognition/recaptcha2", json=body)


class _Token:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/hcaptcha", json=body)

    def recaptcha2(
        self,
        *,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
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
        body: dict[str, Any] = {
            "page_action": page_action,
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/recaptcha3", json=body)


class _AsyncRecognition:
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
        body: dict[str, Any] = {**kwargs}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/recognition/hcaptcha", json=body)

    async def image2text(
        self,
        *,
        image: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image": image, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/recognition/image2text", json=body)

    async def recaptcha2(
        self,
        *,
        image: str,
        question: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"image": image, "question": question, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/recognition/recaptcha2", json=body)


class _AsyncToken:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/hcaptcha", json=body)

    async def recaptcha2(
        self,
        *,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
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
        body: dict[str, Any] = {
            "page_action": page_action,
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/recaptcha3", json=body)


class Captcha:
    """Synchronous captcha client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = _Recognition(transport)
        self.token = _Token(transport)


class AsyncCaptcha:
    """Async captcha client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = _AsyncRecognition(transport)
        self.token = _AsyncToken(transport)
