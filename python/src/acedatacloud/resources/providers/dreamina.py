"""Dreamina (dreamina) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle


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


class Dreamina:
    """Synchronous dreamina client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        audio_url: str,
        image_url: str,
        model: Literal["omnihuman-1.5"] | None = None,
        prompt: str | None = None,
        mask_url: list[str] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Audio-driven talking-photo digital human video generation (OmniHuman 1.5)"""
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        body["image_url"] = image_url
        body["model"] = model if model is not None else "omnihuman-1.5"
        if prompt is not None:
            body["prompt"] = prompt
        if mask_url is not None:
            body["mask_url"] = mask_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/dreamina/videos", json=body)
        handle = TaskHandle(_task_id(result), "/dreamina/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncDreamina:
    """Asynchronous dreamina client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        audio_url: str,
        image_url: str,
        model: Literal["omnihuman-1.5"] | None = None,
        prompt: str | None = None,
        mask_url: list[str] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Audio-driven talking-photo digital human video generation (OmniHuman 1.5)"""
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        body["image_url"] = image_url
        body["model"] = model if model is not None else "omnihuman-1.5"
        if prompt is not None:
            body["prompt"] = prompt
        if mask_url is not None:
            body["mask_url"] = mask_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/dreamina/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/dreamina/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
