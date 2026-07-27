"""Producer (producer) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

ProducerModel = Literal[
    "FUZZ-2.0 Pro",
    "FUZZ-2.0",
    "FUZZ-2.0 Raw",
    "FUZZ-1.1 Pro",
    "FUZZ-1.0 Pro",
    "FUZZ-1.0",
    "FUZZ-1.1",
    "FUZZ-0.8",
]
ProducerAction = Literal[
    "generate",
    "cover",
    "extend",
    "variation",
    "swap_vocals",
    "swap_instrumentals",
    "replace_section",
    "stems",
]


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


class Producer:
    """Synchronous producer client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def upload(
        self,
        *,
        audio_url: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Producer reference audio upload API, upload audio to get an audio_id for generation."""
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/producer/upload", json=body)

    def generate(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """AceData Producer MP4 retrieval API. Pass an audio_id to receive an MP4 video download link with cover art."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/producer/videos", json=body)

    def wav(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """AceData Producer WAV (lossless) retrieval API. Pass an audio_id to receive a WAV-format download link."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/producer/wav", json=body)

    def producer_audios(
        self,
        *,
        lyric: str,
        action: ProducerAction,
        prompt: str,
        seed: str | None = None,
        model: ProducerModel | None = None,
        title: str | None = None,
        custom: bool | None = None,
        audio_id: str | None = None,
        weirdness: float | None = None,
        continue_at: float | None = None,
        instrumental: bool | None = None,
        sound_strength: float | None = None,
        lyrics_strength: float | None = None,
        replace_section_end: float | None = None,
        replace_section_start: float | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Producer AI music generation API, generates 1 song per request."""
        body: dict[str, Any] = {}
        body["lyric"] = lyric
        body["action"] = action
        body["prompt"] = prompt
        if seed is not None:
            body["seed"] = seed
        if model is not None:
            body["model"] = model
        if title is not None:
            body["title"] = title
        if custom is not None:
            body["custom"] = custom
        if audio_id is not None:
            body["audio_id"] = audio_id
        body["weirdness"] = weirdness if weirdness is not None else False
        body["continue_at"] = continue_at if continue_at is not None else False
        body["instrumental"] = instrumental if instrumental is not None else False
        body["sound_strength"] = sound_strength if sound_strength is not None else False
        body["lyrics_strength"] = lyrics_strength if lyrics_strength is not None else False
        body["replace_section_end"] = replace_section_end if replace_section_end is not None else False
        body["replace_section_start"] = replace_section_start if replace_section_start is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/producer/audios", json=body)
        handle = TaskHandle(_task_id(result), "/producer/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def lyrics(
        self,
        *,
        prompt: dict[str, Any],
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Producer AI lyrics generation API, input a prompt to generate lyrics."""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/producer/lyrics", json=body)


class AsyncProducer:
    """Asynchronous producer client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def upload(
        self,
        *,
        audio_url: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Producer reference audio upload API, upload audio to get an audio_id for generation."""
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/producer/upload", json=body)

    async def generate(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """AceData Producer MP4 retrieval API. Pass an audio_id to receive an MP4 video download link with cover art."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/producer/videos", json=body)

    async def wav(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """AceData Producer WAV (lossless) retrieval API. Pass an audio_id to receive a WAV-format download link."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/producer/wav", json=body)

    async def producer_audios(
        self,
        *,
        lyric: str,
        action: ProducerAction,
        prompt: str,
        seed: str | None = None,
        model: ProducerModel | None = None,
        title: str | None = None,
        custom: bool | None = None,
        audio_id: str | None = None,
        weirdness: float | None = None,
        continue_at: float | None = None,
        instrumental: bool | None = None,
        sound_strength: float | None = None,
        lyrics_strength: float | None = None,
        replace_section_end: float | None = None,
        replace_section_start: float | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Producer AI music generation API, generates 1 song per request."""
        body: dict[str, Any] = {}
        body["lyric"] = lyric
        body["action"] = action
        body["prompt"] = prompt
        if seed is not None:
            body["seed"] = seed
        if model is not None:
            body["model"] = model
        if title is not None:
            body["title"] = title
        if custom is not None:
            body["custom"] = custom
        if audio_id is not None:
            body["audio_id"] = audio_id
        body["weirdness"] = weirdness if weirdness is not None else False
        body["continue_at"] = continue_at if continue_at is not None else False
        body["instrumental"] = instrumental if instrumental is not None else False
        body["sound_strength"] = sound_strength if sound_strength is not None else False
        body["lyrics_strength"] = lyrics_strength if lyrics_strength is not None else False
        body["replace_section_end"] = replace_section_end if replace_section_end is not None else False
        body["replace_section_start"] = replace_section_start if replace_section_start is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/producer/audios", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/producer/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def lyrics(
        self,
        *,
        prompt: dict[str, Any],
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Producer AI lyrics generation API, input a prompt to generate lyrics."""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/producer/lyrics", json=body)
