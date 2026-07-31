"""Grok (grok) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from collections.abc import Iterator  # noqa: F401
from typing import Any, Literal

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

GrokChatModel = Literal[
    "grok-4.5",
    "grok-4",
    "grok-3",
]
GrokVideoModel = Literal[
    "grok-imagine-video-1.5-fast:reverse",
    "grok-imagine-video:reverse",
    "grok-imagine-video:official",
    "grok-imagine-video-1.5:official",
    "grok-imagine-video",
]
GrokAspectRatio = Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]
GrokResolution = Literal["480p", "720p", "1080p"]


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


class _GrokChat:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    @property
    def completions(self) -> _GrokChatCompletions:
        return _GrokChatCompletions(self._transport)


class _GrokChatCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: GrokChatModel,
        messages: list[dict[str, Any]],
        stream: bool | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: float | None = None,
        max_completion_tokens: int | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        n: float | None = None,
        stop: Any | None = None,
        seed: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        stream_options: dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        user: str | None = None,
        reasoning_effort: Literal["minimal", "low", "medium", "high"] | None = None,
        service_tier: Literal["auto", "default", "flex", "scale", "priority"] | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[Any] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[Any] | None = None,
        tool_choice: Any | None = None,
        response_format: dict[str, Any] | None = None,
        **extra: Any,
    ) -> Any:
        """Grok chat completions. Supports streaming."""
        body: dict[str, Any] = {"model": model, "messages": messages}
        if stream is not None:
            body["stream"] = stream
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["top_p"] = top_p
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if max_completion_tokens is not None:
            body["max_completion_tokens"] = max_completion_tokens
        if frequency_penalty is not None:
            body["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            body["presence_penalty"] = presence_penalty
        if n is not None:
            body["n"] = n
        if stop is not None:
            body["stop"] = stop
        if seed is not None:
            body["seed"] = seed
        if logprobs is not None:
            body["logprobs"] = logprobs
        if top_logprobs is not None:
            body["top_logprobs"] = top_logprobs
        if stream_options is not None:
            body["stream_options"] = stream_options
        if parallel_tool_calls is not None:
            body["parallel_tool_calls"] = parallel_tool_calls
        if user is not None:
            body["user"] = user
        if reasoning_effort is not None:
            body["reasoning_effort"] = reasoning_effort
        if service_tier is not None:
            body["service_tier"] = service_tier
        if store is not None:
            body["store"] = store
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
        return self._transport.request("POST", "/grok/chat/completions", json=body)


class _GrokVideos:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str | None = None,
        model: GrokVideoModel | None = None,
        image_url: str | None = None,
        reference_image_urls: list[str] | None = None,
        aspect_ratio: GrokAspectRatio | None = None,
        resolution: GrokResolution | None = None,
        duration: int | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Grok video generation API."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if model is not None:
            body["model"] = model
        if image_url is not None:
            body["image_url"] = image_url
        if reference_image_urls is not None:
            body["reference_image_urls"] = reference_image_urls
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if resolution is not None:
            body["resolution"] = resolution
        if duration is not None:
            body["duration"] = duration
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/grok/videos", json=body)
        handle = TaskHandle(_task_id(result), "/grok/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class Grok:
    """Synchronous grok client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _GrokChat(transport)
        self.videos = _GrokVideos(transport)


class _AsyncGrokChat:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    @property
    def completions(self) -> _AsyncGrokChatCompletions:
        return _AsyncGrokChatCompletions(self._transport)


class _AsyncGrokChatCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: GrokChatModel,
        messages: list[dict[str, Any]],
        stream: bool | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: float | None = None,
        max_completion_tokens: int | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        n: float | None = None,
        stop: Any | None = None,
        seed: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        stream_options: dict[str, Any] | None = None,
        parallel_tool_calls: bool | None = None,
        user: str | None = None,
        reasoning_effort: Literal["minimal", "low", "medium", "high"] | None = None,
        service_tier: Literal["auto", "default", "flex", "scale", "priority"] | None = None,
        store: bool | None = None,
        metadata: dict[str, Any] | None = None,
        logit_bias: dict[str, Any] | None = None,
        modalities: list[Any] | None = None,
        audio: dict[str, Any] | None = None,
        prediction: dict[str, Any] | None = None,
        web_search_options: dict[str, Any] | None = None,
        tools: list[Any] | None = None,
        tool_choice: Any | None = None,
        response_format: dict[str, Any] | None = None,
        **extra: Any,
    ) -> Any:
        """Grok chat completions. Supports streaming."""
        body: dict[str, Any] = {"model": model, "messages": messages}
        if stream is not None:
            body["stream"] = stream
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["top_p"] = top_p
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if max_completion_tokens is not None:
            body["max_completion_tokens"] = max_completion_tokens
        if frequency_penalty is not None:
            body["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            body["presence_penalty"] = presence_penalty
        if n is not None:
            body["n"] = n
        if stop is not None:
            body["stop"] = stop
        if seed is not None:
            body["seed"] = seed
        if logprobs is not None:
            body["logprobs"] = logprobs
        if top_logprobs is not None:
            body["top_logprobs"] = top_logprobs
        if stream_options is not None:
            body["stream_options"] = stream_options
        if parallel_tool_calls is not None:
            body["parallel_tool_calls"] = parallel_tool_calls
        if user is not None:
            body["user"] = user
        if reasoning_effort is not None:
            body["reasoning_effort"] = reasoning_effort
        if service_tier is not None:
            body["service_tier"] = service_tier
        if store is not None:
            body["store"] = store
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
        return await self._transport.request("POST", "/grok/chat/completions", json=body)


class _AsyncGrokVideos:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str | None = None,
        model: GrokVideoModel | None = None,
        image_url: str | None = None,
        reference_image_urls: list[str] | None = None,
        aspect_ratio: GrokAspectRatio | None = None,
        resolution: GrokResolution | None = None,
        duration: int | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Grok video generation API."""
        body: dict[str, Any] = {}
        if prompt is not None:
            body["prompt"] = prompt
        if model is not None:
            body["model"] = model
        if image_url is not None:
            body["image_url"] = image_url
        if reference_image_urls is not None:
            body["reference_image_urls"] = reference_image_urls
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if resolution is not None:
            body["resolution"] = resolution
        if duration is not None:
            body["duration"] = duration
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/grok/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/grok/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncGrok:
    """Asynchronous grok client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncGrokChat(transport)
        self.videos = _AsyncGrokVideos(transport)
