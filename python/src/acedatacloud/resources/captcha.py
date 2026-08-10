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
        rqdata: str | None = None,
        proxy: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if rqdata is not None:
            body["rqdata"] = rqdata
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
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/recaptcha2", json=body)

    def recaptcha3(
        self,
        *,
        website_key: str,
        website_url: str,
        page_action: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "website_key": website_key,
            "website_url": website_url,
            "page_action": page_action,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/recaptcha3", json=body)


class _Tasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def retrieve(self, *, task_id: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/captcha/tasks", json={"task_id": task_id, **kwargs})


class Captcha:
    """Synchronous captcha client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = _Recognition(transport)
        self.token = _Token(transport)
        self.tasks = _Tasks(transport)


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
        rqdata: str | None = None,
        proxy: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if rqdata is not None:
            body["rqdata"] = rqdata
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
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/recaptcha2", json=body)

    async def recaptcha3(
        self,
        *,
        website_key: str,
        website_url: str,
        page_action: str,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "website_key": website_key,
            "website_url": website_url,
            "page_action": page_action,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/recaptcha3", json=body)


class _AsyncTasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def retrieve(self, *, task_id: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/captcha/tasks", json={"task_id": task_id, **kwargs})


class AsyncCaptcha:
    """Async captcha client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = _AsyncRecognition(transport)
        self.token = _AsyncToken(transport)
        self.tasks = _AsyncTasks(transport)
