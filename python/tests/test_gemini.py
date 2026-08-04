"""Gemini resource contract tests."""

from typing import Any

import pytest

from acedatacloud.resources.gemini import AsyncGemini, Gemini


class SyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"task_id": "task-gemini"}


class AsyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    async def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"task_id": "task-gemini"}


def test_chat_completions_posts_to_gemini_path() -> None:
    transport = SyncTransport()
    Gemini(transport).chat.completions.create(
        model="gemini-3.0-pro",
        messages=[{"role": "user", "content": "hi"}],
        temperature=0.5,
    )
    method, path, body = transport.calls[0]
    assert (method, path) == ("POST", "/gemini/chat/completions")
    assert body == {
        "model": "gemini-3.0-pro",
        "messages": [{"role": "user", "content": "hi"}],
        "temperature": 0.5,
    }


def test_videos_generate_applies_spec_defaults_and_returns_a_handle() -> None:
    transport = SyncTransport()
    handle = Gemini(transport).videos.generate(prompt="a kitten in a garden")

    method, path, body = transport.calls[0]
    assert (method, path) == ("POST", "/gemini/videos")
    assert body == {
        "prompt": "a kitten in a garden",
        "model": "omni-flash",
        "aspect_ratio": "16:9",
        "resolution": "720p",
        "async": True,
    }
    assert handle.id == "task-gemini"


def test_videos_generate_rejects_more_than_one_reference_video() -> None:
    """The spec caps video_urls at one item; failing here beats a 400."""
    with pytest.raises(ValueError, match="at most 1"):
        Gemini(SyncTransport()).videos.generate(
            prompt="x",
            video_urls=["https://example.com/a.mp4", "https://example.com/b.mp4"],
        )


def test_native_generate_content_puts_the_model_in_the_path() -> None:
    transport = SyncTransport()
    Gemini(transport).generate_content(
        model="gemini-2.5-flash",
        contents=[{"role": "user", "parts": [{"text": "hi"}]}],
        generationConfig={"temperature": 0.2},
    )
    method, path, body = transport.calls[0]
    assert (method, path) == ("POST", "/v1beta/models/gemini-2.5-flash:generateContent")
    assert body == {
        "contents": [{"role": "user", "parts": [{"text": "hi"}]}],
        "generationConfig": {"temperature": 0.2},
    }


@pytest.mark.asyncio
async def test_async_videos_generate_matches_the_sync_body() -> None:
    transport = AsyncTransport()
    handle = await AsyncGemini(transport).videos.generate(
        prompt="a kitten",
        resolution="1080p",
        aspect_ratio="9:16",
        image_urls=["https://example.com/a.png"],
        async_=False,
    )
    _method, path, body = transport.calls[0]
    assert path == "/gemini/videos"
    assert body["resolution"] == "1080p"
    assert body["aspect_ratio"] == "9:16"
    assert body["image_urls"] == ["https://example.com/a.png"]
    assert body["async"] is False
    assert handle.id == "task-gemini"


def test_client_exposes_gemini_and_the_tasks_endpoint() -> None:
    from acedatacloud import AceDataCloud
    from acedatacloud.resources.tasks import _SERVICE_TASK_ENDPOINTS

    client = AceDataCloud(api_token="test-token")
    assert isinstance(client.gemini, Gemini)
    assert _SERVICE_TASK_ENDPOINTS["gemini"] == "/gemini/tasks"
