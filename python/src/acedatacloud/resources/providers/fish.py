"""Fish (fish) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401
from urllib.parse import quote

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


class Fish:
    """Synchronous fish client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        text: str,
        reference_id: str | list[str] | None = None,
        format: Literal["mp3", "wav", "pcm"] | None = None,
        sample_rate: int | None = None,
        mp3_bitrate: int | None = None,
        latency: Literal["normal", "balanced"] | None = None,
        chunk_length: int | None = None,
        min_chunk_length: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        repetition_penalty: float | None = None,
        max_new_tokens: int | None = None,
        normalize: bool | None = None,
        prosody: dict[str, Any] | None = None,
        references: list[dict[str, Any]] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Fish Tts"""
        body: dict[str, Any] = {}
        body["text"] = text
        if reference_id is not None:
            body["reference_id"] = reference_id
        if format is not None:
            body["format"] = format
        if sample_rate is not None:
            body["sample_rate"] = sample_rate
        if mp3_bitrate is not None:
            body["mp3_bitrate"] = mp3_bitrate
        if latency is not None:
            body["latency"] = latency
        if chunk_length is not None:
            body["chunk_length"] = chunk_length
        if min_chunk_length is not None:
            body["min_chunk_length"] = min_chunk_length
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["top_p"] = top_p
        if repetition_penalty is not None:
            body["repetition_penalty"] = repetition_penalty
        if max_new_tokens is not None:
            body["max_new_tokens"] = max_new_tokens
        if normalize is not None:
            body["normalize"] = normalize
        if prosody is not None:
            body["prosody"] = prosody
        if references is not None:
            body["references"] = references
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/fish/tts", json=body)
        handle = TaskHandle(_task_id(result), "/fish/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def model(
        self,
        *,
        page_size: int | None = None,
        page_number: int | None = None,
        title: str | None = None,
        tag: str | None = None,
        self_: bool | None = None,
        author_id: str | None = None,
        language: str | None = None,
        title_language: str | None = None,
        sort_by: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Fish Model Query"""
        params: dict[str, Any] = {}
        params["page_size"] = page_size if page_size is not None else 10
        params["page_number"] = page_number if page_number is not None else 1
        if title is not None:
            params["title"] = title
        if tag is not None:
            params["tag"] = tag
        if self_ is not None:
            params["self"] = self_
        if author_id is not None:
            params["author_id"] = author_id
        if language is not None:
            params["language"] = language
        if title_language is not None:
            params["title_language"] = title_language
        if sort_by is not None:
            params["sort_by"] = sort_by
        params.update(extra)
        return self._transport.request("GET", "/fish/model", params=params)

    def model_by_id(
        self,
        *,
        id: str,
        **extra: Any,
    ) -> dict[str, Any]:
        """Fish Model Get"""
        params: dict[str, Any] = {}
        params.update(extra)
        return self._transport.request("GET", f"/fish/model/{quote(str(id), safe='')}", params=params)


class AsyncFish:
    """Asynchronous fish client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        text: str,
        reference_id: str | list[str] | None = None,
        format: Literal["mp3", "wav", "pcm"] | None = None,
        sample_rate: int | None = None,
        mp3_bitrate: int | None = None,
        latency: Literal["normal", "balanced"] | None = None,
        chunk_length: int | None = None,
        min_chunk_length: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        repetition_penalty: float | None = None,
        max_new_tokens: int | None = None,
        normalize: bool | None = None,
        prosody: dict[str, Any] | None = None,
        references: list[dict[str, Any]] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Fish Tts"""
        body: dict[str, Any] = {}
        body["text"] = text
        if reference_id is not None:
            body["reference_id"] = reference_id
        if format is not None:
            body["format"] = format
        if sample_rate is not None:
            body["sample_rate"] = sample_rate
        if mp3_bitrate is not None:
            body["mp3_bitrate"] = mp3_bitrate
        if latency is not None:
            body["latency"] = latency
        if chunk_length is not None:
            body["chunk_length"] = chunk_length
        if min_chunk_length is not None:
            body["min_chunk_length"] = min_chunk_length
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["top_p"] = top_p
        if repetition_penalty is not None:
            body["repetition_penalty"] = repetition_penalty
        if max_new_tokens is not None:
            body["max_new_tokens"] = max_new_tokens
        if normalize is not None:
            body["normalize"] = normalize
        if prosody is not None:
            body["prosody"] = prosody
        if references is not None:
            body["references"] = references
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/fish/tts", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/fish/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def model(
        self,
        *,
        page_size: int | None = None,
        page_number: int | None = None,
        title: str | None = None,
        tag: str | None = None,
        self_: bool | None = None,
        author_id: str | None = None,
        language: str | None = None,
        title_language: str | None = None,
        sort_by: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Fish Model Query"""
        params: dict[str, Any] = {}
        params["page_size"] = page_size if page_size is not None else 10
        params["page_number"] = page_number if page_number is not None else 1
        if title is not None:
            params["title"] = title
        if tag is not None:
            params["tag"] = tag
        if self_ is not None:
            params["self"] = self_
        if author_id is not None:
            params["author_id"] = author_id
        if language is not None:
            params["language"] = language
        if title_language is not None:
            params["title_language"] = title_language
        if sort_by is not None:
            params["sort_by"] = sort_by
        params.update(extra)
        return await self._transport.request("GET", "/fish/model", params=params)

    async def model_by_id(
        self,
        *,
        id: str,
        **extra: Any,
    ) -> dict[str, Any]:
        """Fish Model Get"""
        params: dict[str, Any] = {}
        params.update(extra)
        return await self._transport.request("GET", f"/fish/model/{quote(str(id), safe='')}", params=params)
