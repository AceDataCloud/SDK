"""QwenImage (qwen-image) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle


QwenImageModel = Literal[
    "qwen-image-3.0",
    "qwen-image-3.0-pro",
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


class QwenImage:
    """Synchronous qwen-image client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        model: QwenImageModel,
        prompt: str,
        image_urls: list[str] | None = None,
        n: int | None = None,
        size: str | None = None,
        prompt_extend: bool | None = None,
        prompt_extend_mode: Literal["direct", "agent"] | None = None,
        enable_thinking: bool | None = None,
        negative_prompt: str | None = None,
        seed: int | None = None,
        watermark: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Qwen Image Images"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["prompt"] = prompt
        if image_urls is not None:
            body["image_urls"] = image_urls
        body["n"] = n if n is not None else 1
        if size is not None:
            body["size"] = size
        body["prompt_extend"] = prompt_extend if prompt_extend is not None else True
        body["prompt_extend_mode"] = prompt_extend_mode if prompt_extend_mode is not None else "direct"
        body["enable_thinking"] = enable_thinking if enable_thinking is not None else True
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if seed is not None:
            body["seed"] = seed
        body["watermark"] = watermark if watermark is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/qwen-image/images", json=body)
        handle = TaskHandle(_task_id(result), "/qwen-image/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncQwenImage:
    """Asynchronous qwen-image client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        model: QwenImageModel,
        prompt: str,
        image_urls: list[str] | None = None,
        n: int | None = None,
        size: str | None = None,
        prompt_extend: bool | None = None,
        prompt_extend_mode: Literal["direct", "agent"] | None = None,
        enable_thinking: bool | None = None,
        negative_prompt: str | None = None,
        seed: int | None = None,
        watermark: bool | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Qwen Image Images"""
        body: dict[str, Any] = {}
        body["model"] = model
        body["prompt"] = prompt
        if image_urls is not None:
            body["image_urls"] = image_urls
        body["n"] = n if n is not None else 1
        if size is not None:
            body["size"] = size
        body["prompt_extend"] = prompt_extend if prompt_extend is not None else True
        body["prompt_extend_mode"] = prompt_extend_mode if prompt_extend_mode is not None else "direct"
        body["enable_thinking"] = enable_thinking if enable_thinking is not None else True
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if seed is not None:
            body["seed"] = seed
        body["watermark"] = watermark if watermark is not None else False
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/qwen-image/images", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/qwen-image/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
