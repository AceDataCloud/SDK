"""Gemini (gemini) — provider client for Gemini AI chat completions and video generation."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

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
    "gemini-3.1-flash-image",
    "gemini-2.5-flash-image",
    "gemini-3-pro-image",
]
GeminiVideoModel = Literal["omni-flash"]
GeminiVideoAspectRatio = Literal["16:9", "9:16"]
GeminiVideoResolution = Literal["720p", "1080p"]


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


class _GeminiCompletions:
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
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _GeminiChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _GeminiCompletions(transport)


class _AsyncGeminiChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncGeminiCompletions(transport)


class _GeminiVideos:
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
        """Gemini video generation API."""
        body: dict[str, Any] = {"prompt": prompt}
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
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/gemini/videos", json=body)
        handle = TaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _AsyncGeminiVideos:
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
        """Gemini video generation API."""
        body: dict[str, Any] = {"prompt": prompt}
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
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/gemini/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class Gemini:
    """Synchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _GeminiChat(transport)
        self.videos = _GeminiVideos(transport)

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
        return self._transport.request("POST", f"/v1beta/models/{model}:generateContent", json=body)

    def stream_generate_content(
        self,
        *,
        model: str,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> Iterator[dict[str, Any]]:
        """Native Gemini streamGenerateContent API."""
        body: dict[str, Any] = {"contents": contents, **kwargs}
        for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json=body
        ):
            yield _json.loads(chunk)


class AsyncGemini:
    """Asynchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncGeminiChat(transport)
        self.videos = _AsyncGeminiVideos(transport)

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
        return await self._transport.request("POST", f"/v1beta/models/{model}:generateContent", json=body)

    async def stream_generate_content(
        self,
        *,
        model: str,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """Native Gemini streamGenerateContent API."""
        body: dict[str, Any] = {"contents": contents, **kwargs}
        async for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json=body
        ):
            yield _json.loads(chunk)
