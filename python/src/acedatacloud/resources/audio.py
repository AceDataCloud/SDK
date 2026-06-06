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
        prompt: str,
        provider: AudioProvider | str = "suno",
        model: str | None = None,
        tags: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        if provider == "fish":
            body: dict[str, Any] = {"text": prompt, **kwargs}
            if callback_url is not None:
                body["callback_url"] = callback_url
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
            if callback_url is not None:
                body["callback_url"] = callback_url
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
        prompt: str,
        provider: AudioProvider | str = "suno",
        model: str | None = None,
        tags: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        if provider == "fish":
            body: dict[str, Any] = {"text": prompt, **kwargs}
            if callback_url is not None:
                body["callback_url"] = callback_url
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
            if callback_url is not None:
                body["callback_url"] = callback_url
            result = await self._transport.request("POST", f"/{provider}/audios", json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
