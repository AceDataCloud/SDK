"""Telegram Account Proxy resource."""

from __future__ import annotations

from typing import Any


class Telegram:
    """Synchronous Telegram Account Proxy client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create_qr(self) -> dict[str, Any]:
        return self._transport.request("POST", "/api/auth/qr")

    def auth_status(self) -> dict[str, Any]:
        return self._transport.request("GET", "/api/auth/status")

    def submit_password(self, *, password: str) -> dict[str, Any]:
        return self._transport.request("POST", "/api/auth/password", json={"password": password})

    def logout(self) -> dict[str, Any]:
        return self._transport.request("POST", "/api/auth/logout")

    def whoami(self) -> dict[str, Any]:
        return self._transport.request("GET", "/api/whoami")

    def chats(self, *, limit: int | None = None, unread_only: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if unread_only is not None:
            params["unread_only"] = unread_only
        return self._transport.request("GET", "/api/chats", params=params or None)

    def contacts(self) -> dict[str, Any]:
        return self._transport.request("GET", "/api/contacts")

    def messages(self, *, target: str, limit: int | None = None) -> dict[str, Any]:
        params = {"limit": limit} if limit is not None else None
        return self._transport.request("GET", f"/api/chats/{target}/messages", params=params)

    def search_messages(
        self, *, q: str, target: str | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"q": q}
        if target is not None:
            params["target"] = target
        if limit is not None:
            params["limit"] = limit
        return self._transport.request("GET", "/api/messages/search", params=params)

    def send_message(self, *, target: str, text: str, reply_to: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"target": target, "text": text}
        if reply_to is not None:
            body["reply_to"] = reply_to
        return self._transport.request("POST", "/api/messages", json=body)

    def delete_message(self, *, target: str, message_id: str) -> dict[str, Any]:
        return self._transport.request("DELETE", f"/api/chats/{target}/messages/{message_id}")

    def add_reaction(self, *, target: str, message_id: str, emoji: str) -> dict[str, Any]:
        return self._transport.request(
            "POST", f"/api/chats/{target}/messages/{message_id}/reactions", json={"emoji": emoji}
        )

    def mark_read(self, *, target: str) -> dict[str, Any]:
        return self._transport.request("POST", f"/api/chats/{target}/read")


class AsyncTelegram:
    """Asynchronous Telegram Account Proxy client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create_qr(self) -> dict[str, Any]:
        return await self._transport.request("POST", "/api/auth/qr")

    async def auth_status(self) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/auth/status")

    async def submit_password(self, *, password: str) -> dict[str, Any]:
        return await self._transport.request("POST", "/api/auth/password", json={"password": password})

    async def logout(self) -> dict[str, Any]:
        return await self._transport.request("POST", "/api/auth/logout")

    async def whoami(self) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/whoami")

    async def chats(self, *, limit: int | None = None, unread_only: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if unread_only is not None:
            params["unread_only"] = unread_only
        return await self._transport.request("GET", "/api/chats", params=params or None)

    async def contacts(self) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/contacts")

    async def messages(self, *, target: str, limit: int | None = None) -> dict[str, Any]:
        params = {"limit": limit} if limit is not None else None
        return await self._transport.request("GET", f"/api/chats/{target}/messages", params=params)

    async def search_messages(
        self, *, q: str, target: str | None = None, limit: int | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"q": q}
        if target is not None:
            params["target"] = target
        if limit is not None:
            params["limit"] = limit
        return await self._transport.request("GET", "/api/messages/search", params=params)

    async def send_message(self, *, target: str, text: str, reply_to: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"target": target, "text": text}
        if reply_to is not None:
            body["reply_to"] = reply_to
        return await self._transport.request("POST", "/api/messages", json=body)

    async def delete_message(self, *, target: str, message_id: str) -> dict[str, Any]:
        return await self._transport.request("DELETE", f"/api/chats/{target}/messages/{message_id}")

    async def add_reaction(self, *, target: str, message_id: str, emoji: str) -> dict[str, Any]:
        return await self._transport.request(
            "POST", f"/api/chats/{target}/messages/{message_id}/reactions", json={"emoji": emoji}
        )

    async def mark_read(self, *, target: str) -> dict[str, Any]:
        return await self._transport.request("POST", f"/api/chats/{target}/read")
