"""Discord Agent Proxy resource."""

from __future__ import annotations

from typing import Any


class Discord:
    """Synchronous Discord Agent Proxy client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def whoami(self) -> dict[str, Any]:
        return self._transport.request("GET", "/api/whoami")

    def guilds(self) -> dict[str, Any]:
        return self._transport.request("GET", "/api/guilds")

    def create_channel(self, *, guild_id: str, name: str) -> dict[str, Any]:
        return self._transport.request("POST", f"/api/guilds/{guild_id}/channels", json={"name": name})

    def members(self, *, guild_id: str, limit: int | None = None) -> dict[str, Any]:
        params = {"limit": limit} if limit is not None else None
        return self._transport.request("GET", f"/api/guilds/{guild_id}/members", params=params)

    def send_message(
        self, *, channel_id: str, content: str, reply_to: str | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"channel_id": channel_id, "content": content}
        if reply_to is not None:
            body["reply_to"] = reply_to
        return self._transport.request("POST", "/api/messages", json=body)

    def messages(self, *, channel_id: str, limit: int | None = None) -> dict[str, Any]:
        params = {"limit": limit} if limit is not None else None
        return self._transport.request("GET", f"/api/channels/{channel_id}/messages", params=params)

    def search_messages(
        self, *, channel_id: str, q: str, limit: int | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"q": q}
        if limit is not None:
            params["limit"] = limit
        return self._transport.request("GET", f"/api/channels/{channel_id}/messages/search", params=params)

    def delete_message(self, *, channel_id: str, message_id: str) -> dict[str, Any]:
        return self._transport.request("DELETE", f"/api/channels/{channel_id}/messages/{message_id}")

    def add_reaction(self, *, channel_id: str, message_id: str, emoji: str) -> dict[str, Any]:
        return self._transport.request(
            "POST", f"/api/channels/{channel_id}/messages/{message_id}/reactions", json={"emoji": emoji}
        )

    def pin_message(self, *, channel_id: str, message_id: str) -> dict[str, Any]:
        return self._transport.request("POST", f"/api/channels/{channel_id}/messages/{message_id}/pin")

    def create_dm(self, *, recipient_id: str) -> dict[str, Any]:
        return self._transport.request("POST", "/api/dms", json={"recipient_id": recipient_id})

    def send_dm(self, *, recipient_id: str, content: str) -> dict[str, Any]:
        return self._transport.request(
            "POST", "/api/dms/send", json={"recipient_id": recipient_id, "content": content}
        )


class AsyncDiscord:
    """Asynchronous Discord Agent Proxy client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def whoami(self) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/whoami")

    async def guilds(self) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/guilds")

    async def create_channel(self, *, guild_id: str, name: str) -> dict[str, Any]:
        return await self._transport.request("POST", f"/api/guilds/{guild_id}/channels", json={"name": name})

    async def members(self, *, guild_id: str, limit: int | None = None) -> dict[str, Any]:
        params = {"limit": limit} if limit is not None else None
        return await self._transport.request("GET", f"/api/guilds/{guild_id}/members", params=params)

    async def send_message(
        self, *, channel_id: str, content: str, reply_to: str | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"channel_id": channel_id, "content": content}
        if reply_to is not None:
            body["reply_to"] = reply_to
        return await self._transport.request("POST", "/api/messages", json=body)

    async def messages(self, *, channel_id: str, limit: int | None = None) -> dict[str, Any]:
        params = {"limit": limit} if limit is not None else None
        return await self._transport.request("GET", f"/api/channels/{channel_id}/messages", params=params)

    async def search_messages(
        self, *, channel_id: str, q: str, limit: int | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"q": q}
        if limit is not None:
            params["limit"] = limit
        return await self._transport.request("GET", f"/api/channels/{channel_id}/messages/search", params=params)

    async def delete_message(self, *, channel_id: str, message_id: str) -> dict[str, Any]:
        return await self._transport.request("DELETE", f"/api/channels/{channel_id}/messages/{message_id}")

    async def add_reaction(self, *, channel_id: str, message_id: str, emoji: str) -> dict[str, Any]:
        return await self._transport.request(
            "POST", f"/api/channels/{channel_id}/messages/{message_id}/reactions", json={"emoji": emoji}
        )

    async def pin_message(self, *, channel_id: str, message_id: str) -> dict[str, Any]:
        return await self._transport.request("POST", f"/api/channels/{channel_id}/messages/{message_id}/pin")

    async def create_dm(self, *, recipient_id: str) -> dict[str, Any]:
        return await self._transport.request("POST", "/api/dms", json={"recipient_id": recipient_id})

    async def send_dm(self, *, recipient_id: str, content: str) -> dict[str, Any]:
        return await self._transport.request(
            "POST", "/api/dms/send", json={"recipient_id": recipient_id, "content": content}
        )
