"""Gemini resources — OpenAI-compatible chat, video generation, native v1beta.

Hand-written rather than generated: the service spans three shapes the provider
generator does not model — an OpenAI-compatible chat surface, an async video
endpoint, and Google's native `generateContent` calls with the model in the path.
"""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

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
GeminiNativeModel = Literal[
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-3-flash-preview",
    "gemini-3.5-flash",
    "gemini-3.0-pro",
    "gemini-3.1-pro",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-flash-image",
    "gemini-2.5-flash-image",
    "gemini-3-pro-image",
]
GeminiVideoModel = Literal["omni-flash"]
GeminiVideoAspectRatio = Literal["16:9", "9:16"]
GeminiVideoResolution = Literal["720p", "1080p"]

_CHAT_PATH = "/gemini/chat/completions"
_VIDEOS_PATH = "/gemini/videos"
_TASKS_PATH = "/gemini/tasks"


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


def _video_body(
    *,
    prompt: str,
    model: str | None,
    aspect_ratio: str | None,
    resolution: str | None,
    image_urls: list[str] | None,
    video_urls: list[str] | None,
    callback_url: str | None,
    async_: bool | None,
    extra: dict[str, Any],
) -> dict[str, Any]:
    if video_urls is not None and len(video_urls) > 1:
        raise ValueError("video_urls accepts at most 1 video URL")
    body: dict[str, Any] = {"prompt": prompt}
    body["model"] = model if model is not None else "omni-flash"
    body["aspect_ratio"] = aspect_ratio if aspect_ratio is not None else "16:9"
    body["resolution"] = resolution if resolution is not None else "720p"
    if image_urls is not None:
        body["image_urls"] = image_urls
    if video_urls is not None:
        body["video_urls"] = video_urls
    body.update(extra)
    if callback_url is not None:
        body["callback_url"] = callback_url
    body["async"] = True if async_ is None else async_
    return body


def _native_path(model: str, *, stream: bool) -> str:
    action = "streamGenerateContent" if stream else "generateContent"
    return f"/v1beta/models/{model}:{action}"


def _native_body(contents: list[dict[str, Any]], extra: dict[str, Any]) -> dict[str, Any]:
    return {"contents": contents, **extra}


class _Completions:
    """Namespace for gemini.chat.completions."""

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
        body: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return self._transport.request("POST", _CHAT_PATH, json=body)

    def _stream(self, body: dict[str, Any]) -> Iterator[dict[str, Any]]:
        for chunk in self._transport.request_stream("POST", _CHAT_PATH, json=body):
            yield _json.loads(chunk)


class _AsyncCompletions:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def create(
        self,
        *,
        model: GeminiChatModel | str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncIterator[dict[str, Any]]:
        body: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        if stream:
            body["stream"] = True
            return self._stream(body)
        return await self._transport.request("POST", _CHAT_PATH, json=body)

    async def _stream(self, body: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        async for chunk in self._transport.request_stream("POST", _CHAT_PATH, json=body):
            yield _json.loads(chunk)


class _ChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _Completions(transport)


class _AsyncChatNamespace:
    def __init__(self, transport: Any) -> None:
        self.completions = _AsyncCompletions(transport)


class _Videos:
    """Namespace for gemini.videos."""

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
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **extra: Any,
    ) -> TaskHandle:
        body = _video_body(
            prompt=prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            image_urls=image_urls,
            video_urls=video_urls,
            callback_url=callback_url,
            async_=async_,
            extra=extra,
        )
        result = self._transport.request("POST", _VIDEOS_PATH, json=body)
        handle = TaskHandle(_task_id(result), _TASKS_PATH, self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _AsyncVideos:
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
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **extra: Any,
    ) -> AsyncTaskHandle:
        body = _video_body(
            prompt=prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            image_urls=image_urls,
            video_urls=video_urls,
            callback_url=callback_url,
            async_=async_,
            extra=extra,
        )
        result = await self._transport.request("POST", _VIDEOS_PATH, json=body)
        handle = AsyncTaskHandle(_task_id(result), _TASKS_PATH, self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class Gemini:
    """Synchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _ChatNamespace(transport)
        self.videos = _Videos(transport)

    def generate_content(
        self,
        *,
        model: GeminiNativeModel | str,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Google's native `POST /v1beta/models/{model}:generateContent`."""
        return self._transport.request("POST", _native_path(model, stream=False), json=_native_body(contents, kwargs))

    def stream_generate_content(
        self,
        *,
        model: GeminiNativeModel | str,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> Iterator[dict[str, Any]]:
        """Google's native `POST /v1beta/models/{model}:streamGenerateContent`."""
        for chunk in self._transport.request_stream(
            "POST", _native_path(model, stream=True), json=_native_body(contents, kwargs)
        ):
            yield _json.loads(chunk)


class AsyncGemini:
    """Asynchronous Gemini client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.chat = _AsyncChatNamespace(transport)
        self.videos = _AsyncVideos(transport)

    async def generate_content(
        self,
        *,
        model: GeminiNativeModel | str,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Google's native `POST /v1beta/models/{model}:generateContent`."""
        return await self._transport.request(
            "POST", _native_path(model, stream=False), json=_native_body(contents, kwargs)
        )

    async def stream_generate_content(
        self,
        *,
        model: GeminiNativeModel | str,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """Google's native `POST /v1beta/models/{model}:streamGenerateContent`."""
        async for chunk in self._transport.request_stream(
            "POST", _native_path(model, stream=True), json=_native_body(contents, kwargs)
        ):
            yield _json.loads(chunk)
