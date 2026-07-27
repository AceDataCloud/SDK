"""Seedance (seedance) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

SeedanceModel = Literal[
    "doubao-seedance-1-0-pro-250528",
    "doubao-seedance-1-0-pro-fast-251015",
    "doubao-seedance-1-5-pro-251215",
    "doubao-seedance-1-0-lite-t2v-250428",
    "doubao-seedance-1-0-lite-i2v-250428",
    "doubao-seedance-2-0-260128",
    "doubao-seedance-2-0-fast-260128",
    "doubao-seedance-2-0-mini-260615",
]
SeedanceRatio = Literal[
    "16:9",
    "4:3",
    "1:1",
    "3:4",
    "9:16",
    "21:9",
    "adaptive",
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


class Seedance:
    """Synchronous seedance client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        model: SeedanceModel,
        content: list[Any],
        seed: int | None = None,
        ratio: SeedanceRatio | None = None,
        frames: int | None = None,
        duration: int | None = None,
        watermark: bool | None = None,
        resolution: Literal["480p", "720p", "1080p", "4k"] | None = None,
        camerafixed: bool | None = None,
        generate_audio: bool | None = None,
        return_last_frame: bool | None = None,
        execution_expires_after: int | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """ByteDance Seedance video generation API. Supports doubao-seedance-1-0-pro-250528,
        doubao-seedance-1-0-pro-fast-251015, doubao-seedance-1-5-pro-251215, doubao-seedance-1-0-lite-t2v-250428,
        and doubao-s
        """
        body: dict[str, Any] = {}
        body["model"] = model
        body["content"] = content
        if seed is not None:
            body["seed"] = seed
        body["ratio"] = ratio if ratio is not None else "16:9"
        if frames is not None:
            body["frames"] = frames
        if duration is not None:
            body["duration"] = duration
        if watermark is not None:
            body["watermark"] = watermark
        if resolution is not None:
            body["resolution"] = resolution
        if camerafixed is not None:
            body["camerafixed"] = camerafixed
        body["generate_audio"] = generate_audio if generate_audio is not None else False
        body["return_last_frame"] = return_last_frame if return_last_frame is not None else False
        body["execution_expires_after"] = execution_expires_after if execution_expires_after is not None else 172800
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/seedance/videos", json=body)
        handle = TaskHandle(_task_id(result), "/seedance/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncSeedance:
    """Asynchronous seedance client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        model: SeedanceModel,
        content: list[Any],
        seed: int | None = None,
        ratio: SeedanceRatio | None = None,
        frames: int | None = None,
        duration: int | None = None,
        watermark: bool | None = None,
        resolution: Literal["480p", "720p", "1080p", "4k"] | None = None,
        camerafixed: bool | None = None,
        generate_audio: bool | None = None,
        return_last_frame: bool | None = None,
        execution_expires_after: int | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """ByteDance Seedance video generation API. Supports doubao-seedance-1-0-pro-250528,
        doubao-seedance-1-0-pro-fast-251015, doubao-seedance-1-5-pro-251215, doubao-seedance-1-0-lite-t2v-250428,
        and doubao-s
        """
        body: dict[str, Any] = {}
        body["model"] = model
        body["content"] = content
        if seed is not None:
            body["seed"] = seed
        body["ratio"] = ratio if ratio is not None else "16:9"
        if frames is not None:
            body["frames"] = frames
        if duration is not None:
            body["duration"] = duration
        if watermark is not None:
            body["watermark"] = watermark
        if resolution is not None:
            body["resolution"] = resolution
        if camerafixed is not None:
            body["camerafixed"] = camerafixed
        body["generate_audio"] = generate_audio if generate_audio is not None else False
        body["return_last_frame"] = return_last_frame if return_last_frame is not None else False
        body["execution_expires_after"] = execution_expires_after if execution_expires_after is not None else 172800
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/seedance/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/seedance/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
