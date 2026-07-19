"""Images resource contract tests."""

from typing import Any

import pytest

from acedatacloud.resources.images import AsyncImages, Images


class SyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"task_id": "task-image"}


class AsyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    async def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"task_id": "task-image"}


def test_sync_nano_banana_defaults_match_docs() -> None:
    transport = SyncTransport()
    client = Images(transport)

    client.generate(
        prompt="A cat",
        image_url="https://example.com/reference.png",
        count=2,
    )

    assert transport.calls == [
        (
            "POST",
            "/nano-banana/images",
            {
                "prompt": "A cat",
                "action": "generate",
                "image_urls": ["https://example.com/reference.png"],
                "count": 2,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_non_nano_banana_payloads_are_unchanged() -> None:
    transport = AsyncTransport()
    client = AsyncImages(transport)

    await client.generate(
        provider="flux",
        prompt="A cat",
        image_url="https://example.com/reference.png",
    )

    assert transport.calls == [
        (
            "POST",
            "/flux/images",
            {
                "prompt": "A cat",
                "image_url": "https://example.com/reference.png",
            },
        )
    ]
