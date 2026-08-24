"""GLM chat completions resource."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

GlmModel = Literal[
    "glm-5.3",
    "glm-5.2",
    "glm-5",
    "glm-5-turbo",
    "glm-5.1",
    "glm-4.7",
    "glm-4.6",
    "glm-3-turbo",
]

GlmReasoningEffort = Literal["minimal", "low", "medium", "high"]
GlmServiceTier = Literal["auto", "default", "flex", "scale", "priority"]


def _build_body(required: dict[str, Any], optional: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    body = {**required, **extra}
    for key, value in optional.items():
        if value is not None:
            body[key] = value
    return body


class _Completions:
    """Namespace for glm.chat.completions."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: GlmModel,
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool = False,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        seed: int | None = None,
        stop: str | list[str] | None = None,
        max_completion_tokens: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        stream_options: dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        user: str | None = None,
        reasoning_effort: GlmReasoningEffort | None = None,
        service_tier: GlmServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, str] | None = None,
        logit_bias: dict[str, int] | None = None,
        modalities: list[Literal["text", "audio"]] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = _build_body(
            {"model": model, "messages": messages},
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
            kwargs,
        )
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/glm/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/glm/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: GlmModel,
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool = False,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        seed: int | None = None,
        stop: str | list[str] | None = None,
        max_completion_tokens: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        stream_options: dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        user: str | None = None,
        reasoning_effort: GlmReasoningEffort | None = None,
        service_tier: GlmServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, str] | None = None,
        logit_bias: dict[str, int] | None = None,
        modalities: list[Literal["text", "audio"]] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = _build_body(
            {"model": model, "messages": messages},
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
            kwargs,
        )
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/glm/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", "/glm/chat/completions", json=body):
            yield _json.loads(chunk)


class _ChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _AsyncChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class Glm:
    """Synchronous GLM client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _ChatNamespace(transport)


class AsyncGlm:
    """Async GLM client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncChatNamespace(transport)
