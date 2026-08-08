"""Gemini provider resource."""

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
GeminiContentModel = Literal[
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
GeminiVideoAspectRatio = Literal["16:9", "9:16"]
GeminiVideoResolution = Literal["720p", "1080p"]


def _task_id(result: Any) -> str:
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


def _content_path(model: str, *, stream: bool = False) -> str:
    suffix = "streamGenerateContent?alt=sse" if stream else "generateContent"
    return f"/v1beta/models/{quote(model, safe='')}:{suffix}"


def _content_body(
    contents: list[dict[str, Any]],
    *,
    system_instruction: dict[str, Any] | None = None,
    generation_config: dict[str, Any] | None = None,
    tools: list[dict[str, Any]] | None = None,
    tool_config: dict[str, Any] | None = None,
    safety_settings: list[dict[str, Any]] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"contents": contents}
    if system_instruction is not None:
        body["systemInstruction"] = system_instruction
    if generation_config is not None:
        body["generationConfig"] = generation_config
    if tools is not None:
        body["tools"] = tools
    if tool_config is not None:
        body["toolConfig"] = tool_config
    if safety_settings is not None:
        body["safetySettings"] = safety_settings
    body.update(extra or {})
    return body


def _chat_body(
    *,
    model: GeminiChatModel,
    messages: list[dict[str, Any]],
    stream: bool,
    n: float | None = None,
    max_tokens: float | None = None,
    temperature: float | None = None,
    response_format: Any = None,
    top_p: float | None = None,
    frequency_penalty: float | None = None,
    presence_penalty: float | None = None,
    seed: int | None = None,
    stop: Any = None,
    max_completion_tokens: int | None = None,
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
    tools: list[dict[str, Any]] | None = None,
    tool_choice: Any = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "n": 1 if n is None else n,
        "temperature": 1 if temperature is None else temperature,
        "top_p": 1 if top_p is None else top_p,
        "frequency_penalty": 0 if frequency_penalty is None else frequency_penalty,
        "presence_penalty": 0 if presence_penalty is None else presence_penalty,
        "logprobs": False if logprobs is None else logprobs,
        "parallel_tool_calls": True if parallel_tool_calls is None else parallel_tool_calls,
        "reasoning_effort": "medium" if reasoning_effort is None else reasoning_effort,
        "service_tier": "auto" if service_tier is None else service_tier,
        "store": False if store is None else store,
    }
    optional = {
        "max_tokens": max_tokens,
        "response_format": response_format,
        "seed": seed,
        "stop": stop,
        "max_completion_tokens": max_completion_tokens,
        "top_logprobs": top_logprobs,
        "stream_options": stream_options,
        "user": user,
        "metadata": metadata,
        "logit_bias": logit_bias,
        "modalities": modalities,
        "audio": audio,
        "prediction": prediction,
        "web_search_options": web_search_options,
        "tools": tools,
        "tool_choice": tool_choice,
    }
    body.update({key: value for key, value in optional.items() if value is not None})
    body.update(extra or {})
    return body


class _Completions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: GeminiChatModel,
        messages: list[dict[str, Any]],
        stream: bool = False,
        n: float | None = None,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: Any = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        seed: int | None = None,
        stop: Any = None,
        max_completion_tokens: int | None = None,
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
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Any = None,
        **extra: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = _chat_body(
            model=model,
            messages=messages,
            stream=stream,
            n=n,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            seed=seed,
            stop=stop,
            max_completion_tokens=max_completion_tokens,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
            stream_options=stream_options,
            parallel_tool_calls=parallel_tool_calls,
            user=user,
            reasoning_effort=reasoning_effort,
            service_tier=service_tier,
            store=store,
            metadata=metadata,
            logit_bias=logit_bias,
            modalities=modalities,
            audio=audio,
            prediction=prediction,
            web_search_options=web_search_options,
            tools=tools,
            tool_choice=tool_choice,
            extra=extra,
        )
        if stream:
            return self._stream(body)
        return self._transport.request("POST", "/gemini/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: GeminiChatModel,
        messages: list[dict[str, Any]],
        stream: bool = False,
        n: float | None = None,
        max_tokens: float | None = None,
        temperature: float | None = None,
        response_format: Any = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        seed: int | None = None,
        stop: Any = None,
        max_completion_tokens: int | None = None,
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
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Any = None,
        **extra: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = _chat_body(
            model=model,
            messages=messages,
            stream=stream,
            n=n,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            seed=seed,
            stop=stop,
            max_completion_tokens=max_completion_tokens,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
            stream_options=stream_options,
            parallel_tool_calls=parallel_tool_calls,
            user=user,
            reasoning_effort=reasoning_effort,
            service_tier=service_tier,
            store=store,
            metadata=metadata,
            logit_bias=logit_bias,
            modalities=modalities,
            audio=audio,
            prediction=prediction,
            web_search_options=web_search_options,
            tools=tools,
            tool_choice=tool_choice,
            extra=extra,
        )
        if stream:
            return self._stream(body)
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _ChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _AsyncChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class _Videos:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        model: GeminiVideoModel | None = None,
        aspect_ratio: GeminiVideoAspectRatio | None = None,
        resolution: GeminiVideoResolution | None = None,
        image_urls: list[str] | None = None,
        video_urls: list[str] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        body: dict[str, Any] = {
            "prompt": prompt,
            "model": model or "omni-flash",
            "aspect_ratio": aspect_ratio or "16:9",
            "resolution": resolution or "720p",
            "async": True if async_ is None else async_,
        }
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_urls is not None:
            body["video_urls"] = video_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        body.update(extra)
        result = self._transport.request("POST", "/gemini/videos", json=body)
        handle = TaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _AsyncVideos:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        model: GeminiVideoModel | None = None,
        aspect_ratio: GeminiVideoAspectRatio | None = None,
        resolution: GeminiVideoResolution | None = None,
        image_urls: list[str] | None = None,
        video_urls: list[str] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        body: dict[str, Any] = {
            "prompt": prompt,
            "model": model or "omni-flash",
            "aspect_ratio": aspect_ratio or "16:9",
            "resolution": resolution or "720p",
            "async": True if async_ is None else async_,
        }
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_urls is not None:
            body["video_urls"] = video_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        body.update(extra)
        result = await self._transport.request("POST", "/gemini/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _Tasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def retrieve(self, id: str, **extra: Any) -> dict[str, Any]:
        return self._transport.request("POST", "/gemini/tasks", json={"action": "retrieve", "id": id, **extra})

    def retrieve_batch(self, ids: list[str] | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve_batch", **extra}
        if ids is not None:
            body["ids"] = ids
        return self._transport.request("POST", "/gemini/tasks", json=body)


class _AsyncTasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def retrieve(self, id: str, **extra: Any) -> dict[str, Any]:
        return await self._transport.request("POST", "/gemini/tasks", json={"action": "retrieve", "id": id, **extra})

    async def retrieve_batch(self, ids: list[str] | None = None, **extra: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve_batch", **extra}
        if ids is not None:
            body["ids"] = ids
        return await self._transport.request("POST", "/gemini/tasks", json=body)


class Gemini:
    """Synchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _ChatNamespace(transport)
        self.videos = _Videos(transport)
        self.tasks = _Tasks(transport)

    def generate_content(
        self,
        *,
        model: GeminiContentModel,
        contents: list[dict[str, Any]],
        system_instruction: dict[str, Any] | None = None,
        generation_config: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_config: dict[str, Any] | None = None,
        safety_settings: list[dict[str, Any]] | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        body = _content_body(
            contents,
            system_instruction=system_instruction,
            generation_config=generation_config,
            tools=tools,
            tool_config=tool_config,
            safety_settings=safety_settings,
            extra=extra,
        )
        return self._transport.request("POST", _content_path(model), json=body)

    def stream_generate_content(
        self,
        *,
        model: GeminiContentModel,
        contents: list[dict[str, Any]],
        system_instruction: dict[str, Any] | None = None,
        generation_config: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_config: dict[str, Any] | None = None,
        safety_settings: list[dict[str, Any]] | None = None,
        **extra: Any,
    ) -> Iterator[dict[str, Any]]:
        body = _content_body(
            contents,
            system_instruction=system_instruction,
            generation_config=generation_config,
            tools=tools,
            tool_config=tool_config,
            safety_settings=safety_settings,
            extra=extra,
        )
        for chunk in self._transport.request_stream("POST", _content_path(model, stream=True), json=body):
            yield _json.loads(chunk)


class AsyncGemini:
    """Asynchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncChatNamespace(transport)
        self.videos = _AsyncVideos(transport)
        self.tasks = _AsyncTasks(transport)

    async def generate_content(
        self,
        *,
        model: GeminiContentModel,
        contents: list[dict[str, Any]],
        system_instruction: dict[str, Any] | None = None,
        generation_config: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_config: dict[str, Any] | None = None,
        safety_settings: list[dict[str, Any]] | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        body = _content_body(
            contents,
            system_instruction=system_instruction,
            generation_config=generation_config,
            tools=tools,
            tool_config=tool_config,
            safety_settings=safety_settings,
            extra=extra,
        )
        return await self._transport.request("POST", _content_path(model), json=body)

    async def stream_generate_content(
        self,
        *,
        model: GeminiContentModel,
        contents: list[dict[str, Any]],
        system_instruction: dict[str, Any] | None = None,
        generation_config: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_config: dict[str, Any] | None = None,
        safety_settings: list[dict[str, Any]] | None = None,
        **extra: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        body = _content_body(
            contents,
            system_instruction=system_instruction,
            generation_config=generation_config,
            tools=tools,
            tool_config=tool_config,
            safety_settings=safety_settings,
            extra=extra,
        )
        async for chunk in self._transport.request_stream("POST", _content_path(model, stream=True), json=body):
            yield _json.loads(chunk)
