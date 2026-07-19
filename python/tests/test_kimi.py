"""Kimi resource contract tests."""

from typing import Any

import pytest

from acedatacloud import KimiModel
from acedatacloud.resources.kimi import AsyncKimi, Kimi


class SyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"id": "chatcmpl-kimi"}


class AsyncTransport:
    def __init__(self) -> None:
        self.request_calls: list[tuple[str, str, dict[str, Any]]] = []
        self.stream_calls: list[tuple[str, str, dict[str, Any]]] = []

    async def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.request_calls.append((method, path, json))
        return {"id": "chatcmpl-kimi"}

    async def request_stream(self, method: str, path: str, *, json: dict[str, Any]):
        self.stream_calls.append((method, path, json))
        yield '{"delta":"hello"}'


def test_public_kimi_type_is_importable() -> None:
    model: KimiModel = "kimi-k3"
    assert model == "kimi-k3"


def test_sync_chat_completions_uses_kimi_endpoint() -> None:
    transport = SyncTransport()
    client = Kimi(transport)

    result = client.chat.completions.create(
        model="kimi-k3",
        messages=[{"role": "user", "content": "hello"}],
        temperature=0.2,
    )

    assert result == {"id": "chatcmpl-kimi"}
    assert transport.calls == [
        (
            "POST",
            "/kimi/chat/completions",
            {
                "model": "kimi-k3",
                "messages": [{"role": "user", "content": "hello"}],
                "temperature": 0.2,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_stream_chat_completions_use_kimi_endpoint() -> None:
    transport = AsyncTransport()
    client = AsyncKimi(transport)

    stream = await client.chat.completions.create(
        model="kimi-k3",
        messages=[{"role": "user", "content": "hello"}],
        stream=True,
    )
    chunks = [chunk async for chunk in stream]

    assert chunks == [{"delta": "hello"}]
    assert transport.stream_calls == [
        (
            "POST",
            "/kimi/chat/completions",
            {
                "model": "kimi-k3",
                "messages": [{"role": "user", "content": "hello"}],
                "stream": True,
            },
        )
    ]
