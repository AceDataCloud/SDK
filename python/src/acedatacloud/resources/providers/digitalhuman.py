"""Digitalhuman (digitalhuman) — generated from the platform OpenAPI spec.

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


def _build_generate_body(
    *,
    video_url: str | None,
    text: str | None,
    speed: float | None,
    steps: int | None,
    engine: Literal["latentsync", "heygem"] | None,
    guidance: float | None,
    seam_fix: bool | None,
    voice_id: str | None,
    audio_url: str | None,
    image_url: str | None,
    resolution: Literal["720p", "540p"] | None,
    async_: bool | None,
    callback_url: str | None,
    extra: dict[str, Any],
) -> dict[str, Any]:
    if not video_url and not image_url:
        raise ValueError("video_url or image_url is required")

    body: dict[str, Any] = {}
    if video_url:
        body["video_url"] = video_url
    body["text"] = text if text is not None else "大家好，这是离线生成的数字人。"
    body["speed"] = speed if speed is not None else 1.0
    body["steps"] = steps if steps is not None else 40
    body["engine"] = engine if engine is not None else "latentsync"
    body["guidance"] = guidance if guidance is not None else 2.0
    body["seam_fix"] = seam_fix if seam_fix is not None else True
    if voice_id is not None:
        body["voice_id"] = voice_id
    if audio_url is not None:
        body["audio_url"] = audio_url
    if image_url:
        body["image_url"] = image_url
    body["resolution"] = resolution if resolution is not None else "720p"
    body.update(extra)
    if callback_url is not None:
        body["callback_url"] = callback_url
    body["async"] = True if async_ is None else async_
    return body


class Digitalhuman:
    """Synchronous digitalhuman client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        video_url: str | None = None,
        text: str | None = None,
        speed: float | None = None,
        steps: int | None = None,
        engine: Literal["latentsync", "heygem"] | None = None,
        guidance: float | None = None,
        seam_fix: bool | None = None,
        voice_id: str | None = None,
        audio_url: str | None = None,
        image_url: str | None = None,
        resolution: Literal["720p", "540p"] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Digital Human video generation API — turn a portrait plus audio or text into a talking-head video."""
        body = _build_generate_body(
            video_url=video_url,
            text=text,
            speed=speed,
            steps=steps,
            engine=engine,
            guidance=guidance,
            seam_fix=seam_fix,
            voice_id=voice_id,
            audio_url=audio_url,
            image_url=image_url,
            resolution=resolution,
            async_=async_,
            callback_url=callback_url,
            extra=extra,
        )
        result = self._transport.request("POST", "/digital-human/videos", json=body)
        handle = TaskHandle(_task_id(result), "/digital-human/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    def voices(
        self,
        *,
        audio_url: str,
        lang: Literal["zh", "en"] | None = None,
        name: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Digital Human voice-clone API — upload an audio sample to clone a custom voice for speech synthesis."""
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        body["lang"] = lang if lang is not None else "zh"
        if name is not None:
            body["name"] = name
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/digital-human/voices", json=body)
        handle = TaskHandle(_task_id(result), "/digital-human/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncDigitalhuman:
    """Asynchronous digitalhuman client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        video_url: str | None = None,
        text: str | None = None,
        speed: float | None = None,
        steps: int | None = None,
        engine: Literal["latentsync", "heygem"] | None = None,
        guidance: float | None = None,
        seam_fix: bool | None = None,
        voice_id: str | None = None,
        audio_url: str | None = None,
        image_url: str | None = None,
        resolution: Literal["720p", "540p"] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Digital Human video generation API — turn a portrait plus audio or text into a talking-head video."""
        body = _build_generate_body(
            video_url=video_url,
            text=text,
            speed=speed,
            steps=steps,
            engine=engine,
            guidance=guidance,
            seam_fix=seam_fix,
            voice_id=voice_id,
            audio_url=audio_url,
            image_url=image_url,
            resolution=resolution,
            async_=async_,
            callback_url=callback_url,
            extra=extra,
        )
        result = await self._transport.request("POST", "/digital-human/videos", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/digital-human/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle

    async def voices(
        self,
        *,
        audio_url: str,
        lang: Literal["zh", "en"] | None = None,
        name: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Digital Human voice-clone API — upload an audio sample to clone a custom voice for speech synthesis."""
        body: dict[str, Any] = {}
        body["audio_url"] = audio_url
        body["lang"] = lang if lang is not None else "zh"
        if name is not None:
            body["name"] = name
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/digital-human/voices", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/digital-human/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
