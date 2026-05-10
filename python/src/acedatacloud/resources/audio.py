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
        text: str | None = None,
        provider: AudioProvider | str = "suno",
        model: str | None = None,
        tags: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        is_fish = provider == "fish"
        body: dict[str, Any] = {**kwargs}
        if is_fish:
            body["text"] = text or prompt
        else:
            body["prompt"] = prompt
        extra_headers: dict[str, str] = {}
        if model is not None:
            if is_fish:
                extra_headers["model"] = model
            else:
                body["model"] = model
        if tags is not None:
            body["tags"] = tags
        if callback_url is not None:
            body["callback_url"] = callback_url

        endpoint = "/fish/tts" if is_fish else f"/{provider}/audios"
        result = self._transport.request("POST", endpoint, json=body, extra_headers=extra_headers)
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

    async def generate(
        self,
        *,
        prompt: str,
        text: str | None = None,
        provider: AudioProvider | str = "suno",
        model: str | None = None,
        tags: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        is_fish = provider == "fish"
        body: dict[str, Any] = {**kwargs}
        if is_fish:
            body["text"] = text or prompt
        else:
            body["prompt"] = prompt
        extra_headers: dict[str, str] = {}
        if model is not None:
            if is_fish:
                extra_headers["model"] = model
            else:
                body["model"] = model
        if tags is not None:
            body["tags"] = tags
        if callback_url is not None:
            body["callback_url"] = callback_url

        endpoint = "/fish/tts" if is_fish else f"/{provider}/audios"
        result = await self._transport.request("POST", endpoint, json=body, extra_headers=extra_headers)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
