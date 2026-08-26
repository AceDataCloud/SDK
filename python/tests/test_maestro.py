"""Maestro generated provider contract tests."""

from typing import Any

from acedatacloud.resources.providers.maestro import Maestro


class Transport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"success": True, "task_id": "task-maestro", "trace_id": "trace-maestro"}


def test_generate_serializes_new_sku_contract() -> None:
    transport = Transport()
    client = Maestro(transport)

    result = client.generate(
        prompt="Launch video",
        quality="pro",
        duration=300,
        scenario="drama",
        action="extend",
        ref_task_id="task-before",
        langs=["en", "de"],
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
                "langs": ["en", "de"],
                "aspect": "9:16",
                "duration": 300,
                "quality": "pro",
                "scenario": "drama",
                "style": "auto",
                "voice": "auto",
            },
        )
    ]
    assert not hasattr(client, "estimates")
