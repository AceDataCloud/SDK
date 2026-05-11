"""Audio/music generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

AudioProvider = Literal["suno", "producer", "fish"]


class Audio:
    """Synchronous audio generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        provider: AudioProvider | str = "suno",
        model: str | None = None,
        text: str | None = None,
        reference_id: str | None = None,
        format: str | None = None,
        sample_rate: int | None = None,
        mp3_bitrate: int | None = None,
        opus_bitrate: int | None = None,
        latency: str | None = None,
        chunk_length: int | None = None,
        min_chunk_length: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        repetition_penalty: float | None = None,
        max_new_tokens: int | None = None,
        normalize: bool | None = None,
        prosody: dict[str, Any] | None = None,
        references: list[dict[str, Any]] | None = None,
        tags: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        """Generate audio; for Fish TTS, ``prompt`` is a backward-compatible alias of ``text``."""
        body: dict[str, Any] = {}
        endpoint = f"/{provider}/audios"
        extra_headers: dict[str, str] | None = None
        if provider == "fish":
            endpoint = "/fish/tts"
            body = {"text": text or prompt, **kwargs}
            if reference_id is not None:
                body["reference_id"] = reference_id
            if format is not None:
                body["format"] = format
            if sample_rate is not None:
                body["sample_rate"] = sample_rate
            if mp3_bitrate is not None:
                body["mp3_bitrate"] = mp3_bitrate
            if opus_bitrate is not None:
                body["opus_bitrate"] = opus_bitrate
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
            if callback_url is not None:
                body["callback_url"] = callback_url
            if model is not None:
                extra_headers = {"model": model}
        else:
            body = {"prompt": prompt, **kwargs}
            if model is not None:
                body["model"] = model
            if tags is not None:
                body["tags"] = tags
            if callback_url is not None:
                body["callback_url"] = callback_url

        result = self._transport.request("POST", endpoint, json=body, extra_headers=extra_headers)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = TaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def list_fish_models(self, **params: Any) -> dict[str, Any]:
        """List available Fish voice models."""
        return self._transport.request("GET", "/fish/model", params=params or None)

    def get_fish_model(self, model_id: str) -> dict[str, Any]:
        """Get details for a Fish voice model."""
        return self._transport.request("GET", f"/fish/model/{model_id}")


class AsyncAudio:
    """Async audio generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        provider: AudioProvider | str = "suno",
        model: str | None = None,
        text: str | None = None,
        reference_id: str | None = None,
        format: str | None = None,
        sample_rate: int | None = None,
        mp3_bitrate: int | None = None,
        opus_bitrate: int | None = None,
        latency: str | None = None,
        chunk_length: int | None = None,
        min_chunk_length: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        repetition_penalty: float | None = None,
        max_new_tokens: int | None = None,
        normalize: bool | None = None,
        prosody: dict[str, Any] | None = None,
        references: list[dict[str, Any]] | None = None,
        tags: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        """Generate audio; for Fish TTS, ``prompt`` is a backward-compatible alias of ``text``."""
        body: dict[str, Any] = {}
        endpoint = f"/{provider}/audios"
        extra_headers: dict[str, str] | None = None
        if provider == "fish":
            endpoint = "/fish/tts"
            body = {"text": text or prompt, **kwargs}
            if reference_id is not None:
                body["reference_id"] = reference_id
            if format is not None:
                body["format"] = format
            if sample_rate is not None:
                body["sample_rate"] = sample_rate
            if mp3_bitrate is not None:
                body["mp3_bitrate"] = mp3_bitrate
            if opus_bitrate is not None:
                body["opus_bitrate"] = opus_bitrate
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
            if callback_url is not None:
                body["callback_url"] = callback_url
            if model is not None:
                extra_headers = {"model": model}
        else:
            body = {"prompt": prompt, **kwargs}
            if model is not None:
                body["model"] = model
            if tags is not None:
                body["tags"] = tags
            if callback_url is not None:
                body["callback_url"] = callback_url

        result = await self._transport.request("POST", endpoint, json=body, extra_headers=extra_headers)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def list_fish_models(self, **params: Any) -> dict[str, Any]:
        """List available Fish voice models."""
        return await self._transport.request("GET", "/fish/model", params=params or None)

    async def get_fish_model(self, model_id: str) -> dict[str, Any]:
        """Get details for a Fish voice model."""
        return await self._transport.request("GET", f"/fish/model/{model_id}")
