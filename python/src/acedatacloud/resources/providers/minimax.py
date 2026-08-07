"""Minimax (minimax) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MinimaxModel = Literal["minimax-h3"]
MinimaxRatio = Literal["16:9", "9:16"]


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


class Minimax:
    """Synchronous minimax client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        model: MinimaxModel | None = None,
        prompt: str | None = None,
        image_urls: list[str] | None = None,
        audio_urls: list[str] | None = None,
        ratio: MinimaxRatio | None = None,
        duration: int | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """MiniMax H3 video generation API."""
        body: dict[str, Any] = {}
        body["model"] = model if model is not None else "minimax-h3"
        body["prompt"] = (
            prompt
            if prompt is not None
            else "A red fox running through a snowy forest at dawn, cinematic tracking shot"
        )
        if image_urls is not None:
            body["image_urls"] = image_urls
        if audio_urls is not None:
            body["audio_urls"] = audio_urls
        body["ratio"] = ratio if ratio is not None else "16:9"
        body["duration"] = duration if duration is not None else 4
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/minimax/videos", json=body)
        handle = TaskHandle(_task_id(result), "/minimax/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncMinimax:
    """Asynchronous minimax client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        model: MinimaxModel | None = None,
        prompt: str | None = None,
        image_urls: list[str] | None = None,
        audio_urls: list[str] | None = None,
        ratio: MinimaxRatio | None = None,
        duration: int | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """MiniMax H3 video generation API."""
        body: dict[str, Any] = {}
        body["model"] = model if model is not None else "minimax-h3"
        body["prompt"] = (
            prompt
            if prompt is not None
            else "A red fox running through a snowy forest at dawn, cinematic tracking shot"
        )
        if image_urls is not None:
            body["image_urls"] = image_urls
        if audio_urls is not None:
            body["audio_urls"] = audio_urls
        body["ratio"] = ratio if ratio is not None else "16:9"
        body["duration"] = duration if duration is not None else 4
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/minimax/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/minimax/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
