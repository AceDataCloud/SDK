"""Suno-specific music generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

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


class Suno:
    """Synchronous Suno music generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        lyric: str | None = None,
        model: str | None = None,
        style: str | None = None,
        variation_category: str | None = None,
        title: str | None = None,
        action: str | None = None,
        custom: bool | None = None,
        prompt: Any | None = None,
        lyric_prompt: Any | None = None,
        audio_id: str | None = None,
        mashup_audio_ids: list[str] | None = None,
        audio_urls: list[str] | None = None,
        weirdness: float | None = None,
        persona_id: str | None = None,
        overpainting_start: float | None = None,
        overpainting_end: float | None = None,
        samples_start: float | None = None,
        samples_end: float | None = None,
        underpainting_start: float | None = None,
        underpainting_end: float | None = None,
        continue_at: float | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        instrumental: bool | None = None,
        vocal_gender: str | None = None,
        style_negative: str | None = None,
        style_influence: float | None = None,
        audio_weight: float | None = None,
        replace_section_end: float | None = None,
        replace_section_start: float | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {**kwargs}
        if lyric is not None:
            body["lyric"] = lyric
        if model is not None:
            body["model"] = model
        if style is not None:
            body["style"] = style
        if variation_category is not None:
            body["variation_category"] = variation_category
        if title is not None:
            body["title"] = title
        if action is not None:
            body["action"] = action
        if custom is not None:
            body["custom"] = custom
        if prompt is not None:
            body["prompt"] = prompt
        if lyric_prompt is not None:
            body["lyric_prompt"] = lyric_prompt
        if audio_id is not None:
            body["audio_id"] = audio_id
        if mashup_audio_ids is not None:
            body["mashup_audio_ids"] = mashup_audio_ids
        if audio_urls is not None:
            body["audio_urls"] = audio_urls
        if weirdness is not None:
            body["weirdness"] = weirdness
        if persona_id is not None:
            body["persona_id"] = persona_id
        if overpainting_start is not None:
            body["overpainting_start"] = overpainting_start
        if overpainting_end is not None:
            body["overpainting_end"] = overpainting_end
        if samples_start is not None:
            body["samples_start"] = samples_start
        if samples_end is not None:
            body["samples_end"] = samples_end
        if underpainting_start is not None:
            body["underpainting_start"] = underpainting_start
        if underpainting_end is not None:
            body["underpainting_end"] = underpainting_end
        if continue_at is not None:
            body["continue_at"] = continue_at
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        if instrumental is not None:
            body["instrumental"] = instrumental
        if vocal_gender is not None:
            body["vocal_gender"] = vocal_gender
        if style_negative is not None:
            body["style_negative"] = style_negative
        if style_influence is not None:
            body["style_influence"] = style_influence
        if audio_weight is not None:
            body["audio_weight"] = audio_weight
        if replace_section_end is not None:
            body["replace_section_end"] = replace_section_end
        if replace_section_start is not None:
            body["replace_section_start"] = replace_section_start
        result = self._transport.request("POST", "/suno/audios", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = TaskHandle(task_id, "/suno/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def create_persona(
        self,
        *,
        audio_id: str,
        name: str,
        vox_audio_id: str | None = None,
        vocal_start: float | None = None,
        vocal_end: float | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, "name": name, **kwargs}
        if vox_audio_id is not None:
            body["vox_audio_id"] = vox_audio_id
        if vocal_start is not None:
            body["vocal_start"] = vocal_start
        if vocal_end is not None:
            body["vocal_end"] = vocal_end
        if description is not None:
            body["description"] = description
        return self._transport.request("POST", "/suno/persona", json=body)

    def list_personas(
        self,
        *,
        user_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
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
        params: dict[str, Any] = {"persona_id": persona_id}
        if user_id is not None:
            params["user_id"] = user_id
        return self._transport.request("DELETE", "/suno/persona", params=params)

    def mp4(
        self,
        *,
        audio_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return self._transport.request("POST", "/suno/mp4", json=body)

    def voices(
        self,
        *,
        audio_url: str,
        name: str | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        return self._transport.request("POST", "/suno/voices", json=body)

    def timing(
        self,
        *,
        audio_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return self._transport.request("POST", "/suno/timing", json=body)

    def vox(
        self,
        *,
        audio_id: str,
        vocal_start: float | None = None,
        vocal_end: float | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        if vocal_start is not None:
            body["vocal_start"] = vocal_start
        if vocal_end is not None:
            body["vocal_end"] = vocal_end
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/suno/vox", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = TaskHandle(task_id, "/suno/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def wav(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/suno/wav", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = TaskHandle(task_id, "/suno/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def midi(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/suno/midi", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = TaskHandle(task_id, "/suno/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def style(
        self,
        *,
        prompt: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return self._transport.request("POST", "/suno/style", json=body)

    def lyrics(
        self,
        *,
        prompt: Any,
        model: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, "model": model, **kwargs}
        return self._transport.request("POST", "/suno/lyrics", json=body)

    def mashup_lyrics(
        self,
        *,
        lyrics_a: str,
        lyrics_b: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"lyrics_a": lyrics_a, "lyrics_b": lyrics_b, **kwargs}
        return self._transport.request("POST", "/suno/mashup-lyrics", json=body)

    def upload(
        self,
        *,
        audio_url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        return self._transport.request("POST", "/suno/upload", json=body)


class AsyncSuno:
    """Async Suno music generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        lyric: str | None = None,
        model: str | None = None,
        style: str | None = None,
        variation_category: str | None = None,
        title: str | None = None,
        action: str | None = None,
        custom: bool | None = None,
        prompt: Any | None = None,
        lyric_prompt: Any | None = None,
        audio_id: str | None = None,
        mashup_audio_ids: list[str] | None = None,
        audio_urls: list[str] | None = None,
        weirdness: float | None = None,
        persona_id: str | None = None,
        overpainting_start: float | None = None,
        overpainting_end: float | None = None,
        samples_start: float | None = None,
        samples_end: float | None = None,
        underpainting_start: float | None = None,
        underpainting_end: float | None = None,
        continue_at: float | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        instrumental: bool | None = None,
        vocal_gender: str | None = None,
        style_negative: str | None = None,
        style_influence: float | None = None,
        audio_weight: float | None = None,
        replace_section_end: float | None = None,
        replace_section_start: float | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {**kwargs}
        if lyric is not None:
            body["lyric"] = lyric
        if model is not None:
            body["model"] = model
        if style is not None:
            body["style"] = style
        if variation_category is not None:
            body["variation_category"] = variation_category
        if title is not None:
            body["title"] = title
        if action is not None:
            body["action"] = action
        if custom is not None:
            body["custom"] = custom
        if prompt is not None:
            body["prompt"] = prompt
        if lyric_prompt is not None:
            body["lyric_prompt"] = lyric_prompt
        if audio_id is not None:
            body["audio_id"] = audio_id
        if mashup_audio_ids is not None:
            body["mashup_audio_ids"] = mashup_audio_ids
        if audio_urls is not None:
            body["audio_urls"] = audio_urls
        if weirdness is not None:
            body["weirdness"] = weirdness
        if persona_id is not None:
            body["persona_id"] = persona_id
        if overpainting_start is not None:
            body["overpainting_start"] = overpainting_start
        if overpainting_end is not None:
            body["overpainting_end"] = overpainting_end
        if samples_start is not None:
            body["samples_start"] = samples_start
        if samples_end is not None:
            body["samples_end"] = samples_end
        if underpainting_start is not None:
            body["underpainting_start"] = underpainting_start
        if underpainting_end is not None:
            body["underpainting_end"] = underpainting_end
        if continue_at is not None:
            body["continue_at"] = continue_at
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        if instrumental is not None:
            body["instrumental"] = instrumental
        if vocal_gender is not None:
            body["vocal_gender"] = vocal_gender
        if style_negative is not None:
            body["style_negative"] = style_negative
        if style_influence is not None:
            body["style_influence"] = style_influence
        if audio_weight is not None:
            body["audio_weight"] = audio_weight
        if replace_section_end is not None:
            body["replace_section_end"] = replace_section_end
        if replace_section_start is not None:
            body["replace_section_start"] = replace_section_start
        result = await self._transport.request("POST", "/suno/audios", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = AsyncTaskHandle(task_id, "/suno/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def create_persona(
        self,
        *,
        audio_id: str,
        name: str,
        vox_audio_id: str | None = None,
        vocal_start: float | None = None,
        vocal_end: float | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, "name": name, **kwargs}
        if vox_audio_id is not None:
            body["vox_audio_id"] = vox_audio_id
        if vocal_start is not None:
            body["vocal_start"] = vocal_start
        if vocal_end is not None:
            body["vocal_end"] = vocal_end
        if description is not None:
            body["description"] = description
        return await self._transport.request("POST", "/suno/persona", json=body)

    async def list_personas(
        self,
        *,
        user_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
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
        params: dict[str, Any] = {"persona_id": persona_id}
        if user_id is not None:
            params["user_id"] = user_id
        return await self._transport.request("DELETE", "/suno/persona", params=params)

    async def mp4(
        self,
        *,
        audio_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return await self._transport.request("POST", "/suno/mp4", json=body)

    async def voices(
        self,
        *,
        audio_url: str,
        name: str | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        return await self._transport.request("POST", "/suno/voices", json=body)

    async def timing(
        self,
        *,
        audio_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return await self._transport.request("POST", "/suno/timing", json=body)

    async def vox(
        self,
        *,
        audio_id: str,
        vocal_start: float | None = None,
        vocal_end: float | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        if vocal_start is not None:
            body["vocal_start"] = vocal_start
        if vocal_end is not None:
            body["vocal_end"] = vocal_end
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/suno/vox", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = AsyncTaskHandle(task_id, "/suno/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def wav(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/suno/wav", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = AsyncTaskHandle(task_id, "/suno/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def midi(
        self,
        *,
        audio_id: str,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/suno/midi", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = AsyncTaskHandle(task_id, "/suno/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def style(
        self,
        *,
        prompt: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return await self._transport.request("POST", "/suno/style", json=body)

    async def lyrics(
        self,
        *,
        prompt: Any,
        model: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, "model": model, **kwargs}
        return await self._transport.request("POST", "/suno/lyrics", json=body)

    async def mashup_lyrics(
        self,
        *,
        lyrics_a: str,
        lyrics_b: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"lyrics_a": lyrics_a, "lyrics_b": lyrics_b, **kwargs}
        return await self._transport.request("POST", "/suno/mashup-lyrics", json=body)

    async def upload(
        self,
        *,
        audio_url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        return await self._transport.request("POST", "/suno/upload", json=body)
