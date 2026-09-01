"""Gemini resources."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

GeminiModel = Literal[
    "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite", "gemini-3.1-pro-preview", "gemini-3-flash-preview",
    "gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite",
    "gemini-3.1-flash-image", "gemini-2.5-flash-image", "gemini-3-pro-image",
]


def _task_id(result: dict[str, Any]) -> str:
    return str(result.get("task_id") or result.get("id") or "")


class Gemini:
    """Synchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def chat_completions(
        self, *, model: GeminiModel, messages: list[dict[str, Any]], stream: bool = False, **extra: Any
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **extra}
        if stream:
            body["stream"] = True
            return (json.loads(chunk) for chunk in self._transport.request_stream("POST", "/gemini/chat/completions", json=body))
        return self._transport.request("POST", "/gemini/chat/completions", json=body)

    def generate_content(self, *, model: GeminiModel, contents: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
        return self._transport.request(
            "POST", f"/v1beta/models/{model}:generateContent", json={"contents": contents, **extra}
        )

    def stream_generate_content(
        self, *, model: GeminiModel, contents: list[dict[str, Any]], **extra: Any
    ) -> Iterator[dict[str, Any]]:
        body = {"contents": contents, **extra}
        return (json.loads(chunk) for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json=body
        ))

    def generate_video(
        self, *, prompt: str, model: Literal["omni-flash"] = "omni-flash",
        aspect_ratio: Literal["16:9", "9:16"] = "16:9",
        resolution: Literal["720p", "1080p"] = "720p", image_urls: list[str] | None = None,
        video_urls: list[str] | None = None, async_: bool | None = None, wait: bool = False,
        poll_interval: float = 3.0, max_wait: float = 600.0, callback_url: str | None = None,
    ) -> TaskHandle:
        body: dict[str, Any] = {"prompt": prompt, "model": model, "aspect_ratio": aspect_ratio, "resolution": resolution}
        if image_urls is not None: body["image_urls"] = image_urls
        if video_urls is not None: body["video_urls"] = video_urls
        if callback_url is not None: body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/gemini/videos", json=body)
        handle = TaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait: handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def tasks(
        self, *, id: str | None = None, ids: list[str] | None = None,
        action: Literal["retrieve", "retrieve_batch"] = "retrieve",
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": action}
        if id is not None: body["id"] = id
        if ids is not None: body["ids"] = ids
        return self._transport.request("POST", "/gemini/tasks", json=body)


class AsyncGemini:
    """Asynchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def chat_completions(
        self, *, model: GeminiModel, messages: list[dict[str, Any]], stream: bool = False, **extra: Any
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **extra}
        if stream:
            body["stream"] = True
            return self._stream("/gemini/chat/completions", body)
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)

    async def generate_content(self, *, model: GeminiModel, contents: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
        return await self._transport.request(
            "POST", f"/v1beta/models/{model}:generateContent", json={"contents": contents, **extra}
        )

    async def stream_generate_content(
        self, *, model: GeminiModel, contents: list[dict[str, Any]], **extra: Any
    ) -> AsyncIterator[dict[str, Any]]:
        return self._stream(f"/v1beta/models/{model}:streamGenerateContent", {"contents": contents, **extra})

    async def generate_video(
        self, *, prompt: str, model: Literal["omni-flash"] = "omni-flash",
        aspect_ratio: Literal["16:9", "9:16"] = "16:9",
        resolution: Literal["720p", "1080p"] = "720p", image_urls: list[str] | None = None,
        video_urls: list[str] | None = None, async_: bool | None = None, wait: bool = False,
        poll_interval: float = 3.0, max_wait: float = 600.0, callback_url: str | None = None,
    ) -> AsyncTaskHandle:
        body: dict[str, Any] = {"prompt": prompt, "model": model, "aspect_ratio": aspect_ratio, "resolution": resolution}
        if image_urls is not None: body["image_urls"] = image_urls
        if video_urls is not None: body["video_urls"] = video_urls
        if callback_url is not None: body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/gemini/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait: await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def tasks(
        self, *, id: str | None = None, ids: list[str] | None = None,
        action: Literal["retrieve", "retrieve_batch"] = "retrieve",
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": action}
        if id is not None: body["id"] = id
        if ids is not None: body["ids"] = ids
        return await self._transport.request("POST", "/gemini/tasks", json=body)

    async def _stream(self, path: str, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", path, json=body):
            yield json.loads(chunk)
