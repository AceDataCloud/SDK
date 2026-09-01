"""Fish generated provider contract tests."""

from typing import Any

from acedatacloud.resources.providers.fish import Fish


class Transport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any], dict[str, str]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any], extra_headers: dict[str, str]) -> dict[str, Any]:
        self.calls.append((method, path, json, extra_headers))
        return {"task_id": "task-fish"}


def test_generate_serializes_current_fish_contract() -> None:
    transport = Transport()
    result = Fish(transport).generate(text="Hello", format="pcm", mp3_bitrate=192, model="s2.1-pro")

    assert result.id == "task-fish"
    assert transport.calls == [
        (
            "POST",
            "/fish/tts",
            {"text": "Hello", "format": "pcm", "mp3_bitrate": 192, "async": True},
            {"model": "s2.1-pro"},
        )
    ]
