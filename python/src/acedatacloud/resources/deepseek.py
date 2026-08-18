"""DeepSeek chat completions resource."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

DeepseekModel = Literal[
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v3.2-exp",
    "deepseek-v4-flash",
    "deepseek-v4-pro",
]
DeepseekReasoningEffort = Literal["minimal", "low", "medium", "high"]
DeepseekServiceTier = Literal["auto", "default", "flex", "scale", "priority"]
DeepseekModality = Literal["text", "audio"]


def _set_if_not_none(body: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        body[key] = value


class _Completions:
    """Namespace for deepseek.chat.completions."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: DeepseekModel,
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool = False,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: Any | None = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        seed: int | None = None,
        stop: Any | None = None,
        max_completion_tokens: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        stream_options: dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        user: str | None = None,
        reasoning_effort: DeepseekReasoningEffort | None = None,
        service_tier: DeepseekServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[DeepseekModality] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Any | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        for key, value in {
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
        }.items():
            _set_if_not_none(body, key, value)
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/deepseek/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/deepseek/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: DeepseekModel,
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool = False,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: Any | None = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        seed: int | None = None,
        stop: Any | None = None,
        max_completion_tokens: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        stream_options: dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        user: str | None = None,
        reasoning_effort: DeepseekReasoningEffort | None = None,
        service_tier: DeepseekServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[DeepseekModality] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Any | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        for key, value in {
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
        }.items():
            _set_if_not_none(body, key, value)
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/deepseek/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", "/deepseek/chat/completions", json=body):
            yield _json.loads(chunk)


class _ChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _AsyncChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class Deepseek:
    """Synchronous DeepSeek client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _ChatNamespace(transport)


class AsyncDeepseek:
    """Async DeepSeek client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncChatNamespace(transport)
