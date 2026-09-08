"""Tw (tw) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401


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


class Tw:
    """Synchronous tw client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def comments(
        self,
        *,
        note_id: str,
        cursor: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get all the comment information for a tweet by entering the id of the tweet."""
        body: dict[str, Any] = {}
        body["note_id"] = note_id
        if cursor is not None:
            body["cursor"] = cursor
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/x/comments", json=body)

    def search(
        self,
        *,
        keyword: str,
        cursor: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Find chronological tweets by keyword."""
        body: dict[str, Any] = {}
        body["keyword"] = keyword
        if cursor is not None:
            body["cursor"] = cursor
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/x/search", json=body)

    def posts(
        self,
        *,
        user_id: str,
        cursor: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get all the post information for a tweet by entering the user_id of the tweet."""
        body: dict[str, Any] = {}
        body["user_id"] = user_id
        if cursor is not None:
            body["cursor"] = cursor
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/x/posts", json=body)

    def users(
        self,
        *,
        username: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get user details by Twitter username."""
        body: dict[str, Any] = {}
        body["username"] = username
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/x/users", json=body)

    def retweets(
        self,
        *,
        note_id: str,
        cursor: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Find retweets of a tweet."""
        body: dict[str, Any] = {}
        body["note_id"] = note_id
        if cursor is not None:
            body["cursor"] = cursor
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/x/retweets", json=body)


class AsyncTw:
    """Asynchronous tw client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def comments(
        self,
        *,
        note_id: str,
        cursor: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get all the comment information for a tweet by entering the id of the tweet."""
        body: dict[str, Any] = {}
        body["note_id"] = note_id
        if cursor is not None:
            body["cursor"] = cursor
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/x/comments", json=body)

    async def search(
        self,
        *,
        keyword: str,
        cursor: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Find chronological tweets by keyword."""
        body: dict[str, Any] = {}
        body["keyword"] = keyword
        if cursor is not None:
            body["cursor"] = cursor
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/x/search", json=body)

    async def posts(
        self,
        *,
        user_id: str,
        cursor: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get all the post information for a tweet by entering the user_id of the tweet."""
        body: dict[str, Any] = {}
        body["user_id"] = user_id
        if cursor is not None:
            body["cursor"] = cursor
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/x/posts", json=body)

    async def users(
        self,
        *,
        username: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Get user details by Twitter username."""
        body: dict[str, Any] = {}
        body["username"] = username
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/x/users", json=body)

    async def retweets(
        self,
        *,
        note_id: str,
        cursor: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Find retweets of a tweet."""
        body: dict[str, Any] = {}
        body["note_id"] = note_id
        if cursor is not None:
            body["cursor"] = cursor
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/x/retweets", json=body)
