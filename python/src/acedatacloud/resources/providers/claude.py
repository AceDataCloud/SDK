"""Claude (claude) provider resource."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

ClaudeModel = Literal[
    "claude-fable-5",
    "claude-opus-5",
    "claude-opus-4-8",
    "claude-sonnet-5",
    "claude-sonnet-4-6",
    "claude-opus-4-7",
    "claude-opus-4-6",
    "claude-opus-4-5-20251101",
    "claude-haiku-4-5-20251001",
    "claude-sonnet-4-5-20250929",
    "claude-opus-4-1-20250805",
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514",
    "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
]


def _add_present(body: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    for key, value in values.items():
        if value is not None:
            body[key] = value
    return body


def _completion_body(
    *,
    model: ClaudeModel,
    messages: list[dict[str, Any]],
    n: float | None = 1,
    stream: bool = False,
    max_tokens: float | None = None,
    temperature: float | None = 1,
    response_format: Any | None = None,
    top_p: float | None = 1,
    frequency_penalty: float | None = 0,
    presence_penalty: float | None = 0,
    seed: int | None = None,
    stop: Any | None = None,
    max_completion_tokens: int | None = None,
    logprobs: bool | None = False,
    top_logprobs: int | None = None,
    stream_options: dict[str, Any] | None = None,
    parallel_tool_calls: bool | None = True,
    user: str | None = None,
    reasoning_effort: Literal["minimal", "low", "medium", "high"] | None = "medium",
    service_tier: Literal["auto", "default", "flex", "scale", "priority"] | None = "auto",
    store: bool | None = False,
    metadata: dict[str, Any] | None = None,
    logit_bias: dict[str, Any] | None = None,
    modalities: list[Any] | None = None,
    audio: dict[str, Any] | None = None,
    prediction: dict[str, Any] | None = None,
    web_search_options: dict[str, Any] | None = None,
    tools: list[Any] | None = None,
    tool_choice: Any | None = None,
    **extra: Any,
) -> dict[str, Any]:
    body: dict[str, Any] = {"model": model, "messages": messages, **extra, "stream": stream}
    return _add_present(
        body,
        {
            "n": n,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "response_format": response_format,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "seed": seed,
            "stop": stop,
            "max_completion_tokens": max_completion_tokens,
            "logprobs": logprobs,
            "top_logprobs": top_logprobs,
            "stream_options": stream_options,
            "parallel_tool_calls": parallel_tool_calls,
            "user": user,
            "reasoning_effort": reasoning_effort,
            "service_tier": service_tier,
            "store": store,
            "metadata": metadata,
            "logit_bias": logit_bias,
            "modalities": modalities,
            "audio": audio,
            "prediction": prediction,
            "web_search_options": web_search_options,
            "tools": tools,
            "tool_choice": tool_choice,
        },
    )


def _messages_body(
    *,
    model: ClaudeModel,
    messages: list[dict[str, Any]],
    max_tokens: int,
    metadata: dict[str, Any] | None = None,
    stop_sequences: list[str] | None = None,
    stream: bool = False,
    system: str | None = None,
    temperature: float | None = None,
    tool_choice: dict[str, Any] | None = None,
    tools: list[Any] | None = None,
    top_k: int | None = None,
    top_p: float | None = None,
    thinking: Any | None = None,
    **extra: Any,
) -> dict[str, Any]:
    body: dict[str, Any] = {"model": model, "messages": messages, "max_tokens": max_tokens, **extra, "stream": stream}
    return _add_present(
        body,
        {
            "metadata": metadata,
            "stop_sequences": stop_sequences,
            "system": system,
            "temperature": temperature,
            "tool_choice": tool_choice,
            "tools": tools,
            "top_k": top_k,
            "top_p": top_p,
            "thinking": thinking,
        },
    )


def _count_tokens_body(
    *,
    model: ClaudeModel,
    messages: list[dict[str, Any]],
    system: str | None = None,
    thinking: dict[str, Any] | None = None,
    tool_choice: dict[str, Any] | None = None,
    tools: list[Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    return _add_present(
        {"model": model, "messages": messages, **extra},
        {"system": system, "thinking": thinking, "tool_choice": tool_choice, "tools": tools},
    )


class _ClaudeChatCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(self, **kwargs: Any) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = _completion_body(**kwargs)
        if body["stream"]:
            return self._stream(body)
        return self._transport.request("POST", "/v1/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/v1/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncClaudeChatCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(self, **kwargs: Any) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = _completion_body(**kwargs)
        if body["stream"]:
            return self._stream(body)
        return await self._transport.request("POST", "/v1/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]):
        async for chunk in self._transport.request_stream("POST", "/v1/chat/completions", json=body):
            yield _json.loads(chunk)


class _ClaudeChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _ClaudeChatCompletions(transport)


class _AsyncClaudeChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncClaudeChatCompletions(transport)


class _ClaudeMessages:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(self, **kwargs: Any) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = _messages_body(**kwargs)
        if body["stream"]:
            return self._stream(body)
        return self._transport.request("POST", "/v1/messages", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/v1/messages", json=body):
            yield _json.loads(chunk)

    def count_tokens(self, **kwargs: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/v1/messages/count_tokens", json=_count_tokens_body(**kwargs))


class _AsyncClaudeMessages:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(self, **kwargs: Any) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = _messages_body(**kwargs)
        if body["stream"]:
            return self._stream(body)
        return await self._transport.request("POST", "/v1/messages", json=body)

    async def _stream(self, body: dict[str, Any]):
        async for chunk in self._transport.request_stream("POST", "/v1/messages", json=body):
            yield _json.loads(chunk)

    async def count_tokens(self, **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/v1/messages/count_tokens", json=_count_tokens_body(**kwargs))


class Claude:
    """Synchronous Claude client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _ClaudeChat(transport)
        self.messages = _ClaudeMessages(transport)


class AsyncClaude:
    """Asynchronous Claude client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncClaudeChat(transport)
        self.messages = _AsyncClaudeMessages(transport)
