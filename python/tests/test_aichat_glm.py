"""AIChat and GLM resource contract tests."""

from typing import Any, get_args

import pytest

from acedatacloud.resources.aichat import AiChat, AiChat2Model, AiChatModel, AsyncAiChat
from acedatacloud.resources.glm import Glm, GlmModel


class SyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"ok": True}


class AsyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    async def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"ok": True}


def test_aichat_model_enums_include_latest_docs_values() -> None:
    assert "gpt-5.6-sol" in get_args(AiChatModel)
    assert "deepseek-v4-pro" in get_args(AiChatModel)
    assert "glm-5.3" in get_args(AiChatModel)
    assert "gpt-5.4-mini" in get_args(AiChat2Model)
    assert "claude-opus-4-6" in get_args(AiChat2Model)
    assert "kimi-k3" in get_args(AiChat2Model)


def test_aichat_create_v2_serialization() -> None:
    transport = SyncTransport()
    aichat = AiChat(transport)

    aichat.create_v2(
        model="gpt-5.4-mini",
        action="retrieve_batch",
        ids=["extra-id"],
        async_=False,
        offset=0,
        limit=25,
        allowed_mcp_servers=["server-a"],
        tool_results=[{"tool_use_id": "tool-1", "output": "ok", "is_error": False}],
        model_group="chatgpt",
    )

    assert transport.calls == [
        (
            "POST",
            "/aichat2/conversations",
            {
                "model": "gpt-5.4-mini",
                "ids": ["extra-id"],
                "action": "retrieve_batch",
                "async": False,
                "allowed_mcp_servers": ["server-a"],
                "tool_results": [{"tool_use_id": "tool-1", "output": "ok", "is_error": False}],
                "model_group": "chatgpt",
                "offset": 0,
                "limit": 25,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_aichat_create_v2_serialization() -> None:
    transport = AsyncTransport()
    aichat = AsyncAiChat(transport)

    await aichat.create_v2(model="glm-5", message="hi", stateful=True)

    assert transport.calls == [
        ("POST", "/aichat2/conversations", {"model": "glm-5", "message": "hi", "stateful": True})
    ]


def test_glm_model_enum_and_serialization() -> None:
    assert "glm-5.3" in get_args(GlmModel)
    assert "glm-5-turbo" in get_args(GlmModel)

    transport = SyncTransport()
    glm = Glm(transport)

    glm.chat.completions.create(
        model="glm-5.3",
        messages=[{"role": "user", "content": "hi"}],
        n=1,
        temperature=0,
        parallel_tool_calls=False,
        reasoning_effort="low",
        web_search_options={"search_context_size": "medium"},
    )

    assert transport.calls == [
        (
            "POST",
            "/glm/chat/completions",
            {
                "model": "glm-5.3",
                "messages": [{"role": "user", "content": "hi"}],
                "n": 1,
                "temperature": 0,
                "parallel_tool_calls": False,
                "reasoning_effort": "low",
                "web_search_options": {"search_context_size": "medium"},
            },
        )
    ]
