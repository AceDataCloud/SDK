"""Maestro-specific video generation resources."""

from __future__ import annotations

from typing import Any, Literal

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

MaestroAction = Literal["generate", "remix", "edit", "extend"]
MaestroAspect = Literal["9:16", "16:9", "1:1"]
MaestroQuality = Literal["lite", "standard", "pro"]
MaestroScenario = Literal["auto", "narrated", "captions", "avatar", "drama"]
MaestroStyle = Literal[
    "auto", "cinematic", "glass", "luxury", "swiss", "modern", "editorial", "warm", "vibrant",
    "neon", "mono", "pastel", "bold", "industrial", "futuristic", "retro",
]
MaestroVoice = Literal[
    "auto", "warm-female", "bright-female", "anchor-female", "clean-female", "calm-male",
    "deep-male", "documentary-male", "energetic-male", "storyteller-male",
]


def _task_id(result: Any) -> str:
    if not isinstance(result, dict):
        return ""
    if result.get("task_id"):
        return str(result["task_id"])
    data = result.get("data")
    if isinstance(data, dict) and data.get("task_id"):
        return str(data["task_id"])
    return str(result.get("id") or "")


def _build_generate_body(
    *,
    prompt: str,
    action: MaestroAction | None,
    ref_task_id: str | None,
    file_urls: list[str] | None,
    langs: list[str] | None,
    aspect: MaestroAspect | None,
    duration: int | None,
    quality: MaestroQuality | None,
    scenario: MaestroScenario | None,
    style: MaestroStyle | None,
    voice: MaestroVoice | None,
    callback_url: str | None,
    async_: bool | None,
) -> dict[str, Any]:
    selected_action = action or "generate"
    selected_quality = quality or "standard"
    selected_scenario = scenario or "auto"
    selected_duration = duration if duration is not None else 30
    selected_langs = langs if langs is not None else ["zh-cn"]

    if selected_action not in {"generate", "remix", "edit", "extend"}:
        raise ValueError("action must be generate, remix, edit, or extend")
    if selected_quality not in {"lite", "standard", "pro"}:
        raise ValueError("quality must be lite, standard, or pro")
    if selected_action != "generate" and not ref_task_id:
        raise ValueError("ref_task_id is required when action is remix, edit, or extend")
    if not selected_langs or len(selected_langs) > 4:
        raise ValueError("langs must contain between 1 and 4 languages")
    if isinstance(selected_duration, bool) or not 5 <= selected_duration <= 300:
        raise ValueError("duration must be an integer between 5 and 300")
    if selected_quality == "lite" and (selected_duration > 30 or selected_action not in {"generate", "edit"}):
        raise ValueError("lite supports generate/edit actions and durations up to 30 seconds")
    if selected_quality == "standard" and (selected_duration > 120 or selected_action == "extend"):
        raise ValueError("standard supports generate/remix/edit actions and durations up to 120 seconds")
    allowed_scenarios = {
        "lite": {"auto", "narrated", "captions"},
        "standard": {"auto", "narrated", "captions", "avatar"},
        "pro": {"auto", "narrated", "captions", "avatar", "drama"},
    }
    if selected_scenario not in {"auto", "narrated", "captions", "avatar", "drama"}:
        raise ValueError("scenario must be auto, narrated, captions, avatar, or drama")
    if selected_scenario not in allowed_scenarios[selected_quality]:
        raise ValueError(f"{selected_scenario} scenario requires a higher quality tier")
    if selected_scenario in {"captions", "avatar"} and not file_urls:
        raise ValueError(f"file_urls is required for the {selected_scenario} scenario")

    body: dict[str, Any] = {
        "prompt": prompt,
        "action": selected_action,
        "langs": selected_langs,
        "aspect": aspect or "9:16",
        "duration": selected_duration,
        "quality": selected_quality,
        "scenario": selected_scenario,
        "style": style or "auto",
        "voice": voice or "auto",
        "async": True if async_ is None else async_,
    }
    if ref_task_id is not None:
        body["ref_task_id"] = ref_task_id
    if file_urls is not None:
        body["file_urls"] = file_urls
    if callback_url is not None:
        body["callback_url"] = callback_url
    return body


class Maestro:
    """Synchronous Maestro client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self, *, prompt: str, action: MaestroAction | None = None, ref_task_id: str | None = None,
        file_urls: list[str] | None = None, langs: list[str] | None = None,
        aspect: MaestroAspect | None = None, duration: int | None = None,
        quality: MaestroQuality | None = None, scenario: MaestroScenario | None = None,
        style: MaestroStyle | None = None, voice: MaestroVoice | None = None,
        async_: bool | None = None, wait: bool = False, poll_interval: float = 3.0,
        max_wait: float = 600.0, callback_url: str | None = None,
    ) -> TaskHandle:
        result = self._transport.request("POST", "/maestro/videos", json=_build_generate_body(
            prompt=prompt, action=action, ref_task_id=ref_task_id, file_urls=file_urls, langs=langs,
            aspect=aspect, duration=duration, quality=quality, scenario=scenario, style=style,
            voice=voice, callback_url=callback_url, async_=async_,
        ))
        handle = TaskHandle(_task_id(result), "/maestro/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncMaestro:
    """Asynchronous Maestro client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self, *, prompt: str, action: MaestroAction | None = None, ref_task_id: str | None = None,
        file_urls: list[str] | None = None, langs: list[str] | None = None,
        aspect: MaestroAspect | None = None, duration: int | None = None,
        quality: MaestroQuality | None = None, scenario: MaestroScenario | None = None,
        style: MaestroStyle | None = None, voice: MaestroVoice | None = None,
        async_: bool | None = None, wait: bool = False, poll_interval: float = 3.0,
        max_wait: float = 600.0, callback_url: str | None = None,
    ) -> AsyncTaskHandle:
        result = await self._transport.request("POST", "/maestro/videos", json=_build_generate_body(
            prompt=prompt, action=action, ref_task_id=ref_task_id, file_urls=file_urls, langs=langs,
            aspect=aspect, duration=duration, quality=quality, scenario=scenario, style=style,
            voice=voice, callback_url=callback_url, async_=async_,
        ))
        handle = AsyncTaskHandle(_task_id(result), "/maestro/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
