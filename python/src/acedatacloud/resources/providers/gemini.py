"""Gemini (gemini) provider resource."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal
from urllib.parse import quote

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

GeminiChatModel = Literal[
    "gemini-3.1-pro",
    "gemini-3.0-pro",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-3.1-flash-lite-preview",
]
GeminiNativeModel = Literal[
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-3-flash-preview",
    "gemini-3.5-flash",
    "gemini-3.0-pro",
    "gemini-3.1-pro",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-flash-image",
    "gemini-2.5-flash-image",
    "gemini-3-pro-image",
]
GeminiVideoModel = Literal["omni-flash"]


def _task_id(result: Any) -> str:
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


def _content_body(
    *,
    contents: list[dict[str, Any]],
    system_instruction: dict[str, Any] | None = None,
    generation_config: dict[str, Any] | None = None,
    tools: list[Any] | None = None,
    tool_config: dict[str, Any] | None = None,
    safety_settings: list[Any] | None = None,
    cached_content: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    body: dict[str, Any] = {"contents": contents, **extra}
    for key, value in {
        "systemInstruction": system_instruction,
        "generationConfig": generation_config,
        "tools": tools,
        "toolConfig": tool_config,
        "safetySettings": safety_settings,
        "cachedContent": cached_content,
    }.items():
        if value is not None:
            body[key] = value
    return body


class _GeminiChatCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: GeminiChatModel,
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
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body: dict[str, Any] = {"model": model, "messages": messages, **extra}
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
            if value is not None:
                body[key] = value
        if stream:
            body["stream"] = True
            return self._stream(body)
        body["stream"] = False
        return self._transport.request("POST", "/gemini/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _GeminiChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _GeminiChatCompletions(transport)


class _GeminiVideos:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        model: GeminiVideoModel | None = None,
        aspect_ratio: Literal["16:9", "9:16"] | None = None,
        resolution: Literal["720p", "1080p"] | None = None,
        image_urls: list[str] | None = None,
        video_urls: list[str] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **extra}
        body["model"] = model if model is not None else "omni-flash"
        body["aspect_ratio"] = aspect_ratio if aspect_ratio is not None else "16:9"
        body["resolution"] = resolution if resolution is not None else "720p"
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_urls is not None:
            body["video_urls"] = video_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/gemini/videos", json=body)
        handle = TaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class Gemini:
    """Synchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _GeminiChat(transport)
        self.videos = _GeminiVideos(transport)

    def generate_content(
        self, *, model: GeminiNativeModel, contents: list[dict[str, Any]], **kwargs: Any
    ) -> dict[str, Any]:
        path = f"/v1beta/models/{quote(model, safe='')}:generateContent"
        return self._transport.request("POST", path, json=_content_body(contents=contents, **kwargs))

    def stream_generate_content(
        self, *, model: GeminiNativeModel, contents: list[dict[str, Any]], **kwargs: Any
    ) -> Iterator[dict[str, Any]]:
        path = f"/v1beta/models/{quote(model, safe='')}:streamGenerateContent?alt=sse"
        body = _content_body(contents=contents, **kwargs)
        for chunk in self._transport.request_stream("POST", path, json=body):
            yield _json.loads(chunk)


class AsyncGemini:
    """Asynchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncGeminiChat(transport)
        self.videos = _AsyncGeminiVideos(transport)

    async def generate_content(
        self, *, model: GeminiNativeModel, contents: list[dict[str, Any]], **kwargs: Any
    ) -> dict[str, Any]:
        path = f"/v1beta/models/{quote(model, safe='')}:generateContent"
        return await self._transport.request("POST", path, json=_content_body(contents=contents, **kwargs))

    async def stream_generate_content(
        self, *, model: GeminiNativeModel, contents: list[dict[str, Any]], **kwargs: Any
    ) -> AsyncIterator[dict[str, Any]]:
        path = f"/v1beta/models/{quote(model, safe='')}:streamGenerateContent?alt=sse"
        body = _content_body(contents=contents, **kwargs)
        async for chunk in self._transport.request_stream("POST", path, json=body):
            yield _json.loads(chunk)


class _AsyncGeminiChatCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(self, **kwargs: Any) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        stream = bool(kwargs.pop("stream", False))
        if stream:
            body = _CaptureBody.from_chat(_GeminiChatCompletions, kwargs, stream=True)
            return self._stream(body)
        body = _CaptureBody.from_chat(_GeminiChatCompletions, kwargs, stream=False)
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]):
        async for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncGeminiChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncGeminiChatCompletions(transport)


class _AsyncGeminiVideos(_GeminiVideos):
    async def generate(self, **kwargs: Any) -> AsyncTaskHandle:
        wait = bool(kwargs.pop("wait", False))
        poll_interval = float(kwargs.pop("poll_interval", 3.0))
        max_wait = float(kwargs.pop("max_wait", 600.0))
        capture = _CaptureTransport()
        _GeminiVideos(capture).generate(wait=False, **kwargs)
        result = await self._transport.request("POST", "/gemini/videos", json=capture.body)
        handle = AsyncTaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _CaptureTransport:
    body: dict[str, Any]

    def request(self, _method: str, _path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.body = json
        return {}


class _CaptureBody:
    @staticmethod
    def from_chat(cls: type[_GeminiChatCompletions], kwargs: dict[str, Any], *, stream: bool) -> dict[str, Any]:
        capture = _CaptureTransport()
        cls(capture).create(stream=stream, **kwargs)
        return capture.body
