"""Gemini AI resources."""

from __future__ import annotations

import json as _json
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

GeminiModel = Literal[
    "gemini-3.1-pro",
    "gemini-3.0-pro",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-flash-image-preview",
    "gemini-2.5-flash-image",
    "gemini-3-pro-image-preview",
]

GeminiVideoModel = Literal["omni-flash"]


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


class _Models:
    """Namespace for native Gemini model API."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate_content(
        self,
        model: str,
        *,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {"contents": contents, **kwargs}
        return self._transport.request("POST", f"/v1beta/models/{model}:generateContent", json=body)

    def stream_generate_content(
        self,
        model: str,
        *,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> Iterator[dict[str, Any]]:
        body = {"contents": contents, **kwargs}
        for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json=body
        ):
            yield _json.loads(chunk)


class _AsyncModels:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate_content(
        self,
        model: str,
        *,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = {"contents": contents, **kwargs}
        return await self._transport.request("POST", f"/v1beta/models/{model}:generateContent", json=body)

    async def stream_generate_content(
        self,
        model: str,
        *,
        contents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        body = {"contents": contents, **kwargs}
        async for chunk in self._transport.request_stream(
            "POST", f"/v1beta/models/{model}:streamGenerateContent", json=body
        ):
            yield _json.loads(chunk)


class _Videos:
    """Namespace for gemini.videos."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        model: str | None = None,
        aspect_ratio: Literal["16:9", "9:16"] | None = None,
        image_urls: list[str] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if image_urls is not None:
            body["image_urls"] = image_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        result = self._transport.request("POST", "/gemini/videos", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result

        handle = TaskHandle(task_id, "/gemini/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _AsyncVideos:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        model: str | None = None,
        aspect_ratio: Literal["16:9", "9:16"] | None = None,
        image_urls: list[str] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if model is not None:
            body["model"] = model
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if image_urls is not None:
            body["image_urls"] = image_urls
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        result = await self._transport.request("POST", "/gemini/videos", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, "/gemini/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class _Tasks:
    """Namespace for gemini.tasks."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def retrieve(
        self,
        *,
        id: str | None = None,
        ids: list[str] | None = None,
        action: Literal["retrieve", "retrieve_batch"] = "retrieve",
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": action, **kwargs}
        if id is not None:
            body["id"] = id
        if ids is not None:
            body["ids"] = ids
        return self._transport.request("POST", "/gemini/tasks", json=body)


class _AsyncTasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def retrieve(
        self,
        *,
        id: str | None = None,
        ids: list[str] | None = None,
        action: Literal["retrieve", "retrieve_batch"] = "retrieve",
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": action, **kwargs}
        if id is not None:
            body["id"] = id
        if ids is not None:
            body["ids"] = ids
        return await self._transport.request("POST", "/gemini/tasks", json=body)


class Gemini:
    """Synchronous Gemini AI client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _ChatNamespace(transport)
        self.models = _Models(transport)
        self.videos = _Videos(transport)
        self.tasks = _Tasks(transport)


class AsyncGemini:
    """Async Gemini AI client."""

    def __init__(self, transport: Any) -> None:
        self.chat = _AsyncChatNamespace(transport)
        self.models = _AsyncModels(transport)
        self.videos = _AsyncVideos(transport)
        self.tasks = _AsyncTasks(transport)
