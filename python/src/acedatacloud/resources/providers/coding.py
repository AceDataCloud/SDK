"""Coding (coding) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

CodingCountTokensModel = Literal[
    "claude-fable-5-1",
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
]
CodingMessagesModel = Literal[
    "claude-fable-5-1",
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
]
CodingCompletionsModel = Literal[
    "gpt-6-astra",
    "gpt-oss:free",
    "gpt-5.5:free",
    "gpt-5:free",
    "gpt-4.1:free",
    "gpt-4o:free",
    "gpt-4o-mini:free",
    "gpt-5.6-luna",
    "gpt-5.6-terra",
    "gpt-5.6-sol",
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.4-mini",
    "gpt-5.4-nano",
    "gpt-5.4-pro",
    "gpt-5.2",
    "gpt-5.1",
    "gpt-5.1-all",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-all",
    "gpt-4o-image",
    "gpt-4o-mini",
    "gpt-35-turbo-16k",
    "o1",
    "o1-mini",
    "o1-pro",
    "o3",
    "o3-mini",
    "o3-pro",
    "o4-mini",
]
CodingCompletionsReasoningEffort = Literal[
    "minimal",
    "low",
    "medium",
    "high",
]
CodingServiceTier = Literal[
    "auto",
    "default",
    "flex",
    "scale",
    "priority",
]
CodingV1ChatCompletionsModel = Literal[
    "claude-fable-5-1",
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
]
CodingV1ChatCompletionsReasoningEffort = Literal[
    "minimal",
    "low",
    "medium",
    "high",
]
CodingDeepseekChatCompletionsModel = Literal[
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v3.2-exp",
    "deepseek-v4-flash",
    "deepseek-v4-pro",
]
CodingDeepseekChatCompletionsReasoningEffort = Literal[
    "minimal",
    "low",
    "medium",
    "high",
]
CodingGlmChatCompletionsModel = Literal[
    "glm-5.3",
    "glm-5.2",
    "glm-5",
    "glm-5-turbo",
    "glm-5.1",
    "glm-4.7",
    "glm-4.6",
    "glm-3-turbo",
]
CodingGlmChatCompletionsReasoningEffort = Literal[
    "minimal",
    "low",
    "medium",
    "high",
]
CodingGeminiChatCompletionsModel = Literal[
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
CodingGeminiChatCompletionsReasoningEffort = Literal[
    "minimal",
    "low",
    "medium",
    "high",
]
CodingGrokChatCompletionsReasoningEffort = Literal[
    "minimal",
    "low",
    "medium",
    "high",
]
CodingKimiChatCompletionsModel = Literal[
    "kimi-k3",
    "kimi-k2.6",
    "kimi-k2-thinking-turbo",
    "kimi-k2.5",
    "kimi-k2-thinking",
]
CodingResponsesModel = Literal[
    "gpt-6-astra",
    "gpt-5.6-luna",
    "gpt-5.6-terra",
    "gpt-5.6-sol",
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.4-mini",
    "gpt-5.4-nano",
    "gpt-5.4-pro",
    "gpt-5.1",
    "gpt-5.1-all",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
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
    "gpt-35-turbo-16k",
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


class Coding:
    """Synchronous coding client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def count_tokens(
        self,
        *,
        model: CodingCountTokensModel,
        messages: list[dict[str, Any]],
        system: str | list[str] | None = None,
        thinking: dict[str, Any] | None = None,
        tool_choice: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        cache_control: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Claude Messages Count Tokens"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["messages"] = messages
        if system is not None:
            body["system"] = system
        if thinking is not None:
            body["thinking"] = thinking
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        if tools is not None:
            body["tools"] = tools
        if cache_control is not None:
            body["cache_control"] = cache_control
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/v1/messages/count_tokens", json=body)

    def messages(
        self,
        *,
        model: CodingMessagesModel,
        messages: list[dict[str, Any]],
        max_tokens: int,
        metadata: dict[str, Any] | None = None,
        stop_sequences: list[str] | None = None,
        stream: bool | None = None,
        system: str | list[str] | None = None,
        temperature: float | None = None,
        tool_choice: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
        thinking: dict[str, Any] | None = None,
        output_config: dict[str, Any] | None = None,
        cache_control: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Claude Messages"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["messages"] = messages
        body["max_tokens"] = max_tokens
        if metadata is not None:
            body["metadata"] = metadata
        if stop_sequences is not None:
            body["stop_sequences"] = stop_sequences
        body["stream"] = stream if stream is not None else False
        if system is not None:
            body["system"] = system
        if temperature is not None:
            body["temperature"] = temperature
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        if tools is not None:
            body["tools"] = tools
        if top_k is not None:
            body["top_k"] = top_k
        if top_p is not None:
            body["top_p"] = top_p
        if thinking is not None:
            body["thinking"] = thinking
        if output_config is not None:
            body["output_config"] = output_config
        if cache_control is not None:
            body["cache_control"] = cache_control
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/v1/messages", json=body)

    def completions(
        self,
        *,
        model: CodingCompletionsModel,
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool | None = None,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
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
        reasoning_effort: CodingCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Openai Chat Completions"""
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
        if tools is not None:
            body["tools"] = tools
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
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
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/openai/chat/completions", json=body)

    def v1_chat_completions(
        self,
        *,
        model: CodingV1ChatCompletionsModel,
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
        reasoning_effort: CodingV1ChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
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
        """Claude Chat Completions"""
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
        return self._transport.request("POST", "/v1/chat/completions", json=body)

    def deepseek_chat_completions(
        self,
        *,
        model: CodingDeepseekChatCompletionsModel,
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
        reasoning_effort: CodingDeepseekChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
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

    def glm_chat_completions(
        self,
        *,
        model: CodingGlmChatCompletionsModel,
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
        reasoning_effort: CodingGlmChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
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
        """Glm Chat Completions"""
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
        return self._transport.request("POST", "/glm/chat/completions", json=body)

    def gemini_chat_completions(
        self,
        *,
        model: CodingGeminiChatCompletionsModel,
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
        reasoning_effort: CodingGeminiChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
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
        """Gemini Chat Completions"""
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
        return self._transport.request("POST", "/gemini/chat/completions", json=body)

    def grok_chat_completions(
        self,
        *,
        model: Literal["grok-4.5", "grok-4", "grok-3"],
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool | None = None,
        max_tokens: float | None = None,
        temperature: float | None = None,
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
        reasoning_effort: CodingGrokChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
        response_format: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Grok Chat Completions"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["messages"] = messages
        body["n"] = n if n is not None else 1
        body["stream"] = stream if stream is not None else False
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        body["temperature"] = temperature if temperature is not None else 1
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
        if response_format is not None:
            body["response_format"] = response_format
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/grok/chat/completions", json=body)

    def kimi_chat_completions(
        self,
        *,
        model: CodingKimiChatCompletionsModel,
        messages: list[dict[str, Any]],
        n: int | None = None,
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
        reasoning_effort: Literal["low", "high", "max"] | None = None,
        service_tier: CodingServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
        thinking: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Kimi Chat Completions"""
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
        if reasoning_effort is not None:
            body["reasoning_effort"] = reasoning_effort
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
        if thinking is not None:
            body["thinking"] = thinking
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/kimi/chat/completions", json=body)

    def responses(
        self,
        *,
        model: CodingResponsesModel,
        input: str | list[str],
        n: float | None = None,
        background: bool | None = None,
        stream: bool | None = None,
        tools: list[dict[str, Any]] | None = None,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        include: list[str] | None = None,
        reasoning: dict[str, Any] | None = None,
        text: dict[str, Any] | None = None,
        max_output_tokens: int | None = None,
        store: bool | None = None,
        stream_options: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Openai V1 Responses"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["input"] = input
        body["n"] = n if n is not None else 1
        body["background"] = background if background is not None else False
        body["stream"] = stream if stream is not None else False
        if tools is not None:
            body["tools"] = tools
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        body["temperature"] = temperature if temperature is not None else 1
        if response_format is not None:
            body["response_format"] = response_format
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        body["parallel_tool_calls"] = parallel_tool_calls if parallel_tool_calls is not None else True
        if include is not None:
            body["include"] = include
        if reasoning is not None:
            body["reasoning"] = reasoning
        if text is not None:
            body["text"] = text
        if max_output_tokens is not None:
            body["max_output_tokens"] = max_output_tokens
        body["store"] = store if store is not None else True
        if stream_options is not None:
            body["stream_options"] = stream_options
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/openai/responses", json=body)


class AsyncCoding:
    """Asynchronous coding client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def count_tokens(
        self,
        *,
        model: CodingCountTokensModel,
        messages: list[dict[str, Any]],
        system: str | list[str] | None = None,
        thinking: dict[str, Any] | None = None,
        tool_choice: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        cache_control: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Claude Messages Count Tokens"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["messages"] = messages
        if system is not None:
            body["system"] = system
        if thinking is not None:
            body["thinking"] = thinking
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        if tools is not None:
            body["tools"] = tools
        if cache_control is not None:
            body["cache_control"] = cache_control
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/v1/messages/count_tokens", json=body)

    async def messages(
        self,
        *,
        model: CodingMessagesModel,
        messages: list[dict[str, Any]],
        max_tokens: int,
        metadata: dict[str, Any] | None = None,
        stop_sequences: list[str] | None = None,
        stream: bool | None = None,
        system: str | list[str] | None = None,
        temperature: float | None = None,
        tool_choice: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
        thinking: dict[str, Any] | None = None,
        output_config: dict[str, Any] | None = None,
        cache_control: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Claude Messages"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["messages"] = messages
        body["max_tokens"] = max_tokens
        if metadata is not None:
            body["metadata"] = metadata
        if stop_sequences is not None:
            body["stop_sequences"] = stop_sequences
        body["stream"] = stream if stream is not None else False
        if system is not None:
            body["system"] = system
        if temperature is not None:
            body["temperature"] = temperature
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        if tools is not None:
            body["tools"] = tools
        if top_k is not None:
            body["top_k"] = top_k
        if top_p is not None:
            body["top_p"] = top_p
        if thinking is not None:
            body["thinking"] = thinking
        if output_config is not None:
            body["output_config"] = output_config
        if cache_control is not None:
            body["cache_control"] = cache_control
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/v1/messages", json=body)

    async def completions(
        self,
        *,
        model: CodingCompletionsModel,
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool | None = None,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
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
        reasoning_effort: CodingCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Openai Chat Completions"""
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
        if tools is not None:
            body["tools"] = tools
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
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
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/openai/chat/completions", json=body)

    async def v1_chat_completions(
        self,
        *,
        model: CodingV1ChatCompletionsModel,
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
        reasoning_effort: CodingV1ChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
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
        """Claude Chat Completions"""
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
        return await self._transport.request("POST", "/v1/chat/completions", json=body)

    async def deepseek_chat_completions(
        self,
        *,
        model: CodingDeepseekChatCompletionsModel,
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
        reasoning_effort: CodingDeepseekChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
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

    async def glm_chat_completions(
        self,
        *,
        model: CodingGlmChatCompletionsModel,
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
        reasoning_effort: CodingGlmChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
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
        """Glm Chat Completions"""
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
        return await self._transport.request("POST", "/glm/chat/completions", json=body)

    async def gemini_chat_completions(
        self,
        *,
        model: CodingGeminiChatCompletionsModel,
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
        reasoning_effort: CodingGeminiChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
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
        """Gemini Chat Completions"""
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
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)

    async def grok_chat_completions(
        self,
        *,
        model: Literal["grok-4.5", "grok-4", "grok-3"],
        messages: list[dict[str, Any]],
        n: float | None = None,
        stream: bool | None = None,
        max_tokens: float | None = None,
        temperature: float | None = None,
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
        reasoning_effort: CodingGrokChatCompletionsReasoningEffort | None = None,
        service_tier: CodingServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
        response_format: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Grok Chat Completions"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["messages"] = messages
        body["n"] = n if n is not None else 1
        body["stream"] = stream if stream is not None else False
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        body["temperature"] = temperature if temperature is not None else 1
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
        if response_format is not None:
            body["response_format"] = response_format
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/grok/chat/completions", json=body)

    async def kimi_chat_completions(
        self,
        *,
        model: CodingKimiChatCompletionsModel,
        messages: list[dict[str, Any]],
        n: int | None = None,
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
        reasoning_effort: Literal["low", "high", "max"] | None = None,
        service_tier: CodingServiceTier | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
        thinking: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Kimi Chat Completions"""
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
        if reasoning_effort is not None:
            body["reasoning_effort"] = reasoning_effort
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
        if thinking is not None:
            body["thinking"] = thinking
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/kimi/chat/completions", json=body)

    async def responses(
        self,
        *,
        model: CodingResponsesModel,
        input: str | list[str],
        n: float | None = None,
        background: bool | None = None,
        stream: bool | None = None,
        tools: list[dict[str, Any]] | None = None,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
        tool_choice: Literal["none", "auto", "required"] | dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        include: list[str] | None = None,
        reasoning: dict[str, Any] | None = None,
        text: dict[str, Any] | None = None,
        max_output_tokens: int | None = None,
        store: bool | None = None,
        stream_options: dict[str, Any] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Openai V1 Responses"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["input"] = input
        body["n"] = n if n is not None else 1
        body["background"] = background if background is not None else False
        body["stream"] = stream if stream is not None else False
        if tools is not None:
            body["tools"] = tools
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        body["temperature"] = temperature if temperature is not None else 1
        if response_format is not None:
            body["response_format"] = response_format
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        body["parallel_tool_calls"] = parallel_tool_calls if parallel_tool_calls is not None else True
        if include is not None:
            body["include"] = include
        if reasoning is not None:
            body["reasoning"] = reasoning
        if text is not None:
            body["text"] = text
        if max_output_tokens is not None:
            body["max_output_tokens"] = max_output_tokens
        body["store"] = store if store is not None else True
        if stream_options is not None:
            body["stream_options"] = stream_options
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/openai/responses", json=body)
