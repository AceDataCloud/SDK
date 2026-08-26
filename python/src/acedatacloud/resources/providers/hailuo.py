"""Hailuo (hailuo) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

HailuoModel = Literal[
    "minimax-i2v",
    "minimax-t2v",
    "minimax-i2v-director",
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


class Hailuo:
    """Synchronous hailuo client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        action: Literal["generate"],
        model: HailuoModel | None = None,
        prompt: str | None = None,
        first_image_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Minimax Hailuo AI video generation API. Supports minimax-t2v for text-to-video, minimax-i2v for
        image-to-video, and minimax-i2v-director for director mode with camera/movement instructions.
        """
        body: dict[str, Any] = {}
        body["action"] = action
        if model is not None:
            body["model"] = model
        if prompt is not None:
            body["prompt"] = prompt
        if first_image_url is not None:
            body["first_image_url"] = first_image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = self._transport.request("POST", "/hailuo/videos", json=body)
        handle = TaskHandle(_task_id(result), "/hailuo/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncHailuo:
    """Asynchronous hailuo client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        action: Literal["generate"],
        model: HailuoModel | None = None,
        prompt: str | None = None,
        first_image_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Minimax Hailuo AI video generation API. Supports minimax-t2v for text-to-video, minimax-i2v for
        image-to-video, and minimax-i2v-director for director mode with camera/movement instructions.
        """
        body: dict[str, Any] = {}
        body["action"] = action
        if model is not None:
            body["model"] = model
        if prompt is not None:
            body["prompt"] = prompt
        if first_image_url is not None:
            body["first_image_url"] = first_image_url
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        result = await self._transport.request("POST", "/hailuo/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/hailuo/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
