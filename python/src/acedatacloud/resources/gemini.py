"""Gemini AI resources — chat completions, native generate content, and video generation."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

GeminiModel = Literal[
    "gemini-3.1-pro",
    "gemini-3.0-pro",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-flash-image",
    "gemini-2.5-flash-image",
    "gemini-3-pro-image",
]

GeminiVideoModel = Literal["omni-flash"]


# ---------------------------------------------------------------------------
# Sync helpers
# ---------------------------------------------------------------------------


class _Completions:
    """Namespace for gemini.chat.completions."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/gemini/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _ChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _Models:
    """Namespace for native Gemini generate-content endpoints."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate_content(
        self,
        *,
        model: str,
        contents: list[dict[str, Any]],
        system_instruction: dict[str, Any] | None = None,
        generation_config: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_config: dict[str, Any] | None = None,
        safety_settings: list[dict[str, Any]] | None = None,
        cached_content: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"contents": contents, **kwargs}
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
        if cached_content is not None:
            body["cachedContent"] = cached_content
        return self._transport.request("POST", f"/v1beta/models/{model}:generateContent", json=body)

    def stream_generate_content(
        self,
        *,
        model: str,
        contents: list[dict[str, Any]],
        system_instruction: dict[str, Any] | None = None,
        generation_config: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_config: dict[str, Any] | None = None,
        safety_settings: list[dict[str, Any]] | None = None,
        cached_content: str | None = None,
        **kwargs: Any,
    ) -> Iterator[dict[str, Any]]:
        body: dict[str, Any] = {"contents": contents, **kwargs}
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
        if cached_content is not None:
            body["cachedContent"] = cached_content
        for chunk in self._transport.request_stream("POST", f"/v1beta/models/{model}:streamGenerateContent", json=body):
            yield _json.loads(chunk)


class _Videos:
    """Namespace for gemini.videos."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        model: str | None = None,
        aspect_ratio: Literal["16:9", "9:16"] | None = None,
        image_urls: list[str] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any]:
        from acedatacloud._runtime.tasks import TaskHandle

        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if image_urls is not None:
            body["image_urls"] = image_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        result = self._transport.request("POST", "/gemini/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = TaskHandle(task_id, "/gemini/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class Gemini:
    """Synchronous Gemini AI client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _ChatNamespace(transport)
        self.models = _Models(transport)
        self.videos = _Videos(transport)


# ---------------------------------------------------------------------------
# Async helpers
# ---------------------------------------------------------------------------


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class _AsyncModels:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate_content(
        self,
        *,
        model: str,
        contents: list[dict[str, Any]],
        system_instruction: dict[str, Any] | None = None,
        generation_config: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_config: dict[str, Any] | None = None,
        safety_settings: list[dict[str, Any]] | None = None,
        cached_content: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"contents": contents, **kwargs}
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
        if cached_content is not None:
            body["cachedContent"] = cached_content
        return await self._transport.request("POST", f"/v1beta/models/{model}:generateContent", json=body)

    async def stream_generate_content(
        self,
        *,
        model: str,
        contents: list[dict[str, Any]],
        system_instruction: dict[str, Any] | None = None,
        generation_config: dict[str, Any] | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_config: dict[str, Any] | None = None,
        safety_settings: list[dict[str, Any]] | None = None,
        cached_content: str | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        body: dict[str, Any] = {"contents": contents, **kwargs}
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
        if cached_content is not None:
            body["cachedContent"] = cached_content
        return self._stream(body, model)

    async def _stream(self, body: dict[str, Any], model: str) -> AsyncIterator[dict[str, Any]]:
        path = f"/v1beta/models/{model}:streamGenerateContent"
        async for chunk in self._transport.request_stream("POST", path, json=body):
            yield _json.loads(chunk)


class _AsyncVideos:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        model: str | None = None,
        aspect_ratio: Literal["16:9", "9:16"] | None = None,
        image_urls: list[str] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any]:
        from acedatacloud._runtime.tasks import AsyncTaskHandle

        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if image_urls is not None:
            body["image_urls"] = image_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        result = await self._transport.request("POST", "/gemini/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, "/gemini/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncGemini:
    """Async Gemini AI client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncChatNamespace(transport)
        self.models = _AsyncModels(transport)
        self.videos = _AsyncVideos(transport)
