"""NanoBanana (nano-banana) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

NanoBananaModel = Literal[
    "nano-banana",
    "nano-banana-2-lite",
    "nano-banana-2",
    "nano-banana-pro",
    "nano-banana:official",
    "nano-banana-2-lite:official",
    "nano-banana-2:official",
    "nano-banana-pro:official",
]
NanoBananaAspectRatio = Literal[
    "1:1",
    "3:2",
    "2:3",
    "16:9",
    "9:16",
    "4:3",
    "3:4",
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


class NanoBanana:
    """Synchronous nano-banana client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: Literal["generate", "edit"],
        prompt: str,
        count: int | None = None,
        model: NanoBananaModel | None = None,
        image_urls: list[str] | None = None,
        resolution: Literal["1K", "2K", "4K"] | None = None,
        aspect_ratio: NanoBananaAspectRatio | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Google Nano Banana image generation and editing API. Supports nano-banana, nano-banana-2, and
        nano-banana-pro for text-to-image generation and reference-image editing.
        """
        body: dict[str, Any] = {}
        body["action"] = action
        body["prompt"] = prompt
        body["count"] = count if count is not None else 1
        if model is not None:
            body["model"] = model
        if image_urls is not None:
            body["image_urls"] = image_urls
        if resolution is not None:
            body["resolution"] = resolution
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/nano-banana/images", json=body)
        handle = TaskHandle(_task_id(result), "/nano-banana/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncNanoBanana:
    """Asynchronous nano-banana client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: Literal["generate", "edit"],
        prompt: str,
        count: int | None = None,
        model: NanoBananaModel | None = None,
        image_urls: list[str] | None = None,
        resolution: Literal["1K", "2K", "4K"] | None = None,
        aspect_ratio: NanoBananaAspectRatio | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Google Nano Banana image generation and editing API. Supports nano-banana, nano-banana-2, and
        nano-banana-pro for text-to-image generation and reference-image editing.
        """
        body: dict[str, Any] = {}
        body["action"] = action
        body["prompt"] = prompt
        body["count"] = count if count is not None else 1
        if model is not None:
            body["model"] = model
        if image_urls is not None:
            body["image_urls"] = image_urls
        if resolution is not None:
            body["resolution"] = resolution
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/nano-banana/images", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/nano-banana/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
