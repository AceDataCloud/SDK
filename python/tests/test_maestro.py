"""Maestro generated provider contract tests."""

import inspect
from typing import Any
from unittest.mock import AsyncMock

import pytest

from acedatacloud.resources.providers.maestro import AsyncMaestro, Maestro


class Transport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"success": True, "task_id": "task-maestro", "trace_id": "trace-maestro"}


def test_generate_serializes_single_language_contract() -> None:
    transport = Transport()
    client = Maestro(transport)

    result = client.generate(
        prompt="Launch video",
        duration=300,
        scenario="drama",
        action="extend",
        ref_task_id="task-before",
        langs=["en"],
    )

    assert result.id == "task-maestro"
    assert transport.calls == [
        (
            "POST",
            "/maestro/videos",
            {
                "prompt": "Launch video",
                "action": "extend",
                "ref_task_id": "task-before",
                "langs": ["en"],
                "aspect": "9:16",
                "duration": 300,
                "scenario": "drama",
                "style": "auto",
                "voice": "auto",
                "async": True,
            },
        )
    ]
    assert not hasattr(client, "estimates")
    assert "quality" not in inspect.signature(client.generate).parameters


def test_generate_defaults_to_chinese_without_quality() -> None:
    transport = Transport()
    Maestro(transport).generate(prompt="Launch video")
    body = transport.calls[0][2]
    assert body["langs"] == ["zh-cn"]
    assert "quality" not in body


@pytest.mark.parametrize("langs", [[], ["en", "de"]])
def test_generate_rejects_invalid_language_count(langs: list[str]) -> None:
    transport = Transport()
    with pytest.raises(ValueError, match="langs must contain exactly one item"):
        Maestro(transport).generate(prompt="Launch video", langs=langs)
    assert transport.calls == []


@pytest.mark.parametrize("langs", [None, ["en"]])
async def test_async_generate_language_and_defaults(langs: list[str] | None) -> None:
    transport = AsyncMock()
    transport.request.return_value = {"task_id": "task-maestro"}
    task = await AsyncMaestro(transport).generate(prompt="Launch video", langs=langs)
    assert task.id == "task-maestro"
    body = transport.request.call_args.kwargs["json"]
    assert body["langs"] == (langs if langs is not None else ["zh-cn"])
    assert "quality" not in body
    await task.get()
    assert transport.request.call_args.args == ("POST", "/maestro/tasks")


@pytest.mark.parametrize("langs", [[], ["en", "de"]])
async def test_async_generate_rejects_invalid_language_count(langs: list[str]) -> None:
    transport = AsyncMock()
    with pytest.raises(ValueError, match="langs must contain exactly one item"):
        await AsyncMaestro(transport).generate(prompt="Launch video", langs=langs)
    transport.request.assert_not_called()
