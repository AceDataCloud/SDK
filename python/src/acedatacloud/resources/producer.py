"""Producer music generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

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


class Producer:
    """Synchronous Producer music generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: str,
        lyric: str,
        prompt: str,
        model: str | None = None,
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
        replace_section_start: float | None = None,
        replace_section_end: float | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"action": action, "lyric": lyric, "prompt": prompt, **kwargs}
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
        if replace_section_start is not None:
            body["replace_section_start"] = replace_section_start
        if replace_section_end is not None:
            body["replace_section_end"] = replace_section_end
        result = self._transport.request("POST", "/producer/audios", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = TaskHandle(task_id, "/producer/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def upload(self, *, audio_url: str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        return self._transport.request("POST", "/producer/upload", json=body)

    def videos(self, *, audio_id: str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return self._transport.request("POST", "/producer/videos", json=body)

    def wav(self, *, audio_id: str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return self._transport.request("POST", "/producer/wav", json=body)

    def lyrics(self, *, prompt: dict[str, Any] | str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return self._transport.request("POST", "/producer/lyrics", json=body)


class AsyncProducer:
    """Async Producer music generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: str,
        lyric: str,
        prompt: str,
        model: str | None = None,
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
        replace_section_start: float | None = None,
        replace_section_end: float | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"action": action, "lyric": lyric, "prompt": prompt, **kwargs}
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
        if replace_section_start is not None:
            body["replace_section_start"] = replace_section_start
        if replace_section_end is not None:
            body["replace_section_end"] = replace_section_end
        result = await self._transport.request("POST", "/producer/audios", json=body)
        task_id = result.get("task_id")
        if not task_id or (result.get("data") and not wait):
            return result
        handle = AsyncTaskHandle(task_id, "/producer/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def upload(self, *, audio_url: str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_url": audio_url, **kwargs}
        return await self._transport.request("POST", "/producer/upload", json=body)

    async def videos(self, *, audio_id: str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return await self._transport.request("POST", "/producer/videos", json=body)

    async def wav(self, *, audio_id: str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"audio_id": audio_id, **kwargs}
        return await self._transport.request("POST", "/producer/wav", json=body)

    async def lyrics(self, *, prompt: dict[str, Any] | str, **kwargs: Any) -> dict[str, Any]:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        return await self._transport.request("POST", "/producer/lyrics", json=body)
