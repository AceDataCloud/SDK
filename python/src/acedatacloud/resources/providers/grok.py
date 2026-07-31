"""Grok (grok) — provider client for Grok chat completions and video generation."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

GrokChatModel = Literal["grok-4.5", "grok-4", "grok-3"]
GrokVideoModel = Literal[
    "grok-imagine-video-1.5-fast:reverse",
    "grok-imagine-video:reverse",
    "grok-imagine-video:official",
    "grok-imagine-video-1.5:official",
    "grok-imagine-video",
]
GrokVideoAspectRatio = Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]
GrokVideoResolution = Literal["480p", "720p", "1080p"]


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


class _GrokCompletions:
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
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/grok/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", "/grok/chat/completions", json=body):
            yield _json.loads(chunk)


class _GrokChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _GrokCompletions(transport)


class _AsyncGrokChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncGrokCompletions(transport)


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
        aspect_ratio: GrokVideoAspectRatio | None = None,
        resolution: GrokVideoResolution | None = None,
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
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/grok/videos", json=body)
        handle = TaskHandle(_task_id(result), "/grok/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


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
        aspect_ratio: GrokVideoAspectRatio | None = None,
        resolution: GrokVideoResolution | None = None,
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
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/grok/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/grok/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class Grok:
    """Synchronous Grok client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _GrokChat(transport)
        self.videos = _GrokVideos(transport)


class AsyncGrok:
    """Asynchronous Grok client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncGrokChat(transport)
        self.videos = _AsyncGrokVideos(transport)
