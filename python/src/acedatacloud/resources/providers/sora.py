"""Sora (sora) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

SoraModel = Literal[
    "sora-2",
    "sora-2-pro",
]
SoraDuration = Literal[4, 8, 10, 12, 15, 25]
SoraSize = Literal[
    "small",
    "large",
    "720x1280",
    "1280x720",
    "1024x1792",
    "1792x1024",
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


class Sora:
    """Synchronous sora client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        model: SoraModel,
        prompt: str,
        duration: SoraDuration | None = None,
        orientation: Literal["landscape", "portrait"] | None = None,
        size: SoraSize | None = None,
        character_url: str | None = None,
        character_start: int | None = None,
        character_end: int | None = None,
        image_urls: list[str] | None = None,
        version: Literal["1.0", "2.0"] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Sora video generation API. Generates videos from text prompts."""
        body: dict[str, Any] = {}
        body["model"] = model
        body["prompt"] = prompt
        if duration is not None:
            body["duration"] = duration
        if orientation is not None:
            body["orientation"] = orientation
        if size is not None:
            body["size"] = size
        if character_url is not None:
            body["character_url"] = character_url
        if character_start is not None:
            body["character_start"] = character_start
        if character_end is not None:
            body["character_end"] = character_end
        if image_urls is not None:
            body["image_urls"] = image_urls
        if version is not None:
            body["version"] = version
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/sora/videos", json=body)
        handle = TaskHandle(_task_id(result), "/sora/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncSora:
    """Asynchronous sora client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        model: SoraModel,
        prompt: str,
        duration: SoraDuration | None = None,
        orientation: Literal["landscape", "portrait"] | None = None,
        size: SoraSize | None = None,
        character_url: str | None = None,
        character_start: int | None = None,
        character_end: int | None = None,
        image_urls: list[str] | None = None,
        version: Literal["1.0", "2.0"] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Sora video generation API. Generates videos from text prompts."""
        body: dict[str, Any] = {}
        body["model"] = model
        body["prompt"] = prompt
        if duration is not None:
            body["duration"] = duration
        if orientation is not None:
            body["orientation"] = orientation
        if size is not None:
            body["size"] = size
        if character_url is not None:
            body["character_url"] = character_url
        if character_start is not None:
            body["character_start"] = character_start
        if character_end is not None:
            body["character_end"] = character_end
        if image_urls is not None:
            body["image_urls"] = image_urls
        if version is not None:
            body["version"] = version
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/sora/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/sora/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
