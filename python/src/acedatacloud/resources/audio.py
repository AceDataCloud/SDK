"""Audio/music generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

AudioProvider = Literal["suno", "producer", "fish"]


class Audio:
    """Synchronous audio generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def list_fish_models(
        self,
        *,
        page_size: int | None = None,
        page_number: int | None = None,
        title: str | None = None,
        tag: str | None = None,
        self_only: bool | None = None,
        author_id: str | None = None,
        language: str | None = None,
        title_language: str | None = None,
        sort_by: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page_size"] = page_size
        if page_number is not None:
            params["page_number"] = page_number
        if title is not None:
            params["title"] = title
        if tag is not None:
            params["tag"] = tag
        if self_only is not None:
            params["self"] = self_only
        if author_id is not None:
            params["author_id"] = author_id
        if language is not None:
            params["language"] = language
        if title_language is not None:
            params["title_language"] = title_language
        if sort_by is not None:
            params["sort_by"] = sort_by
        return self._transport.request("GET", "/fish/model", params=params)

    def get_fish_model(self, model_id: str) -> dict[str, Any]:
        return self._transport.request("GET", f"/fish/model/{model_id}")

    def generate(
        self,
        *,
        prompt: str | dict[str, Any],
        provider: AudioProvider | str = "suno",
        model: str | None = None,
        tags: str | None = None,
        lyric: str | None = None,
        style: str | None = None,
        variation_category: str | None = None,
        title: str | None = None,
        action: str | None = None,
        custom: bool | None = None,
        lyric_prompt: str | dict[str, Any] | None = None,
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
        if provider == "fish":
            body: dict[str, Any] = {"text": prompt, **kwargs}
            if callback_url is not None:
                body["callback_url"] = callback_url
            if async_ is not None:
                body["async"] = async_
            result = self._transport.request(
                "POST",
                "/fish/tts",
                json=body,
                extra_headers={"model": model} if model is not None else {},
            )
        else:
            body = {"prompt": prompt, **kwargs}
            if model is not None:
                body["model"] = model
            if tags is not None:
                body["tags"] = tags
            if lyric is not None:
                body["lyric"] = lyric
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
            result = self._transport.request("POST", f"/{provider}/audios", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = TaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncAudio:
    """Async audio generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def list_fish_models(
        self,
        *,
        page_size: int | None = None,
        page_number: int | None = None,
        title: str | None = None,
        tag: str | None = None,
        self_only: bool | None = None,
        author_id: str | None = None,
        language: str | None = None,
        title_language: str | None = None,
        sort_by: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page_size"] = page_size
        if page_number is not None:
            params["page_number"] = page_number
        if title is not None:
            params["title"] = title
        if tag is not None:
            params["tag"] = tag
        if self_only is not None:
            params["self"] = self_only
        if author_id is not None:
            params["author_id"] = author_id
        if language is not None:
            params["language"] = language
        if title_language is not None:
            params["title_language"] = title_language
        if sort_by is not None:
            params["sort_by"] = sort_by
        return await self._transport.request("GET", "/fish/model", params=params)

    async def get_fish_model(self, model_id: str) -> dict[str, Any]:
        return await self._transport.request("GET", f"/fish/model/{model_id}")

    async def generate(
        self,
        *,
        prompt: str | dict[str, Any],
        provider: AudioProvider | str = "suno",
        model: str | None = None,
        tags: str | None = None,
        lyric: str | None = None,
        style: str | None = None,
        variation_category: str | None = None,
        title: str | None = None,
        action: str | None = None,
        custom: bool | None = None,
        lyric_prompt: str | dict[str, Any] | None = None,
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
        if provider == "fish":
            body: dict[str, Any] = {"text": prompt, **kwargs}
            if callback_url is not None:
                body["callback_url"] = callback_url
            if async_ is not None:
                body["async"] = async_
            result = await self._transport.request(
                "POST",
                "/fish/tts",
                json=body,
                extra_headers={"model": model} if model is not None else {},
            )
        else:
            body = {"prompt": prompt, **kwargs}
            if model is not None:
                body["model"] = model
            if tags is not None:
                body["tags"] = tags
            if lyric is not None:
                body["lyric"] = lyric
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
            result = await self._transport.request("POST", f"/{provider}/audios", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
