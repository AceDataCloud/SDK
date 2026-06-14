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
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-haiku-4-5-20251001",
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-opus-4-5-20251101",
    "claude-opus-4-6",
    "claude-opus-4-7",
    "claude-opus-4-8",
    "claude-sonnet-4-20250514",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-6",
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
    "kimi-k2.5",
    "glm-3-turbo",
    "glm-4.5",
    "glm-4.5v",
    "glm-4.6",
    "glm-4.7",
    "glm-5",
    "glm-5-turbo",
    "glm-5.1",
    "o1",
    "o1-mini",
    "o1-pro",
    "o3",
    "o3-mini",
    "o3-pro",
    "o4-mini",
]

AiChat2ModelGroup = Literal["chatgpt", "claude", "gemini", "grok", "kimi", "glm", "deepseek"]


class AiChat:
    """Synchronous AI chat client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: str,
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

    def create2(
        self,
        *,
        model: str,
        question: str | None = None,
        action: Literal["chat", "retrieve", "retrieve_batch", "update", "delete"] | None = None,
        id: str | None = None,
        preset: str | None = None,
        stateful: bool | None = None,
        references: list[Any] | None = None,
        max_turns: int | None = None,
        tool_results: list[Any] | None = None,
        messages: list[Any] | None = None,
        title: str | None = None,
        user_id: str | None = None,
        application_id: str | None = None,
        model_group: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, **kwargs}
        if question is not None:
            body["question"] = question
        if action is not None:
            body["action"] = action
        if id is not None:
            body["id"] = id
        if preset is not None:
            body["preset"] = preset
        if stateful is not None:
            body["stateful"] = stateful
        if references is not None:
            body["references"] = references
        if max_turns is not None:
            body["max_turns"] = max_turns
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


class AsyncAiChat:
    """Async AI chat client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: str,
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

    async def create2(
        self,
        *,
        model: str,
        question: str | None = None,
        action: Literal["chat", "retrieve", "retrieve_batch", "update", "delete"] | None = None,
        id: str | None = None,
        preset: str | None = None,
        stateful: bool | None = None,
        references: list[Any] | None = None,
        max_turns: int | None = None,
        tool_results: list[Any] | None = None,
        messages: list[Any] | None = None,
        title: str | None = None,
        user_id: str | None = None,
        application_id: str | None = None,
        model_group: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, **kwargs}
        if question is not None:
            body["question"] = question
        if action is not None:
            body["action"] = action
        if id is not None:
            body["id"] = id
        if preset is not None:
            body["preset"] = preset
        if stateful is not None:
            body["stateful"] = stateful
        if references is not None:
            body["references"] = references
        if max_turns is not None:
            body["max_turns"] = max_turns
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
