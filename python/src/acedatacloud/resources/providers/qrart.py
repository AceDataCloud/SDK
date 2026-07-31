"""QrArt (qrart) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

QrartType = Literal["link", "text", "email", "phone", "sms"]
QrartEcl = Literal["L", "M", "Q", "H"]
QrartRotate = Literal[0, 90, 180, 270]
QrartPreset = Literal["sunset", "floral", "snowflakes", "feathers", "raindrops"]
QrartPattern = Literal["custom", "s1", "s2", "s3", "rd1"]
QrartPosition = Literal["center", "top", "right", "bottom", "left"]
QrartSubMarker = Literal["square", "circle", "box", "random", "plus"]
QrartPixelStyle = Literal["square", "rounded", "dot", "squircle", "row"]
QrartAspectRatio = Literal["1:1", "16:9", "9:16", "4:3", "3:4"]


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


class Qrart:
    """Synchronous qrart client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        type: QrartType,
        prompt: str,
        ecl: QrartEcl | None = None,
        qrw: float | None = None,
        seed: float | None = None,
        steps: float | None = None,
        preset: QrartPreset | None = None,
        rawurl: bool | None = None,
        rotate: QrartRotate | None = None,
        content: str | None = None,
        pattern: QrartPattern | None = None,
        position: QrartPosition | None = None,
        sub_marker: QrartSubMarker | None = None,
        pixel_style: QrartPixelStyle | None = None,
        aspect_ratio: QrartAspectRatio | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Art QR Code generation API — generates a styled QR code image."""
        body: dict[str, Any] = {}
        body["type"] = type
        body["prompt"] = prompt
        if ecl is not None:
            body["ecl"] = ecl
        if qrw is not None:
            body["qrw"] = qrw
        if seed is not None:
            body["seed"] = seed
        if steps is not None:
            body["steps"] = steps
        if preset is not None:
            body["preset"] = preset
        if rawurl is not None:
            body["rawurl"] = rawurl
        if rotate is not None:
            body["rotate"] = rotate
        if content is not None:
            body["content"] = content
        if pattern is not None:
            body["pattern"] = pattern
        if position is not None:
            body["position"] = position
        if sub_marker is not None:
            body["sub_marker"] = sub_marker
        if pixel_style is not None:
            body["pixel_style"] = pixel_style
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/qrart/generate", json=body)
        handle = TaskHandle(_task_id(result), "/qrart/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncQrart:
    """Asynchronous qrart client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        type: QrartType,
        prompt: str,
        ecl: QrartEcl | None = None,
        qrw: float | None = None,
        seed: float | None = None,
        steps: float | None = None,
        preset: QrartPreset | None = None,
        rawurl: bool | None = None,
        rotate: QrartRotate | None = None,
        content: str | None = None,
        pattern: QrartPattern | None = None,
        position: QrartPosition | None = None,
        sub_marker: QrartSubMarker | None = None,
        pixel_style: QrartPixelStyle | None = None,
        aspect_ratio: QrartAspectRatio | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Art QR Code generation API — generates a styled QR code image."""
        body: dict[str, Any] = {}
        body["type"] = type
        body["prompt"] = prompt
        if ecl is not None:
            body["ecl"] = ecl
        if qrw is not None:
            body["qrw"] = qrw
        if seed is not None:
            body["seed"] = seed
        if steps is not None:
            body["steps"] = steps
        if preset is not None:
            body["preset"] = preset
        if rawurl is not None:
            body["rawurl"] = rawurl
        if rotate is not None:
            body["rotate"] = rotate
        if content is not None:
            body["content"] = content
        if pattern is not None:
            body["pattern"] = pattern
        if position is not None:
            body["position"] = position
        if sub_marker is not None:
            body["sub_marker"] = sub_marker
        if pixel_style is not None:
            body["pixel_style"] = pixel_style
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/qrart/generate", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/qrart/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
