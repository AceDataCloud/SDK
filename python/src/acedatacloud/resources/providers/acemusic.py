"""Acemusic (acemusic) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle


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


class Acemusic:
    """Synchronous acemusic client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: Literal["generate", "upload", "cover", "mashup"] | None = None,
        model: Literal["acemusic-v1.1", "acemusic-v1"] | None = None,
        custom: bool | None = None,
        prompt: str | None = None,
        lyric: str | None = None,
        style: str | None = None,
        title: str | None = None,
        audio_url: str | None = None,
        name: str | None = None,
        audio_id: str | None = None,
        mashup_audio_ids: list[str] | None = None,
        audio_influence: float | None = None,
        idempotency_key: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """ACE Music Audios"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "generate"
        if model is not None:
            body["model"] = model
        if custom is not None:
            body["custom"] = custom
        if prompt is not None:
            body["prompt"] = prompt
        if lyric is not None:
            body["lyric"] = lyric
        if style is not None:
            body["style"] = style
        if title is not None:
            body["title"] = title
        if audio_url is not None:
            body["audio_url"] = audio_url
        if name is not None:
            body["name"] = name
        if audio_id is not None:
            body["audio_id"] = audio_id
        if mashup_audio_ids is not None:
            body["mashup_audio_ids"] = mashup_audio_ids
        if audio_influence is not None:
            body["audio_influence"] = audio_influence
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        extra_headers = {k: v for k, v in {"Idempotency-Key": idempotency_key}.items() if v is not None}
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/acemusic/audios", json=body, extra_headers=extra_headers)
        handle = TaskHandle(_task_id(result), "/acemusic/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def lyrics(
        self,
        *,
        prompt: str,
        style: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """ACE Music Lyrics"""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        if style is not None:
            body["style"] = style
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/acemusic/lyrics", json=body)

    def tasks(
        self,
        *,
        action: Literal["retrieve", "retrieve_batch", "list"],
        id: str | None = None,
        ids: list[str] | None = None,
        page: int | None = None,
        page_size: int | None = None,
        type: Literal["audios", "lyrics"] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        created_at_min: float | None = None,
        created_at_max: float | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """ACE Music Tasks"""
        body: dict[str, Any] = {}
        body["action"] = action
        if id is not None:
            body["id"] = id
        if ids is not None:
            body["ids"] = ids
        if page is not None:
            body["page"] = page
        if page_size is not None:
            body["page_size"] = page_size
        if type is not None:
            body["type"] = type
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        if created_at_min is not None:
            body["created_at_min"] = created_at_min
        if created_at_max is not None:
            body["created_at_max"] = created_at_max
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/acemusic/tasks", json=body)


class AsyncAcemusic:
    """Asynchronous acemusic client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: Literal["generate", "upload", "cover", "mashup"] | None = None,
        model: Literal["acemusic-v1.1", "acemusic-v1"] | None = None,
        custom: bool | None = None,
        prompt: str | None = None,
        lyric: str | None = None,
        style: str | None = None,
        title: str | None = None,
        audio_url: str | None = None,
        name: str | None = None,
        audio_id: str | None = None,
        mashup_audio_ids: list[str] | None = None,
        audio_influence: float | None = None,
        idempotency_key: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """ACE Music Audios"""
        body: dict[str, Any] = {}
        body["action"] = action if action is not None else "generate"
        if model is not None:
            body["model"] = model
        if custom is not None:
            body["custom"] = custom
        if prompt is not None:
            body["prompt"] = prompt
        if lyric is not None:
            body["lyric"] = lyric
        if style is not None:
            body["style"] = style
        if title is not None:
            body["title"] = title
        if audio_url is not None:
            body["audio_url"] = audio_url
        if name is not None:
            body["name"] = name
        if audio_id is not None:
            body["audio_id"] = audio_id
        if mashup_audio_ids is not None:
            body["mashup_audio_ids"] = mashup_audio_ids
        if audio_influence is not None:
            body["audio_influence"] = audio_influence
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        extra_headers = {k: v for k, v in {"Idempotency-Key": idempotency_key}.items() if v is not None}
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/acemusic/audios", json=body, extra_headers=extra_headers)
        handle = AsyncTaskHandle(_task_id(result), "/acemusic/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def lyrics(
        self,
        *,
        prompt: str,
        style: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """ACE Music Lyrics"""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        if style is not None:
            body["style"] = style
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/acemusic/lyrics", json=body)

    async def tasks(
        self,
        *,
        action: Literal["retrieve", "retrieve_batch", "list"],
        id: str | None = None,
        ids: list[str] | None = None,
        page: int | None = None,
        page_size: int | None = None,
        type: Literal["audios", "lyrics"] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        created_at_min: float | None = None,
        created_at_max: float | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """ACE Music Tasks"""
        body: dict[str, Any] = {}
        body["action"] = action
        if id is not None:
            body["id"] = id
        if ids is not None:
            body["ids"] = ids
        if page is not None:
            body["page"] = page
        if page_size is not None:
            body["page_size"] = page_size
        if type is not None:
            body["type"] = type
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        if created_at_min is not None:
            body["created_at_min"] = created_at_min
        if created_at_max is not None:
            body["created_at_max"] = created_at_max
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/acemusic/tasks", json=body)
