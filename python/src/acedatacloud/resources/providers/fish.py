"""Fish (fish) — generated from the platform OpenAPI spec.

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


class Fish:
    """Synchronous fish client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        text: str,
        model: Literal["s1", "s2-pro", "s2.1-pro"] | None = None,
        top_p: float | None = None,
        format: Literal["mp3", "wav", "pcm"] | None = None,
        latency: Literal["normal", "balanced"] | None = None,
        prosody: dict[str, Any] | None = None,
        normalize: bool | None = None,
        references: list[Any] | None = None,
        mp3_bitrate: Literal[64, 128, 192] | None = None,
        sample_rate: int | None = None,
        temperature: float | None = None,
        chunk_length: int | None = None,
        reference_id: str | None = None,
        max_new_tokens: int | None = None,
        min_chunk_length: int | None = None,
        repetition_penalty: float | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Fish Audio text-to-speech API — convert text into natural speech using a chosen voice model."""
        body: dict[str, Any] = {}
        body["text"] = text
        if top_p is not None:
            body["top_p"] = top_p
        if format is not None:
            body["format"] = format
        if latency is not None:
            body["latency"] = latency
        if prosody is not None:
            body["prosody"] = prosody
        if normalize is not None:
            body["normalize"] = normalize
        if references is not None:
            body["references"] = references
        if mp3_bitrate is not None:
            body["mp3_bitrate"] = mp3_bitrate
        if sample_rate is not None:
            body["sample_rate"] = sample_rate
        if temperature is not None:
            body["temperature"] = temperature
        if chunk_length is not None:
            body["chunk_length"] = chunk_length
        body["reference_id"] = reference_id if reference_id is not None else "d7900c21663f485ab63ebdb7e5905036"
        if max_new_tokens is not None:
            body["max_new_tokens"] = max_new_tokens
        if min_chunk_length is not None:
            body["min_chunk_length"] = min_chunk_length
        if repetition_penalty is not None:
            body["repetition_penalty"] = repetition_penalty
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        headers = {"model": model} if model is not None else None
        result = self._transport.request("POST", "/fish/tts", json=body, extra_headers=headers)
        handle = TaskHandle(_task_id(result), "/fish/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def models(
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
    ) -> dict[str, Any]:
        """Fish Audio model query API."""
        params = {
            "page_size": page_size,
            "page_number": page_number,
            "title": title,
            "tag": tag,
            "self": self_,
            "author_id": author_id,
            "language": language,
            "title_language": title_language,
            "sort_by": sort_by,
        }
        return self._transport.request("GET", "/fish/model", params={k: v for k, v in params.items() if v is not None})

    def get_model(self, id: str) -> dict[str, Any]:
        """Fish Audio model detail API."""
        return self._transport.request("GET", f"/fish/model/{id}")

    def model(
        self,
        *,
        title: str,
        voices: str,
        tags: list[str] | None = None,
        texts: list[str] | None = None,
        visibility: Literal["public", "private"] | None = None,
        cover_image: str | None = None,
        description: str | None = None,
        generate_sample: bool | None = None,
        enhance_audio_quality: bool | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Fish Audio model creation API — upload reference audio to create a custom voice-clone model."""
        body: dict[str, Any] = {}
        body["title"] = title
        body["voices"] = voices
        if tags is not None:
            body["tags"] = tags
        if texts is not None:
            body["texts"] = texts
        if visibility is not None:
            body["visibility"] = visibility
        if cover_image is not None:
            body["cover_image"] = cover_image
        if description is not None:
            body["description"] = description
        if generate_sample is not None:
            body["generate_sample"] = generate_sample
        if enhance_audio_quality is not None:
            body["enhance_audio_quality"] = enhance_audio_quality
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/fish/model", json=body)


class AsyncFish:
    """Asynchronous fish client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        text: str,
        model: Literal["s1", "s2-pro", "s2.1-pro"] | None = None,
        top_p: float | None = None,
        format: Literal["mp3", "wav", "pcm"] | None = None,
        latency: Literal["normal", "balanced"] | None = None,
        prosody: dict[str, Any] | None = None,
        normalize: bool | None = None,
        references: list[Any] | None = None,
        mp3_bitrate: Literal[64, 128, 192] | None = None,
        sample_rate: int | None = None,
        temperature: float | None = None,
        chunk_length: int | None = None,
        reference_id: str | None = None,
        max_new_tokens: int | None = None,
        min_chunk_length: int | None = None,
        repetition_penalty: float | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Fish Audio text-to-speech API — convert text into natural speech using a chosen voice model."""
        body: dict[str, Any] = {}
        body["text"] = text
        if top_p is not None:
            body["top_p"] = top_p
        if format is not None:
            body["format"] = format
        if latency is not None:
            body["latency"] = latency
        if prosody is not None:
            body["prosody"] = prosody
        if normalize is not None:
            body["normalize"] = normalize
        if references is not None:
            body["references"] = references
        if mp3_bitrate is not None:
            body["mp3_bitrate"] = mp3_bitrate
        if sample_rate is not None:
            body["sample_rate"] = sample_rate
        if temperature is not None:
            body["temperature"] = temperature
        if chunk_length is not None:
            body["chunk_length"] = chunk_length
        body["reference_id"] = reference_id if reference_id is not None else "d7900c21663f485ab63ebdb7e5905036"
        if max_new_tokens is not None:
            body["max_new_tokens"] = max_new_tokens
        if min_chunk_length is not None:
            body["min_chunk_length"] = min_chunk_length
        if repetition_penalty is not None:
            body["repetition_penalty"] = repetition_penalty
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        headers = {"model": model} if model is not None else None
        result = await self._transport.request("POST", "/fish/tts", json=body, extra_headers=headers)
        handle = AsyncTaskHandle(_task_id(result), "/fish/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def models(
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
    ) -> dict[str, Any]:
        """Fish Audio model query API."""
        params = {
            "page_size": page_size,
            "page_number": page_number,
            "title": title,
            "tag": tag,
            "self": self_,
            "author_id": author_id,
            "language": language,
            "title_language": title_language,
            "sort_by": sort_by,
        }
        return await self._transport.request(
            "GET", "/fish/model", params={k: v for k, v in params.items() if v is not None}
        )

    async def get_model(self, id: str) -> dict[str, Any]:
        """Fish Audio model detail API."""
        return await self._transport.request("GET", f"/fish/model/{id}")

    async def model(
        self,
        *,
        title: str,
        voices: str,
        tags: list[str] | None = None,
        texts: list[str] | None = None,
        visibility: Literal["public", "private"] | None = None,
        cover_image: str | None = None,
        description: str | None = None,
        generate_sample: bool | None = None,
        enhance_audio_quality: bool | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Fish Audio model creation API — upload reference audio to create a custom voice-clone model."""
        body: dict[str, Any] = {}
        body["title"] = title
        body["voices"] = voices
        if tags is not None:
            body["tags"] = tags
        if texts is not None:
            body["texts"] = texts
        if visibility is not None:
            body["visibility"] = visibility
        if cover_image is not None:
            body["cover_image"] = cover_image
        if description is not None:
            body["description"] = description
        if generate_sample is not None:
            body["generate_sample"] = generate_sample
        if enhance_audio_quality is not None:
            body["enhance_audio_quality"] = enhance_audio_quality
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/fish/model", json=body)
