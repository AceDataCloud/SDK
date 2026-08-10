"""Gemini provider resource."""

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


class _Completions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self, *, model: GeminiChatModel, messages: list[dict[str, Any]], stream: bool = False, **kwargs: Any
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
        self, *, model: GeminiChatModel, messages: list[dict[str, Any]], stream: bool = False, **kwargs: Any
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body):
            yield _json.loads(chunk)


class _Chat:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _AsyncChat:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class Gemini:
    """Synchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _Chat(transport)

    def generate_content(self, *, model: str, contents: list[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
        return self._transport.request(
            "POST", f"/v1beta/models/{model}:generateContent", json={"contents": contents, **kwargs}
        )

    def stream_generate_content(
        self, *, model: str, contents: list[dict[str, Any]], **kwargs: Any
    ) -> Iterator[dict[str, Any]]:
        body = {"contents": contents, **kwargs}
        for chunk in self._transport.request_stream("POST", f"/v1beta/models/{model}:streamGenerateContent", json=body):
            yield _json.loads(chunk)

    def videos(
        self,
        *,
        prompt: str,
        model: GeminiVideoModel = "omni-flash",
        aspect_ratio: Literal["16:9", "9:16"] = "16:9",
        resolution: Literal["720p", "1080p"] = "720p",
        image_urls: list[str] | None = None,
        video_urls: list[str] | None = None,
        async_: bool = True,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
    ) -> TaskHandle:
        body: dict[str, Any] = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "async": async_,
        }
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_urls is not None:
            body["video_urls"] = video_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        result = self._transport.request("POST", "/gemini/videos", json=body)
        handle = TaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncGemini:
    """Async Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncChat(transport)

    async def generate_content(self, *, model: str, contents: list[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
        return await self._transport.request(
            "POST", f"/v1beta/models/{model}:generateContent", json={"contents": contents, **kwargs}
        )

    async def stream_generate_content(
        self, *, model: str, contents: list[dict[str, Any]], **kwargs: Any
    ) -> AsyncIterator[dict[str, Any]]:
        body = {"contents": contents, **kwargs}
        async for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json=body
        ):
            yield _json.loads(chunk)

    async def videos(
        self,
        *,
        prompt: str,
        model: GeminiVideoModel = "omni-flash",
        aspect_ratio: Literal["16:9", "9:16"] = "16:9",
        resolution: Literal["720p", "1080p"] = "720p",
        image_urls: list[str] | None = None,
        video_urls: list[str] | None = None,
        async_: bool = True,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
    ) -> AsyncTaskHandle:
        body: dict[str, Any] = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "async": async_,
        }
        if image_urls is not None:
            body["image_urls"] = image_urls
        if video_urls is not None:
            body["video_urls"] = video_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        result = await self._transport.request("POST", "/gemini/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
