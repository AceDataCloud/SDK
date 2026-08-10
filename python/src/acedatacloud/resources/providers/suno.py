"""Suno (suno) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

SunoModel = Literal[
    "chirp-v5-5",
    "chirp-v5",
    "chirp-v4-5-plus",
    "chirp-v4-5",
    "chirp-v4",
    "chirp-v3-5",
    "chirp-v3-0",
]
SunoAction = Literal[
    "generate",
    "extend",
    "upload_extend",
    "upload_cover",
    "concat",
    "cover",
    "artist_consistency",
    "artist_consistency_vox",
    "stems",
    "all_stems",
    "replace_section",
    "underpainting",
    "overpainting",
    "remaster",
    "mashup",
    "samples",
    "inspo",
]
SunoLyricsModel = Literal["default", "remi-v1"]


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


class Suno:
    """Synchronous suno client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        lyric: str | None = None,
        model: SunoModel | None = None,
        style: str | None = None,
        title: str | None = None,
        action: SunoAction | None = None,
        custom: bool | None = None,
        prompt: str | None = None,
        audio_id: str | None = None,
        duration: int | None = None,
        weirdness: float | None = None,
        audio_urls: list[str] | None = None,
        persona_id: str | None = None,
        continue_at: float | None = None,
        samples_end: float | None = None,
        audio_weight: float | None = None,
        instrumental: bool | None = None,
        lyric_prompt: str | None = None,
        vocal_gender: str | None = None,
        samples_start: float | None = None,
        negative_tags: str | None = None,
        style_influence: float | None = None,
        mashup_audio_ids: list[str] | None = None,
        overpainting_end: float | None = None,
        underpainting_end: float | None = None,
        overpainting_start: float | None = None,
        variation_category: str | None = None,
        replace_section_end: float | None = None,
        underpainting_start: float | None = None,
        replace_section_start: float | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Suno AI music generation API, generates 2 songs per request with extension support."""
        body: dict[str, Any] = {}
        if lyric is not None:
            body["lyric"] = lyric
        body["model"] = model if model is not None else "chirp-v5-5"
        if style is not None:
            body["style"] = style
        if title is not None:
            body["title"] = title
        body["action"] = action if action is not None else "generate"
        if custom is not None:
            body["custom"] = custom
        body["prompt"] = prompt if prompt is not None else "A song for Christmas"
        if audio_id is not None:
            body["audio_id"] = audio_id
        if duration is not None:
            body["duration"] = duration
        if weirdness is not None:
            body["weirdness"] = weirdness
        body["audio_urls"] = (
            audio_urls if audio_urls is not None else ["https://cdn1.suno.ai/b481b17a-bf50-4e10-8adc-4d5635050893.mp3"]
        )
        if persona_id is not None:
            body["persona_id"] = persona_id
        if continue_at is not None:
            body["continue_at"] = continue_at
        if samples_end is not None:
            body["samples_end"] = samples_end
        if audio_weight is not None:
            body["audio_weight"] = audio_weight
        if instrumental is not None:
            body["instrumental"] = instrumental
        if lyric_prompt is not None:
            body["lyric_prompt"] = lyric_prompt
        if vocal_gender is not None:
            body["vocal_gender"] = vocal_gender
        if samples_start is not None:
            body["samples_start"] = samples_start
        if negative_tags is not None:
            body["negative_tags"] = negative_tags
        if style_influence is not None:
            body["style_influence"] = style_influence
        if mashup_audio_ids is not None:
            body["mashup_audio_ids"] = mashup_audio_ids
        if overpainting_end is not None:
            body["overpainting_end"] = overpainting_end
        if underpainting_end is not None:
            body["underpainting_end"] = underpainting_end
        if overpainting_start is not None:
            body["overpainting_start"] = overpainting_start
        if variation_category is not None:
            body["variation_category"] = variation_category
        if replace_section_end is not None:
            body["replace_section_end"] = replace_section_end
        if underpainting_start is not None:
            body["underpainting_start"] = underpainting_start
        if replace_section_start is not None:
            body["replace_section_start"] = replace_section_start
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/suno/audios", json=body)
        handle = TaskHandle(_task_id(result), "/suno/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def persona(
        self,
        *,
        name: str,
        audio_id: str,
        vocal_end: float | None = None,
        description: str | None = None,
        vocal_start: float | None = None,
        vox_audio_id: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno singer style API, set song style based on a generated song ID."""
        body: dict[str, Any] = {}
        body["name"] = name
        body["audio_id"] = audio_id
        if vocal_end is not None:
            body["vocal_end"] = vocal_end
        if description is not None:
            body["description"] = description
        if vocal_start is not None:
            body["vocal_start"] = vocal_start
        if vox_audio_id is not None:
            body["vox_audio_id"] = vox_audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/suno/persona", json=body)

    def list_persona(
        self,
        *,
        user_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Suno singer style API, list singer styles for a user."""
        params: dict[str, Any] = {"user_id": user_id}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._transport.request("GET", "/suno/persona", params=params)

    def delete_persona(
        self,
        *,
        persona_id: str,
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """Suno singer style API, delete a singer style."""
        params: dict[str, Any] = {"persona_id": persona_id}
        if user_id is not None:
            params["user_id"] = user_id
        return self._transport.request("DELETE", "/suno/persona", params=params)

    def mp4(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno MP4 API, get MP4 file link via audio_id."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/suno/mp4", json=body)

    def voices(
        self,
        *,
        audio_url: str,
        name: str | None = None,
        description: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno Voice Clone API. Create a custom voice persona from an uploaded audio file for voice cloning in music
        generation.
        """
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/suno/voices", json=body)

    def timing(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno timeline API, get lyrics and audio timeline of generated music."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/suno/timing", json=body)

    def vox(
        self,
        *,
        audio_id: str,
        vocal_end: float | None = None,
        vocal_start: float | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Suno vocal/instrumental stems API. Pass an audio_id to asynchronously produce vocal-only and
        instrumental-only stem files for remixing and creative reuse.
        """
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        if vocal_end is not None:
            body["vocal_end"] = vocal_end
        if vocal_start is not None:
            body["vocal_start"] = vocal_start
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/suno/vox", json=body)
        handle = TaskHandle(_task_id(result), "/suno/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def wav(
        self,
        *,
        audio_id: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """SUNO allows generating higher quality wav files based on the existing audio_id."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/suno/wav", json=body)
        handle = TaskHandle(_task_id(result), "/suno/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def midi(
        self,
        *,
        audio_id: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Suno MIDI API, retrieve MIDI data from generated music."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/suno/midi", json=body)
        handle = TaskHandle(_task_id(result), "/suno/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def style(
        self,
        *,
        prompt: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """SUNO allows us to input prompts to generate enhanced song styles."""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/suno/style", json=body)

    def lyrics(
        self,
        *,
        model: SunoLyricsModel,
        prompt: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno lyrics generation API. Generates structured song lyrics from a prompt; supports the default and
        remi-v1 models.
        """
        body: dict[str, Any] = {}
        body["model"] = model
        body["prompt"] = prompt
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/suno/lyrics", json=body)

    def mashup_lyrics(
        self,
        *,
        lyrics_a: str,
        lyrics_b: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno mashup lyrics API, merge two lyrics into a blended version."""
        body: dict[str, Any] = {}
        body["lyrics_a"] = lyrics_a
        body["lyrics_b"] = lyrics_b
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/suno/mashup-lyrics", json=body)

    def upload(
        self,
        *,
        audio_url: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno reference audio upload API, upload audio to get an audio_id for extended generation."""
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/suno/upload", json=body)


class AsyncSuno:
    """Asynchronous suno client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        lyric: str | None = None,
        model: SunoModel | None = None,
        style: str | None = None,
        title: str | None = None,
        action: SunoAction | None = None,
        custom: bool | None = None,
        prompt: str | None = None,
        audio_id: str | None = None,
        duration: int | None = None,
        weirdness: float | None = None,
        audio_urls: list[str] | None = None,
        persona_id: str | None = None,
        continue_at: float | None = None,
        samples_end: float | None = None,
        audio_weight: float | None = None,
        instrumental: bool | None = None,
        lyric_prompt: str | None = None,
        vocal_gender: str | None = None,
        samples_start: float | None = None,
        negative_tags: str | None = None,
        style_influence: float | None = None,
        mashup_audio_ids: list[str] | None = None,
        overpainting_end: float | None = None,
        underpainting_end: float | None = None,
        overpainting_start: float | None = None,
        variation_category: str | None = None,
        replace_section_end: float | None = None,
        underpainting_start: float | None = None,
        replace_section_start: float | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Suno AI music generation API, generates 2 songs per request with extension support."""
        body: dict[str, Any] = {}
        if lyric is not None:
            body["lyric"] = lyric
        body["model"] = model if model is not None else "chirp-v5-5"
        if style is not None:
            body["style"] = style
        if title is not None:
            body["title"] = title
        body["action"] = action if action is not None else "generate"
        if custom is not None:
            body["custom"] = custom
        body["prompt"] = prompt if prompt is not None else "A song for Christmas"
        if audio_id is not None:
            body["audio_id"] = audio_id
        if duration is not None:
            body["duration"] = duration
        if weirdness is not None:
            body["weirdness"] = weirdness
        body["audio_urls"] = (
            audio_urls if audio_urls is not None else ["https://cdn1.suno.ai/b481b17a-bf50-4e10-8adc-4d5635050893.mp3"]
        )
        if persona_id is not None:
            body["persona_id"] = persona_id
        if continue_at is not None:
            body["continue_at"] = continue_at
        if samples_end is not None:
            body["samples_end"] = samples_end
        if audio_weight is not None:
            body["audio_weight"] = audio_weight
        if instrumental is not None:
            body["instrumental"] = instrumental
        if lyric_prompt is not None:
            body["lyric_prompt"] = lyric_prompt
        if vocal_gender is not None:
            body["vocal_gender"] = vocal_gender
        if samples_start is not None:
            body["samples_start"] = samples_start
        if negative_tags is not None:
            body["negative_tags"] = negative_tags
        if style_influence is not None:
            body["style_influence"] = style_influence
        if mashup_audio_ids is not None:
            body["mashup_audio_ids"] = mashup_audio_ids
        if overpainting_end is not None:
            body["overpainting_end"] = overpainting_end
        if underpainting_end is not None:
            body["underpainting_end"] = underpainting_end
        if overpainting_start is not None:
            body["overpainting_start"] = overpainting_start
        if variation_category is not None:
            body["variation_category"] = variation_category
        if replace_section_end is not None:
            body["replace_section_end"] = replace_section_end
        if underpainting_start is not None:
            body["underpainting_start"] = underpainting_start
        if replace_section_start is not None:
            body["replace_section_start"] = replace_section_start
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/suno/audios", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/suno/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def persona(
        self,
        *,
        name: str,
        audio_id: str,
        vocal_end: float | None = None,
        description: str | None = None,
        vocal_start: float | None = None,
        vox_audio_id: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno singer style API, set song style based on a generated song ID."""
        body: dict[str, Any] = {}
        body["name"] = name
        body["audio_id"] = audio_id
        if vocal_end is not None:
            body["vocal_end"] = vocal_end
        if description is not None:
            body["description"] = description
        if vocal_start is not None:
            body["vocal_start"] = vocal_start
        if vox_audio_id is not None:
            body["vox_audio_id"] = vox_audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/suno/persona", json=body)

    async def list_persona(
        self,
        *,
        user_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Suno singer style API, list singer styles for a user."""
        params: dict[str, Any] = {"user_id": user_id}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return await self._transport.request("GET", "/suno/persona", params=params)

    async def delete_persona(
        self,
        *,
        persona_id: str,
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """Suno singer style API, delete a singer style."""
        params: dict[str, Any] = {"persona_id": persona_id}
        if user_id is not None:
            params["user_id"] = user_id
        return await self._transport.request("DELETE", "/suno/persona", params=params)

    async def mp4(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno MP4 API, get MP4 file link via audio_id."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/suno/mp4", json=body)

    async def voices(
        self,
        *,
        audio_url: str,
        name: str | None = None,
        description: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno Voice Clone API. Create a custom voice persona from an uploaded audio file for voice cloning in music
        generation.
        """
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/suno/voices", json=body)

    async def timing(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno timeline API, get lyrics and audio timeline of generated music."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/suno/timing", json=body)

    async def vox(
        self,
        *,
        audio_id: str,
        vocal_end: float | None = None,
        vocal_start: float | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Suno vocal/instrumental stems API. Pass an audio_id to asynchronously produce vocal-only and
        instrumental-only stem files for remixing and creative reuse.
        """
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        if vocal_end is not None:
            body["vocal_end"] = vocal_end
        if vocal_start is not None:
            body["vocal_start"] = vocal_start
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/suno/vox", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/suno/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def wav(
        self,
        *,
        audio_id: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """SUNO allows generating higher quality wav files based on the existing audio_id."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/suno/wav", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/suno/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def midi(
        self,
        *,
        audio_id: str,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Suno MIDI API, retrieve MIDI data from generated music."""
        body: dict[str, Any] = {}
        body["audio_id"] = audio_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/suno/midi", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/suno/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def style(
        self,
        *,
        prompt: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """SUNO allows us to input prompts to generate enhanced song styles."""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/suno/style", json=body)

    async def lyrics(
        self,
        *,
        model: SunoLyricsModel,
        prompt: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno lyrics generation API. Generates structured song lyrics from a prompt; supports the default and
        remi-v1 models.
        """
        body: dict[str, Any] = {}
        body["model"] = model
        body["prompt"] = prompt
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/suno/lyrics", json=body)

    async def mashup_lyrics(
        self,
        *,
        lyrics_a: str,
        lyrics_b: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno mashup lyrics API, merge two lyrics into a blended version."""
        body: dict[str, Any] = {}
        body["lyrics_a"] = lyrics_a
        body["lyrics_b"] = lyrics_b
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/suno/mashup-lyrics", json=body)

    async def upload(
        self,
        *,
        audio_url: str,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Suno reference audio upload API, upload audio to get an audio_id for extended generation."""
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/suno/upload", json=body)
