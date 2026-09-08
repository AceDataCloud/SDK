"""Short URL resource (``/shorturl``)."""

from __future__ import annotations

from typing import Any


class ShortUrl:
    """Synchronous short URL client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        content: str | None = None,
        url: str | None = None,
        slug: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if content is None:
            if url is None:
                msg = "Either `content` or legacy `url` must be provided."
                raise ValueError(msg)
            content = url
        body: dict[str, Any] = {"content": content, **kwargs}
        if slug is not None:
            body["slug"] = slug
        return self._transport.request("POST", "/shorturl", json=body)


class AsyncShortUrl:
    """Async short URL client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        content: str | None = None,
        url: str | None = None,
        slug: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if content is None:
            if url is None:
                msg = "Either `content` or legacy `url` must be provided."
                raise ValueError(msg)
            content = url
        body: dict[str, Any] = {"content": content, **kwargs}
        if slug is not None:
            body["slug"] = slug
        return await self._transport.request("POST", "/shorturl", json=body)
