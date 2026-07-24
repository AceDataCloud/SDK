"""Captcha solving resources (``/captcha/*``)."""

from __future__ import annotations

from typing import Any

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle


class _CaptchaBase:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def _request(
        self,
        endpoint: str,
        body: dict[str, Any],
        *,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any] | TaskHandle:
        result = self._transport.request("POST", endpoint, json=body)
        task_id = result.get("task_id")
        has_solved_result = any(result.get(key) is not None for key in ("solution", "text", "token"))

        if not task_id or has_solved_result:
            return result

        handle = TaskHandle(task_id, "/captcha/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _AsyncCaptchaBase:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def _request(
        self,
        endpoint: str,
        body: dict[str, Any],
        *,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any] | AsyncTaskHandle:
        result = await self._transport.request("POST", endpoint, json=body)
        task_id = result.get("task_id")
        has_solved_result = any(result.get(key) is not None for key in ("solution", "text", "token"))

        if not task_id or has_solved_result:
            return result

        handle = AsyncTaskHandle(task_id, "/captcha/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _Recognition(_CaptchaBase):
    def hcaptcha(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {**kwargs}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        if async_ is not None:
            body["async"] = async_
        return self._request(
            "/captcha/recognition/hcaptcha",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    def image2text(
        self,
        *,
        image: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"image": image, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return self._request(
            "/captcha/recognition/image2text",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    def recaptcha2(
        self,
        *,
        image: str,
        question: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"image": image, "question": question, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return self._request(
            "/captcha/recognition/recaptcha2",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )


class _AsyncRecognition(_AsyncCaptchaBase):
    async def hcaptcha(
        self,
        *,
        queries: list[str] | None = None,
        question: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {**kwargs}
        if queries is not None:
            body["queries"] = queries
        if question is not None:
            body["question"] = question
        if async_ is not None:
            body["async"] = async_
        return await self._request(
            "/captcha/recognition/hcaptcha",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    async def image2text(
        self,
        *,
        image: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"image": image, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return await self._request(
            "/captcha/recognition/image2text",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    async def recaptcha2(
        self,
        *,
        image: str,
        question: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"image": image, "question": question, **kwargs}
        if async_ is not None:
            body["async"] = async_
        return await self._request(
            "/captcha/recognition/recaptcha2",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )


class _Token(_CaptchaBase):
    def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return self._request("/captcha/token/hcaptcha", body, wait=wait, poll_interval=poll_interval, max_wait=max_wait)

    def recaptcha2(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return self._request(
            "/captcha/token/recaptcha2",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    def recaptcha3(
        self,
        *,
        page_action: str,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {
            "page_action": page_action,
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        return self._request(
            "/captcha/token/recaptcha3",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )


class _AsyncToken(_AsyncCaptchaBase):
    async def hcaptcha(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return await self._request(
            "/captcha/token/hcaptcha",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    async def recaptcha2(
        self,
        *,
        website_key: str,
        website_url: str,
        proxy: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if proxy is not None:
            body["proxy"] = proxy
        if async_ is not None:
            body["async"] = async_
        return await self._request(
            "/captcha/token/recaptcha2",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )

    async def recaptcha3(
        self,
        *,
        page_action: str,
        website_key: str,
        website_url: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {
            "page_action": page_action,
            "website_key": website_key,
            "website_url": website_url,
            **kwargs,
        }
        if async_ is not None:
            body["async"] = async_
        return await self._request(
            "/captcha/token/recaptcha3",
            body,
            wait=wait,
            poll_interval=poll_interval,
            max_wait=max_wait,
        )


class Captcha:
    """Synchronous captcha solving client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = _Recognition(transport)
        self.token = _Token(transport)


class AsyncCaptcha:
    """Async captcha solving client."""

    def __init__(self, transport: Any) -> None:
        self.recognition = _AsyncRecognition(transport)
        self.token = _AsyncToken(transport)
