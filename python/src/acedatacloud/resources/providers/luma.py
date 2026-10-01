"""Luma (luma) — generated from the platform OpenAPI spec.

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


class Luma:
    """Synchronous luma client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        loop: bool | None = None,
        action: Literal["generate", "extend"] | None = None,
        prompt: str | None = None,
        timeout: float | None = None,
        video_id: str | None = None,
        aspect_ratio: str | None = None,
        video_url: str | None = None,
        enhancement: bool | None = None,
        end_image_url: str | None = None,
        start_image_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Generate videos based on prompt and image frames"""
        body: dict[str, Any] = {}
        body["loop"] = loop if loop is not None else False
        body["action"] = action if action is not None else "generate"
        if prompt is not None:
            body["prompt"] = prompt
        body["timeout"] = timeout if timeout is not None else 300
        if video_id is not None:
            body["video_id"] = video_id
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if video_url is not None:
            body["video_url"] = video_url
        body["enhancement"] = enhancement if enhancement is not None else True
        if end_image_url is not None:
            body["end_image_url"] = end_image_url
        if start_image_url is not None:
            body["start_image_url"] = start_image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/luma/videos", json=body)
        handle = TaskHandle(_task_id(result), "/luma/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncLuma:
    """Asynchronous luma client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        loop: bool | None = None,
        action: Literal["generate", "extend"] | None = None,
        prompt: str | None = None,
        timeout: float | None = None,
        video_id: str | None = None,
        aspect_ratio: str | None = None,
        video_url: str | None = None,
        enhancement: bool | None = None,
        end_image_url: str | None = None,
        start_image_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Generate videos based on prompt and image frames"""
        body: dict[str, Any] = {}
        body["loop"] = loop if loop is not None else False
        body["action"] = action if action is not None else "generate"
        if prompt is not None:
            body["prompt"] = prompt
        body["timeout"] = timeout if timeout is not None else 300
        if video_id is not None:
            body["video_id"] = video_id
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if video_url is not None:
            body["video_url"] = video_url
        body["enhancement"] = enhancement if enhancement is not None else True
        if end_image_url is not None:
            body["end_image_url"] = end_image_url
        if start_image_url is not None:
            body["start_image_url"] = start_image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/luma/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/luma/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
