"""Gemini chat completions and native generate content resources."""

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
    "gemini-2.0-flash",
]


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
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
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


class _ChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _AsyncChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class Gemini:
    """Synchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _ChatNamespace(transport)

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


class AsyncGemini:
    """Async Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncChatNamespace(transport)

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
        url = f"/v1beta/models/{model}:streamGenerateContent"
        async for chunk in self._transport.request_stream("POST", url, json=body):
            yield _json.loads(chunk)
