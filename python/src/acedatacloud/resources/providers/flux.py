"""Flux (flux) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

FluxModel = Literal[
    "flux-dev",
    "flux-pro",
    "flux-kontext-pro",
    "flux-kontext-max",
    "flux-2-flex",
    "flux-2-pro",
    "flux-2-max",
    "flux-2-klein",
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


class Flux:
    """Synchronous flux client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: Literal["generate", "edit"],
        prompt: str,
        size: str | None = None,
        count: float | None = None,
        model: FluxModel | None = None,
        image_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Flux AI image generation API, generates 1 image per request."""
        body: dict[str, Any] = {}
        body["action"] = action
        body["prompt"] = prompt
        body["size"] = size if size is not None else "1024x1024"
        if count is not None:
            body["count"] = count
        if model is not None:
            body["model"] = model
        if image_url is not None:
            body["image_url"] = image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/flux/images", json=body)
        handle = TaskHandle(_task_id(result), "/flux/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncFlux:
    """Asynchronous flux client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: Literal["generate", "edit"],
        prompt: str,
        size: str | None = None,
        count: float | None = None,
        model: FluxModel | None = None,
        image_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Flux AI image generation API, generates 1 image per request."""
        body: dict[str, Any] = {}
        body["action"] = action
        body["prompt"] = prompt
        body["size"] = size if size is not None else "1024x1024"
        if count is not None:
            body["count"] = count
        if model is not None:
            body["model"] = model
        if image_url is not None:
            body["image_url"] = image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/flux/images", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/flux/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
