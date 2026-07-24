"""Producer Music Generation resources."""

from __future__ import annotations

from typing import Any, Literal

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


class _ProducerTasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def retrieve(
        self,
        *,
        id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve", **kwargs}
        if id is not None:
            body["id"] = id
        return self._transport.request("POST", "/producer/tasks", json=body)

    def retrieve_batch(
        self,
        *,
        ids: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve_batch", **kwargs}
        if ids is not None:
            body["ids"] = ids
        return self._transport.request("POST", "/producer/tasks", json=body)


class _AsyncProducerTasks:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def retrieve(
        self,
        *,
        id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve", **kwargs}
        if id is not None:
            body["id"] = id
        return await self._transport.request("POST", "/producer/tasks", json=body)

    async def retrieve_batch(
        self,
        *,
        ids: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"action": "retrieve_batch", **kwargs}
        if ids is not None:
            body["ids"] = ids
        return await self._transport.request("POST", "/producer/tasks", json=body)


class Producer:
    """Synchronous Producer Music Generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.tasks = _ProducerTasks(transport)

    def generate(
        self,
        *,
        lyric: str,
        prompt: str,
        action: ProducerAction | str,
        model: ProducerModel | str | None = None,
        title: str | None = None,
        custom: bool | None = None,
        audio_id: str | None = None,
        continue_at: float | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        seed: str | None = None,
        instrumental: bool | None = None,
        sound_strength: float | None = None,
        lyrics_strength: float | None = None,
        weirdness: float | None = None,
        replace_section_end: float | None = None,
        replace_section_start: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"lyric": lyric, "prompt": prompt, "action": action, **kwargs}
        if model is not None:
            body["model"] = model
        if title is not None:
            body["title"] = title
        if custom is not None:
            body["custom"] = custom
        if audio_id is not None:
            body["audio_id"] = audio_id
        if continue_at is not None:
            body["continue_at"] = continue_at
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        if seed is not None:
            body["seed"] = seed
        if instrumental is not None:
            body["instrumental"] = instrumental
        if sound_strength is not None:
            body["sound_strength"] = sound_strength
        if lyrics_strength is not None:
            body["lyrics_strength"] = lyrics_strength
        if weirdness is not None:
            body["weirdness"] = weirdness
        if replace_section_end is not None:
            body["replace_section_end"] = replace_section_end
        if replace_section_start is not None:
            body["replace_section_start"] = replace_section_start
        return self._transport.request("POST", "/producer/audios", json=body)

    def upload(
        self,
        *,
        audio_url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        return self._transport.request("POST", "/producer/upload", json=body)

    def videos(
        self,
        *,
        audio_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return self._transport.request("POST", "/producer/videos", json=body)

    def wav(
        self,
        *,
        audio_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return self._transport.request("POST", "/producer/wav", json=body)

    def lyrics(
        self,
        *,
        prompt: dict[str, Any],
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return self._transport.request("POST", "/producer/lyrics", json=body)


class AsyncProducer:
    """Async Producer Music Generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport
        self.tasks = _AsyncProducerTasks(transport)

    async def generate(
        self,
        *,
        lyric: str,
        prompt: str,
        action: ProducerAction | str,
        model: ProducerModel | str | None = None,
        title: str | None = None,
        custom: bool | None = None,
        audio_id: str | None = None,
        continue_at: float | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        seed: str | None = None,
        instrumental: bool | None = None,
        sound_strength: float | None = None,
        lyrics_strength: float | None = None,
        weirdness: float | None = None,
        replace_section_end: float | None = None,
        replace_section_start: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"lyric": lyric, "prompt": prompt, "action": action, **kwargs}
        if model is not None:
            body["model"] = model
        if title is not None:
            body["title"] = title
        if custom is not None:
            body["custom"] = custom
        if audio_id is not None:
            body["audio_id"] = audio_id
        if continue_at is not None:
            body["continue_at"] = continue_at
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        if seed is not None:
            body["seed"] = seed
        if instrumental is not None:
            body["instrumental"] = instrumental
        if sound_strength is not None:
            body["sound_strength"] = sound_strength
        if lyrics_strength is not None:
            body["lyrics_strength"] = lyrics_strength
        if weirdness is not None:
            body["weirdness"] = weirdness
        if replace_section_end is not None:
            body["replace_section_end"] = replace_section_end
        if replace_section_start is not None:
            body["replace_section_start"] = replace_section_start
        return await self._transport.request("POST", "/producer/audios", json=body)

    async def upload(
        self,
        *,
        audio_url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        return await self._transport.request("POST", "/producer/upload", json=body)

    async def videos(
        self,
        *,
        audio_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return await self._transport.request("POST", "/producer/videos", json=body)

    async def wav(
        self,
        *,
        audio_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return await self._transport.request("POST", "/producer/wav", json=body)

    async def lyrics(
        self,
        *,
        prompt: dict[str, Any],
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return await self._transport.request("POST", "/producer/lyrics", json=body)
