"""Short URL resource (``/shorturl``)."""

from __future__ import annotations

from typing import Any


class ShortUrl:
    """Synchronous short URL client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(self, *, url: str, slug: str | None = None, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"url": url, **kwargs}
        if slug is not None:
            body["slug"] = slug
        return self._transport.request("POST", "/shorturl", json=body)


class AsyncShortUrl:
    """Async short URL client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(self, *, url: str, slug: str | None = None, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"url": url, **kwargs}
        if slug is not None:
            body["slug"] = slug
        return await self._transport.request("POST", "/shorturl", json=body)
