"""Focused contracts for generated providers refreshed from Docs."""

import inspect
import typing
from unittest.mock import Mock

from acedatacloud.resources.providers.producer import Producer
from acedatacloud.resources.providers.seedance import Seedance
from acedatacloud.resources.providers.seedream import Seedream, SeedreamModel
from acedatacloud.resources.providers.wan import Wan


def test_producer_lyrics_prompt_is_a_string() -> None:
    transport = Mock()
    transport.request.return_value = {"lyrics": "Verse"}
    producer = Producer(transport)

    producer.lyrics(prompt="Write a summer chorus")

    assert transport.request.call_args.args == ("POST", "/producer/lyrics")
    assert transport.request.call_args.kwargs["json"] == {"prompt": "Write a summer chorus"}


def test_seedance_serializes_priority_and_safety_identifier() -> None:
    transport = Mock()
    transport.request.return_value = {"task_id": "seedance-25"}
    seedance = Seedance(transport)

    seedance.generate(
        model="doubao-seedance-2-5-260628",
        content=[{"type": "text", "text": "Extend the scene"}],
        priority=7,
        safety_identifier="tenant-42",
    )

    body = transport.request.call_args.kwargs["json"]
    assert body["priority"] == 7
    assert body["safety_identifier"] == "tenant-42"


def test_seedream_removes_retired_models_and_parameters() -> None:
    models = typing.get_args(SeedreamModel)
    parameters = inspect.signature(Seedream.generate).parameters

    assert "doubao-seedream-3-0-t2i-250415" not in models
    assert "doubao-seededit-3-0-i2i-250628" not in models
    assert "seed" not in parameters
    assert "guidance_scale" not in parameters


def test_wan_exposes_new_fields_without_requiring_action_or_prompt() -> None:
    transport = Mock()
    transport.request.return_value = {"task_id": "wan-3"}
    wan = Wan(transport)

    wan.generate(
        model="wan3.0-video",
        media=[{"type": "image", "url": "https://cdn.example.com/frame.png"}],
        ratio="9:16",
        seed=42,
        watermark=True,
    )

    body = transport.request.call_args.kwargs["json"]
    assert body["model"] == "wan3.0-video"
    assert body["action"] == "text2video"
    assert body["media"] == [{"type": "image", "url": "https://cdn.example.com/frame.png"}]
    assert body["ratio"] == "9:16"
    assert body["seed"] == 42
    assert body["watermark"] is True
    assert "prompt" not in body
