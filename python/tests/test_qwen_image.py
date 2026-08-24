"""Qwen Image generated provider contract tests."""

from typing import Any

from acedatacloud._runtime.tasks import TaskHandle
from acedatacloud.resources.providers.qwen_image import QwenImage


class Transport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"task_id": "qwen-image-1"}


def test_generate_serializes_qwen_image_contract() -> None:
    transport = Transport()
    client = QwenImage(transport)

    task = client.generate(
        model="qwen-image-3.0-pro",
        prompt="A watercolor city",
        image_urls=["https://cdn.example.com/reference.png"],
        n=2,
        size="1536x1024",
        prompt_extend=False,
        prompt_extend_mode="agent",
        enable_thinking=False,
        negative_prompt="text",
        seed=42,
        watermark=True,
    )

    assert isinstance(task, TaskHandle)
    assert task.id == "qwen-image-1"
    assert transport.calls == [
        (
            "POST",
            "/qwen-image/images",
            {
                "model": "qwen-image-3.0-pro",
                "prompt": "A watercolor city",
                "image_urls": ["https://cdn.example.com/reference.png"],
                "n": 2,
                "size": "1536x1024",
                "prompt_extend": False,
                "prompt_extend_mode": "agent",
                "enable_thinking": False,
                "negative_prompt": "text",
                "seed": 42,
                "watermark": True,
                "async": True,
            },
        )
    ]


def test_generate_applies_documented_defaults() -> None:
    transport = Transport()
    client = QwenImage(transport)

    client.generate(model="qwen-image-3.0", prompt="A lighthouse")

    assert transport.calls[0][2] == {
        "model": "qwen-image-3.0",
        "prompt": "A lighthouse",
        "n": 1,
        "prompt_extend": True,
        "prompt_extend_mode": "direct",
        "enable_thinking": True,
        "watermark": False,
        "async": True,
    }
