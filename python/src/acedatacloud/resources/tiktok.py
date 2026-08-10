"""TikTok data resources (``/tiktok/*``)."""

from __future__ import annotations

from typing import Any, Literal


class Tiktok:
    """Synchronous TikTok client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def posts(self, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/tiktok/posts", json=kwargs)

    def search(
        self,
        *,
        type: Literal["user", "video"],
        keywords: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return self._transport.request("POST", "/tiktok/search", json={"type": type, "keywords": keywords, **kwargs})

    def user(self, *, type: str, keywords: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/tiktok/user", json={"type": type, "keywords": keywords, **kwargs})

    def video(self, *, video_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/tiktok/video", json={"video_url": video_url, **kwargs})


class AsyncTiktok:
    """Async TikTok client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def posts(self, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/tiktok/posts", json=kwargs)

    async def search(self, *, type: Literal["user", "video"], keywords: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request(
            "POST", "/tiktok/search", json={"type": type, "keywords": keywords, **kwargs}
        )

    async def user(self, *, type: str, keywords: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request(
            "POST", "/tiktok/user", json={"type": type, "keywords": keywords, **kwargs}
        )

    async def video(self, *, video_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/tiktok/video", json={"video_url": video_url, **kwargs})
