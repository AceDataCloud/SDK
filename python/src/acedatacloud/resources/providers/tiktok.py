"""Tiktok (tiktok) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

TiktokRegion = Literal[
    "us",
    "jp",
    "kr",
    "vn",
    "br",
    "ru",
]


def _task_id(result: Any) -> str:
    """Task ids appear at the top level or nested under `data`."""
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


class Tiktok:
    """Synchronous tiktok client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def posts(
        self,
        *,
        cursor: str | None = None,
        user_id: str | None = None,
        unique_id: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get a TikTok user's work based on their unique id."""
        body: dict[str, Any] = {}
        if cursor is not None:
            body["cursor"] = cursor
        if user_id is not None:
            body["user_id"] = user_id
        if unique_id is not None:
            body["unique_id"] = unique_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/tiktok/posts", json=body)

    def search(
        self,
        *,
        type: Literal["user", "video"],
        keywords: str,
        cursor: int | None = None,
        region: TiktokRegion | None = None,
        sort_type: int | None = None,
        publish_time: int | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Search TikTok users and video resources by keyword."""
        body: dict[str, Any] = {}
        body["type"] = type
        body["keywords"] = keywords
        if cursor is not None:
            body["cursor"] = cursor
        if region is not None:
            body["region"] = region
        if sort_type is not None:
            body["sort_type"] = sort_type
        if publish_time is not None:
            body["publish_time"] = publish_time
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/tiktok/search", json=body)

    def user(
        self,
        *,
        cursor: str | None = None,
        user_id: str | None = None,
        unique_id: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get user details based on a TikTok user's unique id."""
        body: dict[str, Any] = {}
        if cursor is not None:
            body["cursor"] = cursor
        if user_id is not None:
            body["user_id"] = user_id
        if unique_id is not None:
            body["unique_id"] = unique_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/tiktok/user", json=body)

    def video(
        self,
        *,
        video_url: str,
        original_quality: int | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Follow the link to the video on TikTok for more details."""
        body: dict[str, Any] = {}
        body["video_url"] = video_url
        if original_quality is not None:
            body["original_quality"] = original_quality
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/tiktok/video", json=body)


class AsyncTiktok:
    """Asynchronous tiktok client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def posts(
        self,
        *,
        cursor: str | None = None,
        user_id: str | None = None,
        unique_id: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get a TikTok user's work based on their unique id."""
        body: dict[str, Any] = {}
        if cursor is not None:
            body["cursor"] = cursor
        if user_id is not None:
            body["user_id"] = user_id
        if unique_id is not None:
            body["unique_id"] = unique_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/tiktok/posts", json=body)

    async def search(
        self,
        *,
        type: Literal["user", "video"],
        keywords: str,
        cursor: int | None = None,
        region: TiktokRegion | None = None,
        sort_type: int | None = None,
        publish_time: int | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Search TikTok users and video resources by keyword."""
        body: dict[str, Any] = {}
        body["type"] = type
        body["keywords"] = keywords
        if cursor is not None:
            body["cursor"] = cursor
        if region is not None:
            body["region"] = region
        if sort_type is not None:
            body["sort_type"] = sort_type
        if publish_time is not None:
            body["publish_time"] = publish_time
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/tiktok/search", json=body)

    async def user(
        self,
        *,
        cursor: str | None = None,
        user_id: str | None = None,
        unique_id: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get user details based on a TikTok user's unique id."""
        body: dict[str, Any] = {}
        if cursor is not None:
            body["cursor"] = cursor
        if user_id is not None:
            body["user_id"] = user_id
        if unique_id is not None:
            body["unique_id"] = unique_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/tiktok/user", json=body)

    async def video(
        self,
        *,
        video_url: str,
        original_quality: int | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Follow the link to the video on TikTok for more details."""
        body: dict[str, Any] = {}
        body["video_url"] = video_url
        if original_quality is not None:
            body["original_quality"] = original_quality
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/tiktok/video", json=body)
