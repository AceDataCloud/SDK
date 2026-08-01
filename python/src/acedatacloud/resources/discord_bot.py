"""Discord Agent Proxy client.

The Discord Agent Proxy is an independently deployed service.  Users
deploy it from the AceData Cloud console at
https://platform.acedata.cloud/console/applications and receive a
deployment-specific base URL and access token.

This module provides :class:`DiscordBotClient` (synchronous) and
:class:`AsyncDiscordBotClient` (async) for interacting with the REST
API exposed by that deployment.
"""

from __future__ import annotations

from typing import Any

import httpx


class _DiscordBotBase:
    def __init__(self, base_url: str, token: str, *, timeout: float = 300.0) -> None:
        self._base = base_url.rstrip("/")
        self._token = token
        self._timeout = timeout

    def _make_headers(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self._token,
        }

    @staticmethod
    def _unwrap(body: Any) -> Any:
        if isinstance(body, dict) and "data" in body:
            return body["data"]
        return body


class DiscordBotClient(_DiscordBotBase):
    """Synchronous client for a deployed Discord Agent Proxy.

    Args:
        base_url: The deployment URL shown in the AceData Cloud console,
            e.g. ``https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud``.
        token: The access token for this deployment.
        timeout: HTTP timeout in seconds (default 300).
    """

    def __init__(self, base_url: str, token: str, *, timeout: float = 300.0) -> None:
        super().__init__(base_url, token, timeout=timeout)
        self._client = httpx.Client(timeout=timeout)

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self._base}{path}"
        resp = self._client.request(method, url, headers=self._make_headers(), **kwargs)
        resp.raise_for_status()
        return self._unwrap(resp.json())

    # ── No-auth endpoint ──────────────────────────────────────────────

    def health(self) -> dict[str, Any]:
        """Check service health.  Does not require authentication."""
        url = f"{self._base}/health"
        resp = self._client.get(url)
        resp.raise_for_status()
        return resp.json()  # type: ignore[return-value]

    # ── Account ───────────────────────────────────────────────────────

    def whoami(self) -> dict[str, Any]:
        """Return information about the proxied Discord account."""
        return self._request("GET", "/api/whoami")  # type: ignore[return-value]

    # ── Guilds ────────────────────────────────────────────────────────

    def list_guilds(self) -> list[Any]:
        """List all guilds (servers) the account has joined."""
        return self._request("GET", "/api/guilds")  # type: ignore[return-value]

    def list_channels(self, guild_id: str) -> list[Any]:
        """List channels in a guild."""
        return self._request("GET", f"/api/guilds/{guild_id}/channels")  # type: ignore[return-value]

    def create_channel(self, guild_id: str, *, name: str) -> dict[str, Any]:
        """Create a text channel in a guild."""
        return self._request(  # type: ignore[return-value]
            "POST", f"/api/guilds/{guild_id}/channels", json={"name": name}
        )

    def list_members(self, guild_id: str, *, limit: int = 100) -> list[Any]:
        """List members of a guild (default 100)."""
        return self._request(  # type: ignore[return-value]
            "GET", f"/api/guilds/{guild_id}/members", params={"limit": limit}
        )

    # ── Messages ──────────────────────────────────────────────────────

    def send_message(
        self, *, channel_id: str, content: str, reply_to: str | None = None
    ) -> dict[str, Any]:
        """Send a message to a channel.

        Args:
            channel_id: Target channel ID.
            content: Message text.
            reply_to: Optional message ID to reply to.
        """
        body: dict[str, Any] = {"channel_id": channel_id, "content": content}
        if reply_to is not None:
            body["reply_to"] = reply_to
        return self._request("POST", "/api/messages", json=body)  # type: ignore[return-value]

    def list_messages(self, channel_id: str, *, limit: int = 50) -> list[Any]:
        """Read recent messages from a channel (default 50, max 100)."""
        return self._request(  # type: ignore[return-value]
            "GET", f"/api/channels/{channel_id}/messages", params={"limit": limit}
        )

    def search_messages(self, channel_id: str, *, q: str, limit: int = 25) -> list[Any]:
        """Search messages in a channel."""
        return self._request(  # type: ignore[return-value]
            "GET",
            f"/api/channels/{channel_id}/messages/search",
            params={"q": q, "limit": limit},
        )

    def edit_message(
        self, channel_id: str, message_id: str, *, content: str
    ) -> dict[str, Any]:
        """Edit a message you own."""
        return self._request(  # type: ignore[return-value]
            "PATCH",
            f"/api/channels/{channel_id}/messages/{message_id}",
            json={"content": content},
        )

    def delete_message(self, channel_id: str, message_id: str) -> dict[str, Any]:
        """Delete a message."""
        return self._request(  # type: ignore[return-value]
            "DELETE", f"/api/channels/{channel_id}/messages/{message_id}"
        )

    def add_reaction(
        self, channel_id: str, message_id: str, *, emoji: str
    ) -> dict[str, Any]:
        """Add an emoji reaction to a message."""
        return self._request(  # type: ignore[return-value]
            "POST",
            f"/api/channels/{channel_id}/messages/{message_id}/reactions",
            json={"emoji": emoji},
        )

    def pin_message(self, channel_id: str, message_id: str) -> dict[str, Any]:
        """Pin a message in a channel."""
        return self._request(  # type: ignore[return-value]
            "POST", f"/api/channels/{channel_id}/messages/{message_id}/pin"
        )

    # ── Direct messages ───────────────────────────────────────────────

    def create_dm(self, *, recipient_id: str) -> dict[str, Any]:
        """Open a DM channel with a user; returns the channel info."""
        return self._request(  # type: ignore[return-value]
            "POST", "/api/dms", json={"recipient_id": recipient_id}
        )

    def send_dm(self, *, recipient_id: str, content: str) -> dict[str, Any]:
        """Send a direct message to a user."""
        return self._request(  # type: ignore[return-value]
            "POST", "/api/dms/send", json={"recipient_id": recipient_id, "content": content}
        )

    # ── Lifecycle ─────────────────────────────────────────────────────

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> DiscordBotClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncDiscordBotClient(_DiscordBotBase):
    """Asynchronous client for a deployed Discord Agent Proxy.

    Args:
        base_url: The deployment URL shown in the AceData Cloud console,
            e.g. ``https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud``.
        token: The access token for this deployment.
        timeout: HTTP timeout in seconds (default 300).
    """

    def __init__(self, base_url: str, token: str, *, timeout: float = 300.0) -> None:
        super().__init__(base_url, token, timeout=timeout)
        self._client = httpx.AsyncClient(timeout=timeout)

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self._base}{path}"
        resp = await self._client.request(method, url, headers=self._make_headers(), **kwargs)
        resp.raise_for_status()
        return self._unwrap(resp.json())

    async def health(self) -> dict[str, Any]:
        """Check service health.  Does not require authentication."""
        url = f"{self._base}/health"
        resp = await self._client.get(url)
        resp.raise_for_status()
        return resp.json()  # type: ignore[return-value]

    async def whoami(self) -> dict[str, Any]:
        """Return information about the proxied Discord account."""
        return await self._request("GET", "/api/whoami")  # type: ignore[return-value]

    async def list_guilds(self) -> list[Any]:
        """List all guilds (servers) the account has joined."""
        return await self._request("GET", "/api/guilds")  # type: ignore[return-value]

    async def list_channels(self, guild_id: str) -> list[Any]:
        """List channels in a guild."""
        return await self._request(  # type: ignore[return-value]
            "GET", f"/api/guilds/{guild_id}/channels"
        )

    async def create_channel(self, guild_id: str, *, name: str) -> dict[str, Any]:
        """Create a text channel in a guild."""
        return await self._request(  # type: ignore[return-value]
            "POST", f"/api/guilds/{guild_id}/channels", json={"name": name}
        )

    async def list_members(self, guild_id: str, *, limit: int = 100) -> list[Any]:
        """List members of a guild (default 100)."""
        return await self._request(  # type: ignore[return-value]
            "GET", f"/api/guilds/{guild_id}/members", params={"limit": limit}
        )

    async def send_message(
        self, *, channel_id: str, content: str, reply_to: str | None = None
    ) -> dict[str, Any]:
        """Send a message to a channel."""
        body: dict[str, Any] = {"channel_id": channel_id, "content": content}
        if reply_to is not None:
            body["reply_to"] = reply_to
        return await self._request("POST", "/api/messages", json=body)  # type: ignore[return-value]

    async def list_messages(self, channel_id: str, *, limit: int = 50) -> list[Any]:
        """Read recent messages from a channel (default 50, max 100)."""
        return await self._request(  # type: ignore[return-value]
            "GET", f"/api/channels/{channel_id}/messages", params={"limit": limit}
        )

    async def search_messages(
        self, channel_id: str, *, q: str, limit: int = 25
    ) -> list[Any]:
        """Search messages in a channel."""
        return await self._request(  # type: ignore[return-value]
            "GET",
            f"/api/channels/{channel_id}/messages/search",
            params={"q": q, "limit": limit},
        )

    async def edit_message(
        self, channel_id: str, message_id: str, *, content: str
    ) -> dict[str, Any]:
        """Edit a message you own."""
        return await self._request(  # type: ignore[return-value]
            "PATCH",
            f"/api/channels/{channel_id}/messages/{message_id}",
            json={"content": content},
        )

    async def delete_message(self, channel_id: str, message_id: str) -> dict[str, Any]:
        """Delete a message."""
        return await self._request(  # type: ignore[return-value]
            "DELETE", f"/api/channels/{channel_id}/messages/{message_id}"
        )

    async def add_reaction(
        self, channel_id: str, message_id: str, *, emoji: str
    ) -> dict[str, Any]:
        """Add an emoji reaction to a message."""
        return await self._request(  # type: ignore[return-value]
            "POST",
            f"/api/channels/{channel_id}/messages/{message_id}/reactions",
            json={"emoji": emoji},
        )

    async def pin_message(self, channel_id: str, message_id: str) -> dict[str, Any]:
        """Pin a message in a channel."""
        return await self._request(  # type: ignore[return-value]
            "POST", f"/api/channels/{channel_id}/messages/{message_id}/pin"
        )

    async def create_dm(self, *, recipient_id: str) -> dict[str, Any]:
        """Open a DM channel with a user; returns the channel info."""
        return await self._request(  # type: ignore[return-value]
            "POST", "/api/dms", json={"recipient_id": recipient_id}
        )

    async def send_dm(self, *, recipient_id: str, content: str) -> dict[str, Any]:
        """Send a direct message to a user."""
        return await self._request(  # type: ignore[return-value]
            "POST", "/api/dms/send", json={"recipient_id": recipient_id, "content": content}
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncDiscordBotClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
