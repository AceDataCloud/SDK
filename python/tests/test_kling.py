"""Kling resource contract tests."""

from typing import Any

import pytest

from acedatacloud import (
    KlingCameraControl,
    KlingModel,
    KlingReferenceImage,
    KlingReferenceVideo,
    KlingWatermarkInfo,
)
from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle
from acedatacloud.resources.kling import AsyncKling, Kling


class SyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"task_id": "task-kling"}


class AsyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    async def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"task_id": "task-kling"}


def test_public_kling_types_are_importable() -> None:
    model: KlingModel = "kling-o1"
    camera: KlingCameraControl = {"type": "simple"}
    image: KlingReferenceImage = {"image_url": "https://example.com/ref.jpg"}
    video: KlingReferenceVideo = {"video_url": "https://example.com/ref.mp4"}
    watermark: KlingWatermarkInfo = {"enabled": True}
    assert model == "kling-o1"
    assert camera["type"] == "simple"
    assert image["image_url"].endswith("ref.jpg")
    assert video["video_url"].endswith("ref.mp4")
    assert watermark["enabled"] is True


def test_sync_generate_serializes_canonical_omni_request() -> None:
    transport = SyncTransport()
    client = Kling(transport)

    result = client.generate(
        action="text2video",
        model="kling-o1",
        prompt="Use the references",
        mode="std",
        duration=5,
        async_=True,
        timeout=600,
        image_list=[{"image_url": "https://example.com/ref.jpg"}],
        video_list=[
            {
                "video_url": "https://example.com/ref.mp4",
                "refer_type": "feature",
                "keep_original_sound": "yes",
            }
        ],
    )

    assert isinstance(result, TaskHandle)
    assert result.id == "task-kling"
    assert transport.calls == [
        (
            "POST",
            "/kling/videos",
            {
                "action": "text2video",
                "model": "kling-o1",
                "mode": "std",
                "prompt": "Use the references",
                "duration": 5,
                "async": True,
                "timeout": 600,
                "image_list": [{"image_url": "https://example.com/ref.jpg"}],
                "video_list": [
                    {
                        "video_url": "https://example.com/ref.mp4",
                        "refer_type": "feature",
                        "keep_original_sound": "yes",
                    }
                ],
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_generate_serializes_without_callback() -> None:
    transport = AsyncTransport()
    client = AsyncKling(transport)

    await client.generate(
        action="text2video",
        model="kling-o1",
        prompt="test",
        duration=5,
        async_=True,
    )

    assert transport.calls[0][2]["async"] is True
    assert "callback_url" not in transport.calls[0][2]


def test_sync_motion_uses_closed_serialization() -> None:
    transport = SyncTransport()
    client = Kling(transport)

    client.motion(
        mode="pro",
        image_url="https://example.com/subject.jpg",
        video_url="https://example.com/motion.mp4",
        character_orientation="image",
        model_name="kling-v3",
        keep_original_sound="yes",
        watermark_info={"enabled": True},
        prompt="follow the motion",
    )

    assert transport.calls == [
        (
            "POST",
            "/kling/motion",
            {
                "mode": "pro",
                "image_url": "https://example.com/subject.jpg",
                "video_url": "https://example.com/motion.mp4",
                "character_orientation": "image",
                "model_name": "kling-v3",
                "keep_original_sound": "yes",
                "watermark_info": {"enabled": True},
                "prompt": "follow the motion",
                "async": True,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_motion_uses_same_validation() -> None:
    transport = AsyncTransport()
    client = AsyncKling(transport)

    with pytest.raises(ValueError, match="video_url must be an HTTP URL"):
        await client.motion(
            mode="std",
            image_url="https://example.com/subject.jpg",
            video_url="file:///tmp/motion.mp4",
            character_orientation="video",
        )

    assert transport.calls == []


def test_generate_defaults_model_and_async_request() -> None:
    transport = SyncTransport()
    client = Kling(transport)

    handle = client.generate(action="text2video", prompt="test")

    assert isinstance(handle, TaskHandle)
    assert transport.calls[0][2]["model"] == "kling-v1"
    assert transport.calls[0][2]["async"] is True


def test_lip_sync_and_talking_photo_serialize_new_endpoints() -> None:
    transport = SyncTransport()
    client = Kling(transport)

    lip = client.lip_sync(
        mode="audio2video",
        video_url="https://example.com/source.mp4",
        audio_url="https://example.com/voice.mp3",
        voice_language="en",
        voice_speed=1.2,
    )
    talking = client.talking_photo(
        image_url="https://example.com/face.jpg",
        audio_url="https://example.com/voice.mp3",
        model="kling-v2-6",
        duration=5,
        mode="pro",
    )

    assert isinstance(lip, TaskHandle)
    assert isinstance(talking, TaskHandle)
    assert transport.calls[-2] == (
        "POST",
        "/kling/lip-sync",
        {
            "mode": "audio2video",
            "async": True,
            "video_url": "https://example.com/source.mp4",
            "audio_url": "https://example.com/voice.mp3",
            "audio_type": "url",
            "voice_language": "en",
            "voice_speed": 1.2,
        },
    )
    assert transport.calls[-1] == (
        "POST",
        "/kling/talking-photo",
        {
            "image_url": "https://example.com/face.jpg",
            "audio_url": "https://example.com/voice.mp3",
            "async": True,
            "model": "kling-v2-6",
            "duration": 5,
            "mode": "pro",
        },
    )


@pytest.mark.asyncio
async def test_async_lip_sync_returns_async_task_handle() -> None:
    transport = AsyncTransport()
    client = AsyncKling(transport)

    handle = await client.lip_sync(mode="text2video", video_id="video-1", text="hello", voice_id="voice")

    assert isinstance(handle, AsyncTaskHandle)
    assert transport.calls[0][1] == "/kling/lip-sync"


def test_generate_rejects_invalid_contract_before_transport() -> None:
    transport = SyncTransport()
    client = Kling(transport)

    with pytest.raises(ValueError, match="model must be one of"):
        client.generate(action="text2video", model="unknown-model", prompt="test")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="image_list must be non-empty"):
        client.generate(action="text2video", model="kling-o1", prompt="test", image_list=[])
    with pytest.raises(ValueError, match="base reference video"):
        client.generate(
            action="image2video",
            model="kling-v3-omni",
            prompt="test",
            start_image_url="https://example.com/start.jpg",
            video_list=[{"video_url": "https://example.com/ref.mp4", "refer_type": "base"}],
        )
    with pytest.raises(ValueError, match="callback_url must be an HTTP URL"):
        client.generate(
            action="text2video",
            model="kling-v3",
            prompt="test",
            callback_url="not-a-url",
        )

    assert transport.calls == []


@pytest.mark.parametrize(
    ("options", "message"),
    [
        ({"model": "kling-o1", "duration": 10}, "only 5-second"),
        ({"model": "kling-o1", "mode": "4k"}, "only std and pro"),
        ({"model": "kling-o1", "generate_audio": True}, "does not support generate_audio"),
        (
            {"model": "kling-v3", "image_list": [{"image_url": "https://example.com/ref.jpg"}]},
            "Omni references require",
        ),
        ({"action": "extend", "model": "kling-v3", "video_id": "video-1", "prompt": None}, "extend requires"),
        (
            {
                "model": "kling-o1",
                "image_list": [{"image_url": "https://example.com/ref.jpg", "type": "invalid"}],
            },
            "type must be first_frame or end_frame",
        ),
        (
            {
                "model": "kling-o1",
                "video_list": [{"video_url": "https://example.com/ref.mp4", "refer_type": "invalid"}],
            },
            "refer_type must be base or feature",
        ),
        (
            {
                "model": "kling-o1",
                "video_list": [
                    {
                        "video_url": "https://example.com/ref.mp4",
                        "refer_type": "feature",
                        "keep_original_sound": "invalid",
                    }
                ],
            },
            "keep_original_sound must be yes or no",
        ),
        (
            {
                "model": "kling-o1",
                "image_list": [{"image_url": f"https://example.com/ref-{index}.jpg"} for index in range(8)],
            },
            "cannot exceed 7",
        ),
    ],
)
def test_generate_rejects_model_and_reference_constraints(options: dict[str, Any], message: str) -> None:
    transport = SyncTransport()
    client = Kling(transport)
    request = {
        "action": "text2video",
        "model": "kling-o1",
        "prompt": "test",
        **options,
    }

    with pytest.raises(ValueError, match=message):
        client.generate(**request)  # type: ignore[arg-type]

    assert transport.calls == []
