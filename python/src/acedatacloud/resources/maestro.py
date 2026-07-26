"""Maestro AI Video Studio resources (``/maestro/*``)."""

from __future__ import annotations

from typing import Any

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle


class Maestro:
    """Synchronous Maestro client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def videos(
        self,
        *,
        prompt: str,
        action: str | None = None,
        ref_task_id: str | None = None,
        file_urls: list[str] | None = None,
        langs: list[str] | None = None,
        aspect: str | None = None,
        duration: int | None = None,
        quality: str | None = None,
        scenario: str | None = None,
        style: str | None = None,
        voice: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if action is not None:
            body["action"] = action
        if ref_task_id is not None:
            body["ref_task_id"] = ref_task_id
        if file_urls is not None:
            body["file_urls"] = file_urls
        if langs is not None:
            body["langs"] = langs
        if aspect is not None:
            body["aspect"] = aspect
        if duration is not None:
            body["duration"] = duration
        if quality is not None:
            body["quality"] = quality
        if scenario is not None:
            body["scenario"] = scenario
        if style is not None:
            body["style"] = style
        if voice is not None:
            body["voice"] = voice
        if callback_url is not None:
            body["callback_url"] = callback_url

        result = self._transport.request("POST", "/maestro/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or not wait:
            return result

        handle = TaskHandle(task_id, "/maestro/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncMaestro:
    """Async Maestro client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def videos(
        self,
        *,
        prompt: str,
        action: str | None = None,
        ref_task_id: str | None = None,
        file_urls: list[str] | None = None,
        langs: list[str] | None = None,
        aspect: str | None = None,
        duration: int | None = None,
        quality: str | None = None,
        scenario: str | None = None,
        style: str | None = None,
        voice: str | None = None,
        callback_url: str | None = None,
        wait: bool = False,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if action is not None:
            body["action"] = action
        if ref_task_id is not None:
            body["ref_task_id"] = ref_task_id
        if file_urls is not None:
            body["file_urls"] = file_urls
        if langs is not None:
            body["langs"] = langs
        if aspect is not None:
            body["aspect"] = aspect
        if duration is not None:
            body["duration"] = duration
        if quality is not None:
            body["quality"] = quality
        if scenario is not None:
            body["scenario"] = scenario
        if style is not None:
            body["style"] = style
        if voice is not None:
            body["voice"] = voice
        if callback_url is not None:
            body["callback_url"] = callback_url

        result = await self._transport.request("POST", "/maestro/videos", json=body)
        task_id = result.get("task_id")

        if not task_id or not wait:
            return result

        handle = AsyncTaskHandle(task_id, "/maestro/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
