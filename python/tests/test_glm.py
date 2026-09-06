"""GLM resource tests."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

import pytest

from acedatacloud.resources.glm import AsyncGlm, Glm


class SyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.stream_calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"id": "sync"}

    def request_stream(self, method: str, path: str, *, json: dict[str, Any]) -> Iterator[str]:
        self.stream_calls.append((method, path, json))
        yield '{"delta":"hello"}'


class AsyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.stream_calls: list[tuple[str, str, dict[str, Any]]] = []

    async def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"id": "async"}

    async def request_stream(self, method: str, path: str, *, json: dict[str, Any]) -> AsyncIterator[str]:
        self.stream_calls.append((method, path, json))
        yield '{"delta":"hello"}'


def test_sync_glm_create_posts_to_chat_completions() -> None:
    transport = SyncTransport()
    client = Glm(transport)

    result = client.chat.completions.create(
        model="glm-5.3",
        messages=[{"role": "user", "content": "Hi"}],
        temperature=0.2,
    )

    assert result == {"id": "sync"}
    assert transport.calls == [
        (
            "POST",
            "/glm/chat/completions",
            {"model": "glm-5.3", "messages": [{"role": "user", "content": "Hi"}], "temperature": 0.2},
        )
    ]


def test_sync_glm_stream_sets_stream_flag() -> None:
    transport = SyncTransport()
    client = Glm(transport)

    chunks = list(
        client.chat.completions.create(
            model="glm-5.2",
            messages=[{"role": "user", "content": "Hi"}],
            stream=True,
        )
    )

    assert chunks == [{"delta": "hello"}]
    assert transport.stream_calls == [
        (
            "POST",
            "/glm/chat/completions",
            {"model": "glm-5.2", "messages": [{"role": "user", "content": "Hi"}], "stream": True},
        )
    ]


@pytest.mark.asyncio
async def test_async_glm_stream_sets_stream_flag() -> None:
    transport = AsyncTransport()
    client = AsyncGlm(transport)

    stream = await client.chat.completions.create(
        model="glm-5.1",
        messages=[{"role": "user", "content": "Hi"}],
        stream=True,
    )
    chunks = [chunk async for chunk in stream]

    assert chunks == [{"delta": "hello"}]
    assert transport.stream_calls == [
        (
            "POST",
            "/glm/chat/completions",
            {"model": "glm-5.1", "messages": [{"role": "user", "content": "Hi"}], "stream": True},
        )
    ]
