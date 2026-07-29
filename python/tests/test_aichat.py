"""AI Chat resource contract tests."""

from typing import Any

import pytest

from acedatacloud.resources.aichat import AiChat, AsyncAiChat


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


def test_create_preserves_legacy_aichat_endpoint() -> None:
    transport = SyncTransport()
    client = AiChat(transport)

    result = client.create(
        model="gpt-5.6-sol",
        question="Hello",
        id="conv-1",
        preset="default",
        stateful=True,
        references=["doc-1"],
    )

    assert result == {"ok": True}
    assert transport.calls == [
        (
            "POST",
            "/aichat/conversations",
            {
                "model": "gpt-5.6-sol",
                "question": "Hello",
                "id": "conv-1",
                "preset": "default",
                "stateful": True,
                "references": ["doc-1"],
            },
        )
    ]


def test_create_v2_serializes_new_aichat2_contract() -> None:
    transport = SyncTransport()
    client = AiChat(transport)

    result = client.create_v2(
        model="claude-sonnet-5",
        action="chat",
        id="conv-2",
        question="Summarize this",
        message={"role": "user", "content": "Hello"},
        stateful=False,
        references=["doc-1", "doc-2"],
        preset="agent",
        max_turns=8,
        async_=True,
        callback_url="https://example.com/callback",
        allowed_skills=["browser"],
        allowed_mcp_servers=["github"],
        unattended_policy={"mode": "auto"},
        tool_results=[{"tool": "search", "result": "done"}],
        messages=[{"role": "user", "content": "Hello again"}],
        title="Research thread",
        user_id="user-1",
        application_id="app-1",
        model_group="claude",
        offset=10,
        limit=5,
    )

    assert result == {"ok": True}
    assert transport.calls == [
        (
            "POST",
            "/aichat2/conversations",
            {
                "model": "claude-sonnet-5",
                "action": "chat",
                "id": "conv-2",
                "question": "Summarize this",
                "message": {"role": "user", "content": "Hello"},
                "stateful": False,
                "references": ["doc-1", "doc-2"],
                "preset": "agent",
                "max_turns": 8,
                "async": True,
                "callback_url": "https://example.com/callback",
                "allowed_skills": ["browser"],
                "allowed_mcp_servers": ["github"],
                "unattended_policy": {"mode": "auto"},
                "tool_results": [{"tool": "search", "result": "done"}],
                "messages": [{"role": "user", "content": "Hello again"}],
                "title": "Research thread",
                "user_id": "user-1",
                "application_id": "app-1",
                "model_group": "claude",
                "offset": 10,
                "limit": 5,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_create_v2_uses_same_aichat2_endpoint() -> None:
    transport = AsyncTransport()
    client = AsyncAiChat(transport)

    result = await client.create_v2(model="gpt-5.2-pro", action="retrieve", limit=20)

    assert result == {"ok": True}
    assert transport.calls == [
        (
            "POST",
            "/aichat2/conversations",
            {
                "model": "gpt-5.2-pro",
                "action": "retrieve",
                "limit": 20,
            },
        )
    ]
