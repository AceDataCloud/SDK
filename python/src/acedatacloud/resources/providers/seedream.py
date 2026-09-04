"""Seedream (seedream) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

SeedreamModel = Literal[
    "doubao-seedream-5-0-pro-260628",
    "doubao-seedream-5-0-260128",
    "doubao-seedream-5-0-lite-260128",
    "doubao-seedream-4-0-250828",
    "doubao-seedream-4-5-251128",
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


class Seedream:
    """Synchronous seedream client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        model: SeedreamModel,
        prompt: str | None = None,
        image: str | list[str] | None = None,
        size: Literal["1K", "1.5K", "2K", "3K", "4K", "auto"] | str | None = None,
        sequential_image_generation: Literal["auto", "disabled"] | None = None,
        sequential_image_generation_options: dict[str, Any] | None = None,
        stream: bool | None = None,
        response_format: Literal["url", "b64_json"] | None = None,
        watermark: bool | None = None,
        output_format: Literal["jpeg", "png"] | None = None,
        tools: list[dict[str, Any]] | None = None,
        optimize_prompt_options: dict[str, Any] | None = None,
        layer_decomposition: bool | None = None,
        background: Literal["transparent", "opaque"] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Call /seedream/images."""
        body: dict[str, Any] = {}
        body["model"] = model
        if prompt is not None:
            body["prompt"] = prompt
        if image is not None:
            body["image"] = image
        if size is not None:
            body["size"] = size
        if sequential_image_generation is not None:
            body["sequential_image_generation"] = sequential_image_generation
        if sequential_image_generation_options is not None:
            body["sequential_image_generation_options"] = sequential_image_generation_options
        if stream is not None:
            body["stream"] = stream
        if response_format is not None:
            body["response_format"] = response_format
        if watermark is not None:
            body["watermark"] = watermark
        if output_format is not None:
            body["output_format"] = output_format
        if tools is not None:
            body["tools"] = tools
        if optimize_prompt_options is not None:
            body["optimize_prompt_options"] = optimize_prompt_options
        if layer_decomposition is not None:
            body["layer_decomposition"] = layer_decomposition
        if background is not None:
            body["background"] = background
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/seedream/images", json=body)
        handle = TaskHandle(_task_id(result), "/seedream/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncSeedream:
    """Asynchronous seedream client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        model: SeedreamModel,
        prompt: str | None = None,
        image: str | list[str] | None = None,
        size: Literal["1K", "1.5K", "2K", "3K", "4K", "auto"] | str | None = None,
        sequential_image_generation: Literal["auto", "disabled"] | None = None,
        sequential_image_generation_options: dict[str, Any] | None = None,
        stream: bool | None = None,
        response_format: Literal["url", "b64_json"] | None = None,
        watermark: bool | None = None,
        output_format: Literal["jpeg", "png"] | None = None,
        tools: list[dict[str, Any]] | None = None,
        optimize_prompt_options: dict[str, Any] | None = None,
        layer_decomposition: bool | None = None,
        background: Literal["transparent", "opaque"] | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Call /seedream/images."""
        body: dict[str, Any] = {}
        body["model"] = model
        if prompt is not None:
            body["prompt"] = prompt
        if image is not None:
            body["image"] = image
        if size is not None:
            body["size"] = size
        if sequential_image_generation is not None:
            body["sequential_image_generation"] = sequential_image_generation
        if sequential_image_generation_options is not None:
            body["sequential_image_generation_options"] = sequential_image_generation_options
        if stream is not None:
            body["stream"] = stream
        if response_format is not None:
            body["response_format"] = response_format
        if watermark is not None:
            body["watermark"] = watermark
        if output_format is not None:
            body["output_format"] = output_format
        if tools is not None:
            body["tools"] = tools
        if optimize_prompt_options is not None:
            body["optimize_prompt_options"] = optimize_prompt_options
        if layer_decomposition is not None:
            body["layer_decomposition"] = layer_decomposition
        if background is not None:
            body["background"] = background
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/seedream/images", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/seedream/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
