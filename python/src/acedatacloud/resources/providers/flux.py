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
FluxMode = Literal[
    "t2v",
    "i2v",
    "v2v",
    "draft_enhance",
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
        size: str,
        action: Literal["generate", "edit"],
        prompt: str,
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
        """Flux Images"""
        body: dict[str, Any] = {}
        body["size"] = size
        body["action"] = action
        body["prompt"] = prompt
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

    def videos(
        self,
        *,
        mode: FluxMode,
        action: Literal["generate"] | None = None,
        prompt: str | None = None,
        aspect_ratio: Literal["21:9", "2:1", "16:9", "4:3", "1:1", "3:4", "9:16", "9:21"]
        | Literal["auto"]
        | None = None,
        duration: int | Literal["auto"] | None = None,
        resolution: Literal["hd", "fhd", "qhd", "uhd"] | None = None,
        version: Literal["latest"] | None = None,
        generate_audio: bool | None = None,
        safety_tolerance: int | None = None,
        draft: bool | None = None,
        model: FluxModel | None = None,
        keyframes: str | list[Any] | list[str] | None = None,
        start_video: str | None = None,
        draft_task_id: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Flux Generate Summary"""
        body: dict[str, Any] = {}
        body["mode"] = mode
        body["action"] = action if action is not None else "generate"
        if prompt is not None:
            body["prompt"] = prompt
        body["aspect_ratio"] = aspect_ratio if aspect_ratio is not None else "auto"
        if duration is not None:
            body["duration"] = duration
        body["resolution"] = resolution if resolution is not None else "hd"
        body["version"] = version if version is not None else "latest"
        if generate_audio is not None:
            body["generate_audio"] = generate_audio
        body["safety_tolerance"] = safety_tolerance if safety_tolerance is not None else 2
        if draft is not None:
            body["draft"] = draft
        body["model"] = model if model is not None else "flux-3"
        if keyframes is not None:
            body["keyframes"] = keyframes
        if start_video is not None:
            body["start_video"] = start_video
        if draft_task_id is not None:
            body["draft_task_id"] = draft_task_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/flux/videos", json=body)
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
        size: str,
        action: Literal["generate", "edit"],
        prompt: str,
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
        """Flux Images"""
        body: dict[str, Any] = {}
        body["size"] = size
        body["action"] = action
        body["prompt"] = prompt
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

    async def videos(
        self,
        *,
        mode: FluxMode,
        action: Literal["generate"] | None = None,
        prompt: str | None = None,
        aspect_ratio: Literal["21:9", "2:1", "16:9", "4:3", "1:1", "3:4", "9:16", "9:21"]
        | Literal["auto"]
        | None = None,
        duration: int | Literal["auto"] | None = None,
        resolution: Literal["hd", "fhd", "qhd", "uhd"] | None = None,
        version: Literal["latest"] | None = None,
        generate_audio: bool | None = None,
        safety_tolerance: int | None = None,
        draft: bool | None = None,
        model: FluxModel | None = None,
        keyframes: str | list[Any] | list[str] | None = None,
        start_video: str | None = None,
        draft_task_id: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Flux Generate Summary"""
        body: dict[str, Any] = {}
        body["mode"] = mode
        body["action"] = action if action is not None else "generate"
        if prompt is not None:
            body["prompt"] = prompt
        body["aspect_ratio"] = aspect_ratio if aspect_ratio is not None else "auto"
        if duration is not None:
            body["duration"] = duration
        body["resolution"] = resolution if resolution is not None else "hd"
        body["version"] = version if version is not None else "latest"
        if generate_audio is not None:
            body["generate_audio"] = generate_audio
        body["safety_tolerance"] = safety_tolerance if safety_tolerance is not None else 2
        if draft is not None:
            body["draft"] = draft
        body["model"] = model if model is not None else "flux-3"
        if keyframes is not None:
            body["keyframes"] = keyframes
        if start_video is not None:
            body["start_video"] = start_video
        if draft_task_id is not None:
            body["draft_task_id"] = draft_task_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/flux/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/flux/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
