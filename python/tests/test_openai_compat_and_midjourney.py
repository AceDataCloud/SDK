from __future__ import annotations

from typing import Any

from acedatacloud.resources.openai_compat import AsyncOpenAI, OpenAI
from acedatacloud.resources.providers.fish import Fish
from acedatacloud.resources.providers.midjourney import AsyncMidjourney, Midjourney


class SyncTransport:
    def __init__(self) -> None:
        self._base_url = "https://x402.acedata.cloud"
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = {"json": json, "params": params}
        self.calls.append((method, path, payload))
        return {"task_id": "task-1", "data": []}


class AsyncTransport(SyncTransport):
    async def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return super().request(method, path, json=json, params=params)


def test_openai_models_audio_and_realtime_are_available() -> None:
    transport = SyncTransport()
    client = OpenAI(transport)

    client.models.list()
    client.audio.speech(input="hello", model="tts-1", voice="alloy", response_format="mp3", speed=1.25)
    url = client.realtime.url(model="gpt-realtime")

    assert transport.calls == [
        ("GET", "/openai/models", {"json": None, "params": None}),
        (
            "POST",
            "/v1/audio/speech",
            {
                "json": {
                    "input": "hello",
                    "model": "tts-1",
                    "voice": "alloy",
                    "response_format": "mp3",
                    "speed": 1.25,
                },
                "params": None,
            },
        ),
    ]
    assert url == "wss://x402.acedata.cloud/v1/realtime?model=gpt-realtime"


async def test_async_openai_models_and_audio_match_sync_contract() -> None:
    transport = AsyncTransport()
    client = AsyncOpenAI(transport)

    await client.models.list()
    await client.audio.speech(input="hello")

    assert transport.calls == [
        ("GET", "/openai/models", {"json": None, "params": None}),
        ("POST", "/v1/audio/speech", {"json": {"input": "hello"}, "params": None}),
    ]
    assert client.realtime.url(model="gpt-realtime-2") == (
        "wss://x402.acedata.cloud/v1/realtime?model=gpt-realtime-2"
    )


def test_midjourney_provider_serializes_pollable_and_non_pollable_requests() -> None:
    transport = SyncTransport()
    client = Midjourney(transport)

    imagine = client.imagine(prompt="A cat", async_=False)
    describe = client.describe(image_url="https://example.com/cat.png")

    assert imagine.id == "task-1"
    assert describe == {"task_id": "task-1", "data": []}
    assert transport.calls == [
        (
            "POST",
            "/midjourney/imagine",
            {"json": {"prompt": "A cat", "async": False}, "params": None},
        ),
        (
            "POST",
            "/midjourney/describe",
            {"json": {"image_url": "https://example.com/cat.png"}, "params": None},
        ),
    ]


async def test_async_midjourney_provider_matches_sync_contract() -> None:
    transport = AsyncTransport()
    client = AsyncMidjourney(transport)

    handle = await client.videos(action="generate", prompt="Animate this")
    await client.translate(content="精致，无暇，洁白的天使")

    assert handle.id == "task-1"
    assert transport.calls == [
        (
            "POST",
            "/midjourney/videos",
            {"json": {"action": "generate", "prompt": "Animate this", "async": True}, "params": None},
        ),
        (
            "POST",
            "/midjourney/translate",
            {"json": {"content": "精致，无暇，洁白的天使"}, "params": None},
        ),
    ]


def test_fish_provider_exposes_model_read_endpoints() -> None:
    transport = SyncTransport()
    fish = Fish(transport)

    fish.list_models(page_size=10, page_number=2, self_only=True)
    fish.get_model("voice-1")

    assert transport.calls == [
        ("GET", "/fish/model", {"json": None, "params": {"page_size": 10, "page_number": 2, "self": True}}),
        ("GET", "/fish/model/voice-1", {"json": None, "params": None}),
    ]
