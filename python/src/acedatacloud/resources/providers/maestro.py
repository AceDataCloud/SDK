"""Maestro (maestro) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MaestroAction = Literal[
    "generate",
    "remix",
    "edit",
    "extend",
]
MaestroScenario = Literal[
    "auto",
    "narrated",
    "captions",
    "avatar",
    "drama",
]
MaestroStyle = Literal[
    "auto",
    "cinematic",
    "glass",
    "luxury",
    "swiss",
    "modern",
    "editorial",
    "warm",
    "vibrant",
    "neon",
    "mono",
    "pastel",
    "bold",
    "industrial",
    "futuristic",
    "retro",
]
MaestroVoice = Literal[
    "auto",
    "warm-female",
    "bright-female",
    "anchor-female",
    "clean-female",
    "calm-male",
    "deep-male",
    "documentary-male",
    "energetic-male",
    "storyteller-male",
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


class Maestro:
    """Synchronous maestro client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        action: MaestroAction | None = None,
        ref_task_id: str | None = None,
        file_urls: list[str] | None = None,
        langs: list[str] | None = None,
        aspect: Literal["9:16", "16:9", "1:1"] | None = None,
        duration: int | None = None,
        quality: Literal["lite", "standard", "pro"] | None = None,
        scenario: MaestroScenario | None = None,
        style: MaestroStyle | None = None,
        voice: MaestroVoice | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Call /maestro/videos."""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body["action"] = action if action is not None else "generate"
        if ref_task_id is not None:
            body["ref_task_id"] = ref_task_id
        if file_urls is not None:
            body["file_urls"] = file_urls
        body["langs"] = langs if langs is not None else ["zh-cn"]
        body["aspect"] = aspect if aspect is not None else "9:16"
        body["duration"] = duration if duration is not None else 30
        body["quality"] = quality if quality is not None else "standard"
        body["scenario"] = scenario if scenario is not None else "auto"
        body["style"] = style if style is not None else "auto"
        body["voice"] = voice if voice is not None else "auto"
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/maestro/videos", json=body)
        handle = TaskHandle(_task_id(result), "/maestro/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncMaestro:
    """Asynchronous maestro client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        action: MaestroAction | None = None,
        ref_task_id: str | None = None,
        file_urls: list[str] | None = None,
        langs: list[str] | None = None,
        aspect: Literal["9:16", "16:9", "1:1"] | None = None,
        duration: int | None = None,
        quality: Literal["lite", "standard", "pro"] | None = None,
        scenario: MaestroScenario | None = None,
        style: MaestroStyle | None = None,
        voice: MaestroVoice | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Call /maestro/videos."""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body["action"] = action if action is not None else "generate"
        if ref_task_id is not None:
            body["ref_task_id"] = ref_task_id
        if file_urls is not None:
            body["file_urls"] = file_urls
        body["langs"] = langs if langs is not None else ["zh-cn"]
        body["aspect"] = aspect if aspect is not None else "9:16"
        body["duration"] = duration if duration is not None else 30
        body["quality"] = quality if quality is not None else "standard"
        body["scenario"] = scenario if scenario is not None else "auto"
        body["style"] = style if style is not None else "auto"
        body["voice"] = voice if voice is not None else "auto"
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/maestro/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/maestro/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
