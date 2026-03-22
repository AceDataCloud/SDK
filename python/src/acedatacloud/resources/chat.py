"""Chat resources — native provider APIs (Claude Messages, etc.)."""

from __future__ import annotations

import json as _json
from collections.abc import Iterator
from typing import Any


class _Messages:
    """Namespace for chat.messages operations."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            **kwargs,
        }
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/v1/messages", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/v1/messages", json=body):
            yield _json.loads(chunk)

    def count_tokens(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {"model": model, "messages": messages, **kwargs}
        return self._transport.request("POST", "/v1/messages/count_tokens", json=body)


class _AsyncMessages:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            **kwargs,
        }
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/v1/messages", json=body)

    async def _stream(self, body: dict[str, Any]):
        async for chunk in self._transport.request_stream("POST", "/v1/messages", json=body):
            yield _json.loads(chunk)

    async def count_tokens(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {"model": model, "messages": messages, **kwargs}
        return await self._transport.request("POST", "/v1/messages/count_tokens", json=body)


class Chat:
    """Synchronous chat client for native provider APIs."""

    def __init__(self, transport: Any) -> None:
        self.messages = _Messages(transport)


class AsyncChat:
    """Async chat client for native provider APIs."""

    def __init__(self, transport: Any) -> None:
        self.messages = _AsyncMessages(transport)
