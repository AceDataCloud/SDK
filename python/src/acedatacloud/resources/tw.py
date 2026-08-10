"""X/Twitter data resources (``/x/*``)."""

from __future__ import annotations

from typing import Any


class Tw:
    """Synchronous X/Twitter client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def posts(self, *, user_id: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/x/posts", json={"user_id": user_id, **kwargs})

    def users(self, *, username: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/x/users", json={"username": username, **kwargs})

    def retweets(self, *, keyword: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/x/retweets", json={"keyword": keyword, **kwargs})


class AsyncTw:
    """Async X/Twitter client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def posts(self, *, user_id: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/x/posts", json={"user_id": user_id, **kwargs})

    async def users(self, *, username: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/x/users", json={"username": username, **kwargs})

    async def retweets(self, *, keyword: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/x/retweets", json={"keyword": keyword, **kwargs})
