"""Grok resources — chat completions and video generation."""

from __future__ import annotations

import json as _json
from collections.abc import Iterator
from typing import Any, Literal

from .._runtime.tasks import AsyncTaskHandle, TaskHandle

GrokChatModel = Literal["grok-4.5", "grok-4", "grok-3"]
GrokVideoModel = Literal[
    "grok-imagine-video-1.5-fast:reverse",
    "grok-imagine-video:reverse",
    "grok-imagine-video:official",
    "grok-imagine-video-1.5:official",
    "grok-imagine-video",
]


def _task_id(result: Any) -> str:
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


class _GrokCompletions:
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


class _AsyncGrokCompletions:
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


class _GrokChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _GrokCompletions(transport)


class _AsyncGrokChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncGrokCompletions(transport)


class Grok:
    """Synchronous Grok client — chat completions and video generation."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _GrokChatNamespace(transport)

    def generate(
        self,
        *,
        prompt: str | None = None,
        model: GrokVideoModel | None = None,
        image_url: str | None = None,
        reference_image_urls: list[str] | None = None,
        aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"] | None = None,
        resolution: Literal["480p", "720p", "1080p"] | None = None,
        duration: int | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> TaskHandle:
        """Grok video generation."""
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
        result = self._transport.request("POST", "/grok/videos", json=body)
        return TaskHandle(_task_id(result), "/grok/tasks", self._transport, submitted=result)


class AsyncGrok:
    """Async Grok client — chat completions and video generation."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncGrokChatNamespace(transport)

    async def generate(
        self,
        *,
        prompt: str | None = None,
        model: GrokVideoModel | None = None,
        image_url: str | None = None,
        reference_image_urls: list[str] | None = None,
        aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"] | None = None,
        resolution: Literal["480p", "720p", "1080p"] | None = None,
        duration: int | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        **kwargs: Any,
    ) -> AsyncTaskHandle:
        """Grok video generation."""
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
        result = await self._transport.request("POST", "/grok/videos", json=body)
        return AsyncTaskHandle(_task_id(result), "/grok/tasks", self._transport, submitted=result)
