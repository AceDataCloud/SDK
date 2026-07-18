"""AI Chat v2 resources — aichat2/conversations endpoint."""

from __future__ import annotations

from typing import Any, Literal

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
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-haiku-4-5-20251001",
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-opus-4-5-20251101",
    "claude-opus-4-6",
    "claude-fable-5",
    "claude-opus-4-8",
    "claude-opus-4-7",
    "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-6",
    "claude-sonnet-5",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3-pro-preview",
    "gemini-3.1-flash-image-preview",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-pro",
    "gemini-3.1-pro-preview",
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
    "kimi-k2-0711-preview",
    "kimi-k2-0905-preview",
    "kimi-k2-instruct-0905",
    "kimi-k2-thinking",
    "kimi-k2-thinking-turbo",
    "kimi-k2-turbo-preview",
    "kimi-k3",
    "kimi-k2.5",
    "glm-3-turbo",
    "glm-4.5",
    "glm-4.5v",
    "glm-4.6",
    "glm-4.7",
    "glm-5",
    "glm-5-turbo",
    "glm-5.2",
    "glm-5.1",
    "o1",
    "o1-mini",
    "o1-pro",
    "o3",
    "o3-mini",
    "o3-pro",
    "o4-mini",
]


class AiChat2:
    """Synchronous AI chat v2 client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: str,
        action: str | None = None,
        id: str | None = None,
        question: str | None = None,
        message: str | list[Any] | None = None,
        stateful: bool | None = None,
        references: list[str] | None = None,
        preset: str | None = None,
        max_turns: int | None = None,
        async_mode: bool | None = None,
        callback_url: str | None = None,
        allowed_skills: list[str] | None = None,
        allowed_mcp_servers: list[str] | None = None,
        unattended_policy: dict[str, Any] | None = None,
        tool_results: list[dict[str, Any]] | None = None,
        messages: list[dict[str, Any]] | None = None,
        title: str | None = None,
        user_id: str | None = None,
        application_id: str | None = None,
        model_group: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, **kwargs}
        if action is not None:
            body["action"] = action
        if id is not None:
            body["id"] = id
        if question is not None:
            body["question"] = question
        if message is not None:
            body["message"] = message
        if stateful is not None:
            body["stateful"] = stateful
        if references is not None:
            body["references"] = references
        if preset is not None:
            body["preset"] = preset
        if max_turns is not None:
            body["max_turns"] = max_turns
        if async_mode is not None:
            body["async"] = async_mode
        if callback_url is not None:
            body["callback_url"] = callback_url
        if allowed_skills is not None:
            body["allowed_skills"] = allowed_skills
        if allowed_mcp_servers is not None:
            body["allowed_mcp_servers"] = allowed_mcp_servers
        if unattended_policy is not None:
            body["unattended_policy"] = unattended_policy
        if tool_results is not None:
            body["tool_results"] = tool_results
        if messages is not None:
            body["messages"] = messages
        if title is not None:
            body["title"] = title
        if user_id is not None:
            body["user_id"] = user_id
        if application_id is not None:
            body["application_id"] = application_id
        if model_group is not None:
            body["model_group"] = model_group
        if offset is not None:
            body["offset"] = offset
        if limit is not None:
            body["limit"] = limit
        return self._transport.request("POST", "/aichat2/conversations", json=body)


class AsyncAiChat2:
    """Async AI chat v2 client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: str,
        action: str | None = None,
        id: str | None = None,
        question: str | None = None,
        message: str | list[Any] | None = None,
        stateful: bool | None = None,
        references: list[str] | None = None,
        preset: str | None = None,
        max_turns: int | None = None,
        async_mode: bool | None = None,
        callback_url: str | None = None,
        allowed_skills: list[str] | None = None,
        allowed_mcp_servers: list[str] | None = None,
        unattended_policy: dict[str, Any] | None = None,
        tool_results: list[dict[str, Any]] | None = None,
        messages: list[dict[str, Any]] | None = None,
        title: str | None = None,
        user_id: str | None = None,
        application_id: str | None = None,
        model_group: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, **kwargs}
        if action is not None:
            body["action"] = action
        if id is not None:
            body["id"] = id
        if question is not None:
            body["question"] = question
        if message is not None:
            body["message"] = message
        if stateful is not None:
            body["stateful"] = stateful
        if references is not None:
            body["references"] = references
        if preset is not None:
            body["preset"] = preset
        if max_turns is not None:
            body["max_turns"] = max_turns
        if async_mode is not None:
            body["async"] = async_mode
        if callback_url is not None:
            body["callback_url"] = callback_url
        if allowed_skills is not None:
            body["allowed_skills"] = allowed_skills
        if allowed_mcp_servers is not None:
            body["allowed_mcp_servers"] = allowed_mcp_servers
        if unattended_policy is not None:
            body["unattended_policy"] = unattended_policy
        if tool_results is not None:
            body["tool_results"] = tool_results
        if messages is not None:
            body["messages"] = messages
        if title is not None:
            body["title"] = title
        if user_id is not None:
            body["user_id"] = user_id
        if application_id is not None:
            body["application_id"] = application_id
        if model_group is not None:
            body["model_group"] = model_group
        if offset is not None:
            body["offset"] = offset
        if limit is not None:
            body["limit"] = limit
        return await self._transport.request("POST", "/aichat2/conversations", json=body)
