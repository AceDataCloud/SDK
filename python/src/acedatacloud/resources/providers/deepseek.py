"""Deepseek (deepseek) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

DeepseekModel = Literal[
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v3.2-exp",
    "deepseek-v4-flash",
    "deepseek-v4-pro",
]
DeepseekReasoningEffort = Literal[
    "minimal",
    "low",
    "medium",
    "high",
]
DeepseekServiceTier = Literal[
    "auto",
    "default",
    "flex",
    "scale",
    "priority",
]


def _task_id(result: Any) -> str:
    """Task ids appear at the top level or nested under `data`."""
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


class Deepseek:
    """Synchronous deepseek client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def completions(
        self,
        *,
        model: DeepseekModel,
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool | None = None,
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
        reasoning_effort: DeepseekReasoningEffort | None = None,
        service_tier: DeepseekServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Deepseek Chat Completions"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["messages"] = messages
        body["n"] = n if n is not None else 1
        body["stream"] = stream if stream is not None else False
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        body["temperature"] = temperature if temperature is not None else 1
        if response_format is not None:
            body["response_format"] = response_format
        body["top_p"] = top_p if top_p is not None else 1
        body["frequency_penalty"] = frequency_penalty if frequency_penalty is not None else 0
        body["presence_penalty"] = presence_penalty if presence_penalty is not None else 0
        if seed is not None:
            body["seed"] = seed
        if stop is not None:
            body["stop"] = stop
        if max_completion_tokens is not None:
            body["max_completion_tokens"] = max_completion_tokens
        body["logprobs"] = logprobs if logprobs is not None else False
        if top_logprobs is not None:
            body["top_logprobs"] = top_logprobs
        if stream_options is not None:
            body["stream_options"] = stream_options
        body["parallel_tool_calls"] = parallel_tool_calls if parallel_tool_calls is not None else True
        if user is not None:
            body["user"] = user
        body["reasoning_effort"] = reasoning_effort if reasoning_effort is not None else "medium"
        body["service_tier"] = service_tier if service_tier is not None else "auto"
        body["store"] = store if store is not None else False
        if metadata is not None:
            body["metadata"] = metadata
        if logit_bias is not None:
            body["logit_bias"] = logit_bias
        if modalities is not None:
            body["modalities"] = modalities
        if audio is not None:
            body["audio"] = audio
        if prediction is not None:
            body["prediction"] = prediction
        if web_search_options is not None:
            body["web_search_options"] = web_search_options
        if tools is not None:
            body["tools"] = tools
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/deepseek/chat/completions", json=body)


class AsyncDeepseek:
    """Asynchronous deepseek client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def completions(
        self,
        *,
        model: DeepseekModel,
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool | None = None,
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
        reasoning_effort: DeepseekReasoningEffort | None = None,
        service_tier: DeepseekServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Deepseek Chat Completions"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["messages"] = messages
        body["n"] = n if n is not None else 1
        body["stream"] = stream if stream is not None else False
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        body["temperature"] = temperature if temperature is not None else 1
        if response_format is not None:
            body["response_format"] = response_format
        body["top_p"] = top_p if top_p is not None else 1
        body["frequency_penalty"] = frequency_penalty if frequency_penalty is not None else 0
        body["presence_penalty"] = presence_penalty if presence_penalty is not None else 0
        if seed is not None:
            body["seed"] = seed
        if stop is not None:
            body["stop"] = stop
        if max_completion_tokens is not None:
            body["max_completion_tokens"] = max_completion_tokens
        body["logprobs"] = logprobs if logprobs is not None else False
        if top_logprobs is not None:
            body["top_logprobs"] = top_logprobs
        if stream_options is not None:
            body["stream_options"] = stream_options
        body["parallel_tool_calls"] = parallel_tool_calls if parallel_tool_calls is not None else True
        if user is not None:
            body["user"] = user
        body["reasoning_effort"] = reasoning_effort if reasoning_effort is not None else "medium"
        body["service_tier"] = service_tier if service_tier is not None else "auto"
        body["store"] = store if store is not None else False
        if metadata is not None:
            body["metadata"] = metadata
        if logit_bias is not None:
            body["logit_bias"] = logit_bias
        if modalities is not None:
            body["modalities"] = modalities
        if audio is not None:
            body["audio"] = audio
        if prediction is not None:
            body["prediction"] = prediction
        if web_search_options is not None:
            body["web_search_options"] = web_search_options
        if tools is not None:
            body["tools"] = tools
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/deepseek/chat/completions", json=body)
