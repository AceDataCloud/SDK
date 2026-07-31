"""Gemini resources — chat completions, video generation, and native API."""

from __future__ import annotations

import json as _json
from collections.abc import Iterator
from typing import Any, Literal

from .._runtime.tasks import AsyncTaskHandle, TaskHandle

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


class _GeminiCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: GeminiChatModel | str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/gemini/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncGeminiCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: GeminiChatModel | str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]):
        async for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _GeminiChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _GeminiCompletions(transport)


class _AsyncGeminiChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncGeminiCompletions(transport)


class Gemini:
    """Synchronous Gemini client — chat completions, video generation, and native API."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _GeminiChatNamespace(transport)

    def generate(
        self,
        *,
        prompt: str,
        model: GeminiVideoModel | str | None = None,
        aspect_ratio: Literal["16:9", "9:16"] | None = None,
        resolution: Literal["720p", "1080p"] | None = None,
        image_urls: list[str] | None = None,
        video_urls: list[str] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> TaskHandle:
        """Gemini video generation."""
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if resolution is not None:
            body["resolution"] = resolution
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_urls is not None:
            body["video_urls"] = video_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/gemini/videos", json=body)
        return TaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)

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
        """Native Gemini generateContent API."""
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
        return self._transport.request(
            "POST", f"/v1beta/models/{model}:generateContent", json=body
        )

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
        """Native Gemini streamGenerateContent API."""
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
        for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json=body
        ):
            yield _json.loads(chunk)


class AsyncGemini:
    """Async Gemini client — chat completions, video generation, and native API."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncGeminiChatNamespace(transport)

    async def generate(
        self,
        *,
        prompt: str,
        model: GeminiVideoModel | str | None = None,
        aspect_ratio: Literal["16:9", "9:16"] | None = None,
        resolution: Literal["720p", "1080p"] | None = None,
        image_urls: list[str] | None = None,
        video_urls: list[str] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> AsyncTaskHandle:
        """Gemini video generation."""
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if resolution is not None:
            body["resolution"] = resolution
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_urls is not None:
            body["video_urls"] = video_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/gemini/videos", json=body)
        return AsyncTaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)

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
        """Native Gemini generateContent API."""
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
        return await self._transport.request(
            "POST", f"/v1beta/models/{model}:generateContent", json=body
        )

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
    ):
        """Native Gemini streamGenerateContent API."""
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
        async for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json=body
        ):
            yield _json.loads(chunk)
