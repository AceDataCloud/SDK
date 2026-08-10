"""Gemini chat, content generation, and video resources."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

GeminiModel = Literal[
    "gemini-3.1-pro",
    "gemini-3.0-pro",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-3.1-flash-lite-preview",
]


def _task_id(result: dict[str, Any]) -> str:
    return str(result.get("task_id") or result.get("id") or "")


class _Completions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def create(
        self,
        *,
        model: GeminiModel,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | Iterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return ( _json.loads(chunk) for chunk in self._transport.request_stream(
                "POST", "/gemini/chat/completions", json=body
            ))
        return self._transport.request("POST", "/gemini/chat/completions", json=body)


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: GeminiModel,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True

            async def chunks() -> AsyncIterator[dict[str, Any]]:
                async for chunk in self._transport.request_stream(
                    "POST", "/gemini/chat/completions", json=body
                ):
                    yield _json.loads(chunk)

            return chunks()
        return await self._transport.request("POST", "/gemini/chat/completions", json=body)


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
        return (
            _json.loads(chunk)
            for chunk in self._transport.request_stream(
                "POST", f"/v1beta/models/{model}:streamGenerateContent", json={"contents": contents, **kwargs}
            )
        )

    def generate(
        self, *, prompt: str, model: Literal["omni-flash"] = "omni-flash",
        aspect_ratio: Literal["16:9", "9:16"] = "16:9",
        resolution: Literal["720p", "1080p"] = "720p", image_urls: list[str] | None = None,
        video_urls: list[str] | None = None, callback_url: str | None = None,
        async_: bool | None = None, wait: bool = False, poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> TaskHandle:
        body: dict[str, Any] = {"prompt": prompt, "model": model, "aspect_ratio": aspect_ratio, "resolution": resolution, "async": True if async_ is None else async_}
        for key, value in {"image_urls": image_urls, "video_urls": video_urls, "callback_url": callback_url}.items():
            if value is not None:
                body[key] = value
        result = self._transport.request("POST", "/gemini/videos", json=body)
        handle = TaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncGemini:
    """Asynchronous Gemini client."""

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
        async for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json={"contents": contents, **kwargs}
        ):
            yield _json.loads(chunk)

    async def generate(
        self, *, prompt: str, model: Literal["omni-flash"] = "omni-flash",
        aspect_ratio: Literal["16:9", "9:16"] = "16:9",
        resolution: Literal["720p", "1080p"] = "720p", image_urls: list[str] | None = None,
        video_urls: list[str] | None = None, callback_url: str | None = None,
        async_: bool | None = None, wait: bool = False, poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> AsyncTaskHandle:
        body: dict[str, Any] = {"prompt": prompt, "model": model, "aspect_ratio": aspect_ratio, "resolution": resolution, "async": True if async_ is None else async_}
        for key, value in {"image_urls": image_urls, "video_urls": video_urls, "callback_url": callback_url}.items():
            if value is not None:
                body[key] = value
        result = await self._transport.request("POST", "/gemini/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/gemini/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
