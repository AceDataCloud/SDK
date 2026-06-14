"""Short URL generation resources."""

from __future__ import annotations

from typing import Any


class ShortUrl:
    """Synchronous ShortUrl client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        content: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if content is not None:
            body["content"] = content
        return self._transport.request("POST", "/shorturl", json=body)


class AsyncShortUrl:
    """Async ShortUrl client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        content: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if content is not None:
            body["content"] = content
        return await self._transport.request("POST", "/shorturl", json=body)
