"""Image generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

ImageProvider = Literal["nano-banana", "flux", "seedream"]


class Images:
    """Synchronous image generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str,
        provider: ImageProvider | str = "nano-banana",
        action: Literal["generate", "edit"] | None = None,
        model: str | None = None,
        negative_prompt: str | None = None,
        image: list[Any] | None = None,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        aspect_ratio: str | None = None,
        resolution: str | None = None,
        size: str | None = None,
        seed: int | None = None,
        guidance_scale: float | None = None,
        response_format: str | None = None,
        watermark: bool | None = None,
        output_format: str | None = None,
        stream: bool | None = None,
        sequential_image_generation: str | None = None,
        sequential_image_generation_options: dict[str, Any] | None = None,
        tools: list[Any] | None = None,
        optimize_prompt_options: dict[str, Any] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if action is not None:
            body["action"] = action
        if model is not None:
            body["model"] = model
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if image is not None:
            body["image"] = image
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if resolution is not None:
            body["resolution"] = resolution
        if size is not None:
            body["size"] = size
        if seed is not None:
            body["seed"] = seed
        if guidance_scale is not None:
            body["guidance_scale"] = guidance_scale
        if response_format is not None:
            body["response_format"] = response_format
        if watermark is not None:
            body["watermark"] = watermark
        if output_format is not None:
            body["output_format"] = output_format
        if stream is not None:
            body["stream"] = stream
        if sequential_image_generation is not None:
            body["sequential_image_generation"] = sequential_image_generation
        if sequential_image_generation_options is not None:
            body["sequential_image_generation_options"] = sequential_image_generation_options
        if tools is not None:
            body["tools"] = tools
        if optimize_prompt_options is not None:
            body["optimize_prompt_options"] = optimize_prompt_options
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        endpoint = f"/{provider}/images"
        result = self._transport.request("POST", endpoint, json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = TaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncImages:
    """Async image generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        prompt: str,
        provider: ImageProvider | str = "nano-banana",
        action: Literal["generate", "edit"] | None = None,
        model: str | None = None,
        negative_prompt: str | None = None,
        image: list[Any] | None = None,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        aspect_ratio: str | None = None,
        resolution: str | None = None,
        size: str | None = None,
        seed: int | None = None,
        guidance_scale: float | None = None,
        response_format: str | None = None,
        watermark: bool | None = None,
        output_format: str | None = None,
        stream: bool | None = None,
        sequential_image_generation: str | None = None,
        sequential_image_generation_options: dict[str, Any] | None = None,
        tools: list[Any] | None = None,
        optimize_prompt_options: dict[str, Any] | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {"prompt": prompt, **kwargs}
        if action is not None:
            body["action"] = action
        if model is not None:
            body["model"] = model
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if image is not None:
            body["image"] = image
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if resolution is not None:
            body["resolution"] = resolution
        if size is not None:
            body["size"] = size
        if seed is not None:
            body["seed"] = seed
        if guidance_scale is not None:
            body["guidance_scale"] = guidance_scale
        if response_format is not None:
            body["response_format"] = response_format
        if watermark is not None:
            body["watermark"] = watermark
        if output_format is not None:
            body["output_format"] = output_format
        if stream is not None:
            body["stream"] = stream
        if sequential_image_generation is not None:
            body["sequential_image_generation"] = sequential_image_generation
        if sequential_image_generation_options is not None:
            body["sequential_image_generation_options"] = sequential_image_generation_options
        if tools is not None:
            body["tools"] = tools
        if optimize_prompt_options is not None:
            body["optimize_prompt_options"] = optimize_prompt_options
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        endpoint = f"/{provider}/images"
        result = await self._transport.request("POST", endpoint, json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
