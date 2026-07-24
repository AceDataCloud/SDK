"""Turnstile captcha resource (``/captcha/token/turnstile``)."""

from __future__ import annotations

from typing import Any


class Turnstile:
    """Synchronous Turnstile captcha client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def token(
        self,
        *,
        website_key: str,
        website_url: str,
        action: str | None = None,
        cdata: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if action is not None:
            body["action"] = action
        if cdata is not None:
            body["cdata"] = cdata
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/captcha/token/turnstile", json=body)


class AsyncTurnstile:
    """Async Turnstile captcha client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def token(
        self,
        *,
        website_key: str,
        website_url: str,
        action: str | None = None,
        cdata: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"website_key": website_key, "website_url": website_url, **kwargs}
        if action is not None:
            body["action"] = action
        if cdata is not None:
            body["cdata"] = cdata
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/captcha/token/turnstile", json=body)
