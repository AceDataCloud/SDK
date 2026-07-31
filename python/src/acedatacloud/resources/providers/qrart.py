"""QRart (qrart) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

QRartType = Literal["link", "text", "email", "phone", "sms"]
QRartPreset = Literal[
    "sunset",
    "floral",
    "snowflakes",
    "feathers",
    "raindrops",
    "ultra-realism",
    "epic-realms",
    "intricate-studio",
    "symmetric-masterpiece",
    "luminous-highway",
    "celestial-journey",
    "neon-mech",
    "ethereal-low-poly",
    "golden-vista",
    "cinematic-expanse",
    "cinematic-warm",
    "desolate-wilderness",
    "vibrant-palette",
    "enigmatic-journey",
    "timeless-cinematic",
    "regal-galaxy",
    "illustrious-canvas",
    "expressive-mural",
    "serene-haze",
]
QRartPattern = Literal[
    "custom",
    "s1",
    "s2",
    "s3",
    "rd1",
    "rd2",
    "rd3",
    "d1",
    "d2",
    "d3",
    "r1",
    "r2",
    "r3",
    "c1",
    "c2",
    "c3",
    "sq1",
    "sq2",
    "sq3",
]
QRartPixelStyle = Literal["square", "rounded", "dot", "squircle", "row", "column"]
QRartPosition = Literal[
    "center",
    "top",
    "right",
    "bottom",
    "left",
    "top-left",
    "top-right",
    "bottom-left",
    "bottom-right",
]
QRartMarkerShape = Literal["square", "circle", "plus", "box", "octagon", "random", "tiny-plus"]
QRartSubMarker = Literal["square", "circle", "box", "random", "plus"]
QRartAspectRatio = Literal["1:1", "16:9", "9:16", "4:3", "3:4"]
QRartEcl = Literal["L", "M", "Q", "H"]
QRartRotate = Literal[0, 90, 180, 270]
QRartPaddingLevel = Literal[0, 5, 10, 15, 20]
QRartPaddingNoise = Literal[0, 0.25, 0.5, 0.75, 1]


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


class QRart:
    """Synchronous qrart client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        type: QRartType,
        content: str | None = None,
        content_image_url: str | None = None,
        ecl: QRartEcl | None = None,
        qrw: float | None = None,
        seed: float | None = None,
        steps: float | None = None,
        aspect_ratio: QRartAspectRatio | None = None,
        preset: QRartPreset | None = None,
        pattern: QRartPattern | None = None,
        pixel_style: QRartPixelStyle | None = None,
        position: QRartPosition | None = None,
        marker_shape: QRartMarkerShape | None = None,
        sub_marker: QRartSubMarker | None = None,
        padding_level: QRartPaddingLevel | None = None,
        padding_noise: QRartPaddingNoise | None = None,
        rotate: QRartRotate | None = None,
        rawurl: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Art QR Code generation API."""
        body: dict[str, Any] = {"prompt": prompt, "type": type}
        if content is not None:
            body["content"] = content
        if content_image_url is not None:
            body["content_image_url"] = content_image_url
        if ecl is not None:
            body["ecl"] = ecl
        if qrw is not None:
            body["qrw"] = qrw
        if seed is not None:
            body["seed"] = seed
        if steps is not None:
            body["steps"] = steps
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if preset is not None:
            body["preset"] = preset
        if pattern is not None:
            body["pattern"] = pattern
        if pixel_style is not None:
            body["pixel_style"] = pixel_style
        if position is not None:
            body["position"] = position
        if marker_shape is not None:
            body["marker_shape"] = marker_shape
        if sub_marker is not None:
            body["sub_marker"] = sub_marker
        if padding_level is not None:
            body["padding_level"] = padding_level
        if padding_noise is not None:
            body["padding_noise"] = padding_noise
        if rotate is not None:
            body["rotate"] = rotate
        if rawurl is not None:
            body["rawurl"] = rawurl
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/qrart/generate", json=body)
        handle = TaskHandle(_task_id(result), "/qrart/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncQRart:
    """Asynchronous qrart client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        type: QRartType,
        content: str | None = None,
        content_image_url: str | None = None,
        ecl: QRartEcl | None = None,
        qrw: float | None = None,
        seed: float | None = None,
        steps: float | None = None,
        aspect_ratio: QRartAspectRatio | None = None,
        preset: QRartPreset | None = None,
        pattern: QRartPattern | None = None,
        pixel_style: QRartPixelStyle | None = None,
        position: QRartPosition | None = None,
        marker_shape: QRartMarkerShape | None = None,
        sub_marker: QRartSubMarker | None = None,
        padding_level: QRartPaddingLevel | None = None,
        padding_noise: QRartPaddingNoise | None = None,
        rotate: QRartRotate | None = None,
        rawurl: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Art QR Code generation API."""
        body: dict[str, Any] = {"prompt": prompt, "type": type}
        if content is not None:
            body["content"] = content
        if content_image_url is not None:
            body["content_image_url"] = content_image_url
        if ecl is not None:
            body["ecl"] = ecl
        if qrw is not None:
            body["qrw"] = qrw
        if seed is not None:
            body["seed"] = seed
        if steps is not None:
            body["steps"] = steps
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if preset is not None:
            body["preset"] = preset
        if pattern is not None:
            body["pattern"] = pattern
        if pixel_style is not None:
            body["pixel_style"] = pixel_style
        if position is not None:
            body["position"] = position
        if marker_shape is not None:
            body["marker_shape"] = marker_shape
        if sub_marker is not None:
            body["sub_marker"] = sub_marker
        if padding_level is not None:
            body["padding_level"] = padding_level
        if padding_noise is not None:
            body["padding_noise"] = padding_noise
        if rotate is not None:
            body["rotate"] = rotate
        if rawurl is not None:
            body["rawurl"] = rawurl
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/qrart/generate", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/qrart/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
