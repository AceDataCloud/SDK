"""Grok resources."""

from __future__ import annotations

import json as _json
from collections.abc import Iterator
from typing import Any, Literal

GrokChatModel = Literal["grok-4.5", "grok-4", "grok-3"]
GrokVideoModel = Literal["grok-imagine-video-1.5-fast", "grok-imagine-video-1.5"]


class _Completions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: GrokChatModel | str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", "/grok/chat/completions", json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", "/grok/chat/completions", json=body):
            yield _json.loads(chunk)


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: GrokChatModel | str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/grok/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]):
        async for chunk in self._transport.request_stream("POST", "/grok/chat/completions", json=body):
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
        prompt: str | None = None,
        model: GrokVideoModel | str | None = None,
        image_url: str | None = None,
        reference_image_urls: list[str] | None = None,
        aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"] | None = None,
        resolution: Literal["480p", "720p", "1080p"] | None = None,
        duration: int | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
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
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return self._transport.request("POST", "/grok/videos", json=body)


class _AsyncVideos:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str | None = None,
        model: GrokVideoModel | str | None = None,
        image_url: str | None = None,
        reference_image_urls: list[str] | None = None,
        aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"] | None = None,
        resolution: Literal["480p", "720p", "1080p"] | None = None,
        duration: int | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
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
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        return await self._transport.request("POST", "/grok/videos", json=body)


class Grok:
    """Synchronous Grok resource."""

    def __init__(self, transport: Any) -> None:
        self.chat = _ChatNamespace(transport)
        self.videos = _Videos(transport)


class AsyncGrok:
    """Async Grok resource."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncChatNamespace(transport)
        self.videos = _AsyncVideos(transport)
