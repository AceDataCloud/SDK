"""Maestro (maestro) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

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
MaestroAction = Literal[
    "generate",
    "remix",
    "edit",
    "extend",
]
MaestroScenario = Literal[
    "auto",
    "narrated",
    "drama",
    "avatar",
    "motion",
    "slideshow",
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
        langs: list[str] | None = None,
        style: MaestroStyle | None = None,
        voice: MaestroVoice | None = None,
        action: MaestroAction | None = None,
        aspect: Literal["9:16", "16:9", "1:1"] | None = None,
        quality: Literal["draft", "standard", "premium"] | None = None,
        duration: int | None = None,
        scenario: MaestroScenario | None = None,
        file_urls: list[str] | None = None,
        ref_task_id: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Maestro Video Generation API"""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body["langs"] = langs if langs is not None else ["zh-cn"]
        body["style"] = style if style is not None else "auto"
        body["voice"] = voice if voice is not None else "auto"
        body["action"] = action if action is not None else "generate"
        body["aspect"] = aspect if aspect is not None else "9:16"
        body["quality"] = quality if quality is not None else "standard"
        body["duration"] = duration if duration is not None else 30
        body["scenario"] = scenario if scenario is not None else "auto"
        if file_urls is not None:
            body["file_urls"] = file_urls
        if ref_task_id is not None:
            body["ref_task_id"] = ref_task_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/maestro/videos", json=body)

    def estimates(
        self,
        *,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Call /maestro/estimates."""
        body: dict[str, Any] = {}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/maestro/estimates", json=body)


class AsyncMaestro:
    """Asynchronous maestro client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        langs: list[str] | None = None,
        style: MaestroStyle | None = None,
        voice: MaestroVoice | None = None,
        action: MaestroAction | None = None,
        aspect: Literal["9:16", "16:9", "1:1"] | None = None,
        quality: Literal["draft", "standard", "premium"] | None = None,
        duration: int | None = None,
        scenario: MaestroScenario | None = None,
        file_urls: list[str] | None = None,
        ref_task_id: str | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Maestro Video Generation API"""
        body: dict[str, Any] = {}
        body["prompt"] = prompt
        body["langs"] = langs if langs is not None else ["zh-cn"]
        body["style"] = style if style is not None else "auto"
        body["voice"] = voice if voice is not None else "auto"
        body["action"] = action if action is not None else "generate"
        body["aspect"] = aspect if aspect is not None else "9:16"
        body["quality"] = quality if quality is not None else "standard"
        body["duration"] = duration if duration is not None else 30
        body["scenario"] = scenario if scenario is not None else "auto"
        if file_urls is not None:
            body["file_urls"] = file_urls
        if ref_task_id is not None:
            body["ref_task_id"] = ref_task_id
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/maestro/videos", json=body)

    async def estimates(
        self,
        *,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Call /maestro/estimates."""
        body: dict[str, Any] = {}
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/maestro/estimates", json=body)
