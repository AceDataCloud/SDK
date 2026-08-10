"""Kimi chat completions resource."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

KimiModel = Literal["kimi-k3", "kimi-k2.6", "kimi-k2-thinking-turbo", "kimi-k2.5", "kimi-k2-thinking"]


class _Completions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: KimiModel,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/kimi/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/kimi/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: KimiModel,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/kimi/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", "/kimi/chat/completions", json=body):
            yield _json.loads(chunk)


class _Chat:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _AsyncChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class Kimi:
    """Synchronous Kimi client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _Chat(transport)


class AsyncKimi:
    """Async Kimi client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncChat(transport)
