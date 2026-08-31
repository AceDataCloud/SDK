"""AI Chat resources — aichat/conversations endpoint."""

from __future__ import annotations

from typing import Any, Literal

AiChatModel = Literal[
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.4-pro",
    "gpt-5.2",
    "gpt-5.1",
    "gpt-5.1-all",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-5-all",
    "gpt-4",
    "gpt-4-all",
    "gpt-4-turbo",
    "gpt-4-turbo-preview",
    "gpt-4-vision-preview",
    "gpt-4.1",
    "gpt-4.1-2025-04-14",
    "gpt-4.1-mini",
    "gpt-4.1-mini-2025-04-14",
    "gpt-4.1-nano",
    "gpt-4.1-nano-2025-04-14",
    "gpt-4.5-preview",
    "gpt-4.5-preview-2025-02-27",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-11-20",
    "gpt-4o-all",
    "gpt-4o-image",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-mini-search-preview",
    "gpt-4o-mini-search-preview-2025-03-11",
    "gpt-4o-search-preview",
    "gpt-4o-search-preview-2025-03-11",
    "o1",
    "o1-2024-12-17",
    "o1-all",
    "o1-mini",
    "o1-mini-2024-09-12",
    "o1-mini-all",
    "o1-preview",
    "o1-preview-2024-09-12",
    "o1-preview-all",
    "o1-pro",
    "o1-pro-2025-03-19",
    "o1-pro-all",
    "o3",
    "o3-2025-04-16",
    "o3-all",
    "o3-mini",
    "o3-mini-2025-01-31",
    "o3-mini-2025-01-31-high",
    "o3-mini-2025-01-31-low",
    "o3-mini-2025-01-31-medium",
    "o3-mini-all",
    "o3-mini-high",
    "o3-mini-high-all",
    "o3-mini-low",
    "o3-mini-medium",
    "o3-pro",
    "o3-pro-2025-06-10",
    "o4-mini",
    "o4-mini-2025-04-16",
    "o4-mini-all",
    "o4-mini-high-all",
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v4-flash",
    "grok-3",
    "glm-5.1",
    "glm-4.7",
    "glm-4.6",
    "glm-3-turbo",
]

AiChat2Model = Literal[
    "gpt-4",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-all",
    "gpt-4o-image",
    "gpt-4o-mini",
    "gpt-5-all",
    "gpt-5.1-all",
    "gpt-5.2-pro",
    "gpt-5.4-mini",
    "gpt-5.4-nano",
    "gpt-image-1",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022",
    "claude-3-7-sonnet-20250219",
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-haiku-4-5-20251001",
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-opus-4-5-20251101",
    "claude-opus-4-6",
    "claude-fable-5",
    "claude-opus-5",
    "claude-opus-4-8",
    "claude-opus-4-7",
    "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-6",
    "claude-sonnet-5",
    "grok-3",
    "grok-3-fast",
    "grok-4",
    "grok-4.5",
    "grok-4-0709",
    "deepseek-chat",
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-reasoner",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v3.2-exp",
    "deepseek-v4-flash",
    "deepseek-v4-pro",
    "kimi-k2-thinking",
    "kimi-k2-thinking-turbo",
    "kimi-k3",
    "kimi-k2.6",
    "kimi-k2.5",
    "glm-3-turbo",
    "glm-4.5",
    "glm-4.5v",
    "glm-4.6",
    "glm-4.7",
    "glm-5",
    "glm-5-turbo",
    "glm-5.3",
    "glm-5.2",
    "glm-5.1",
    "o1",
    "o1-mini",
    "o1-pro",
    "o3",
    "o3-mini",
    "o3-pro",
    "o4-mini",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]
AiChat2Action = Literal["chat", "retrieve", "retrieve_batch", "update", "delete"]
AiChat2ModelGroup = Literal["chatgpt", "claude", "gemini", "grok", "kimi", "glm", "deepseek"]


def _build_v2_body(model: str, values: dict[str, Any]) -> dict[str, Any]:
    body = {"model": model}
    body.update({key: value for key, value in values.items() if value is not None})
    return body


class AiChat:
    """Synchronous AI chat client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: AiChatModel,
        question: str,
        id: str | None = None,
        preset: str | None = None,
        stateful: bool | None = None,
        references: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, "question": question, **kwargs}
        if id is not None:
            body["id"] = id
        if preset is not None:
            body["preset"] = preset
        if stateful is not None:
            body["stateful"] = stateful
        if references is not None:
            body["references"] = references
        return self._transport.request("POST", "/aichat/conversations", json=body)

    def create_v2(
        self,
        *,
        model: AiChat2Model,
        action: AiChat2Action | None = None,
        id: str | None = None,
        question: str | None = None,
        message: str | dict[str, Any] | None = None,
        stateful: bool | None = None,
        references: list[str] | None = None,
        preset: str | None = None,
        max_turns: int | None = None,
        async_: bool | None = None,
        callback_url: str | None = None,
        allowed_skills: list[str] | None = None,
        allowed_mcp_servers: list[str] | None = None,
        unattended_policy: dict[str, Any] | None = None,
        tool_results: list[dict[str, Any]] | None = None,
        messages: list[dict[str, Any]] | None = None,
        title: str | None = None,
        user_id: str | None = None,
        application_id: str | None = None,
        model_group: AiChat2ModelGroup | None = None,
        offset: int | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = _build_v2_body(
            model,
            {
                "action": action,
                "id": id,
                "question": question,
                "message": message,
                "stateful": stateful,
                "references": references,
                "preset": preset,
                "max_turns": max_turns,
                "async": async_,
                "callback_url": callback_url,
                "allowed_skills": allowed_skills,
                "allowed_mcp_servers": allowed_mcp_servers,
                "unattended_policy": unattended_policy,
                "tool_results": tool_results,
                "messages": messages,
                "title": title,
                "user_id": user_id,
                "application_id": application_id,
                "model_group": model_group,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )
        return self._transport.request("POST", "/aichat2/conversations", json=body)


class AsyncAiChat:
    """Async AI chat client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: AiChatModel,
        question: str,
        id: str | None = None,
        preset: str | None = None,
        stateful: bool | None = None,
        references: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, "question": question, **kwargs}
        if id is not None:
            body["id"] = id
        if preset is not None:
            body["preset"] = preset
        if stateful is not None:
            body["stateful"] = stateful
        if references is not None:
            body["references"] = references
        return await self._transport.request("POST", "/aichat/conversations", json=body)

    async def create_v2(
        self,
        *,
        model: AiChat2Model,
        action: AiChat2Action | None = None,
        id: str | None = None,
        question: str | None = None,
        message: str | dict[str, Any] | None = None,
        stateful: bool | None = None,
        references: list[str] | None = None,
        preset: str | None = None,
        max_turns: int | None = None,
        async_: bool | None = None,
        callback_url: str | None = None,
        allowed_skills: list[str] | None = None,
        allowed_mcp_servers: list[str] | None = None,
        unattended_policy: dict[str, Any] | None = None,
        tool_results: list[dict[str, Any]] | None = None,
        messages: list[dict[str, Any]] | None = None,
        title: str | None = None,
        user_id: str | None = None,
        application_id: str | None = None,
        model_group: AiChat2ModelGroup | None = None,
        offset: int | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = _build_v2_body(
            model,
            {
                "action": action,
                "id": id,
                "question": question,
                "message": message,
                "stateful": stateful,
                "references": references,
                "preset": preset,
                "max_turns": max_turns,
                "async": async_,
                "callback_url": callback_url,
                "allowed_skills": allowed_skills,
                "allowed_mcp_servers": allowed_mcp_servers,
                "unattended_policy": unattended_policy,
                "tool_results": tool_results,
                "messages": messages,
                "title": title,
                "user_id": user_id,
                "application_id": application_id,
                "model_group": model_group,
                "offset": offset,
                "limit": limit,
                **kwargs,
            },
        )
        return await self._transport.request("POST", "/aichat2/conversations", json=body)
