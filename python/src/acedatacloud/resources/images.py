"""Image generation resources."""

from __future__ import annotations

from typing import Any, Literal

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

ImageProvider = Literal["nano-banana", "flux", "seedream", "hcaptcha", "image2text", "recaptcha"]

_IMAGE_ENDPOINTS = {
    "hcaptcha": "/captcha/recognition/hcaptcha",
    "image2text": "/captcha/recognition/image2text",
    "recaptcha": "/captcha/recognition/recaptcha2",
}


class Images:
    """Synchronous image generation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        prompt: str | None = None,
        provider: ImageProvider | str = "nano-banana",
        action: Literal["generate", "edit"] | None = None,
        model: str | None = None,
        negative_prompt: str | None = None,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        image: str | None = None,
        question: str | None = None,
        queries: Any | None = None,
        website_key: str | None = None,
        website_url: str | None = None,
        page_action: str | None = None,
        aspect_ratio: str | None = None,
        resolution: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | TaskHandle:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None and provider not in _IMAGE_ENDPOINTS:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if model is not None:
            body["model"] = model
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if image is not None:
            body["image"] = image
        if question is not None:
            body["question"] = question
        if queries is not None:
            body["queries"] = queries
        if website_key is not None:
            body["website_key"] = website_key
        if website_url is not None:
            body["website_url"] = website_url
        if page_action is not None:
            body["page_action"] = page_action
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if resolution is not None:
            body["resolution"] = resolution
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        endpoint = _IMAGE_ENDPOINTS.get(provider, f"/{provider}/images")
        if prompt is None and provider not in _IMAGE_ENDPOINTS:
            raise ValueError("prompt is required for image generation providers")
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
        prompt: str | None = None,
        provider: ImageProvider | str = "nano-banana",
        action: Literal["generate", "edit"] | None = None,
        model: str | None = None,
        negative_prompt: str | None = None,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        image: str | None = None,
        question: str | None = None,
        queries: Any | None = None,
        website_key: str | None = None,
        website_url: str | None = None,
        page_action: str | None = None,
        aspect_ratio: str | None = None,
        resolution: str | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        **kwargs: Any,
    ) -> dict[str, Any] | AsyncTaskHandle:
        body: dict[str, Any] = {**kwargs}
        if prompt is not None and provider not in _IMAGE_ENDPOINTS:
            body["prompt"] = prompt
        if action is not None:
            body["action"] = action
        if model is not None:
            body["model"] = model
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if image_url is not None:
            body["image_url"] = image_url
        if image_urls is not None:
            body["image_urls"] = image_urls
        if image is not None:
            body["image"] = image
        if question is not None:
            body["question"] = question
        if queries is not None:
            body["queries"] = queries
        if website_key is not None:
            body["website_key"] = website_key
        if website_url is not None:
            body["website_url"] = website_url
        if page_action is not None:
            body["page_action"] = page_action
        if aspect_ratio is not None:
            body["aspect_ratio"] = aspect_ratio
        if resolution is not None:
            body["resolution"] = resolution
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_

        endpoint = _IMAGE_ENDPOINTS.get(provider, f"/{provider}/images")
        if prompt is None and provider not in _IMAGE_ENDPOINTS:
            raise ValueError("prompt is required for image generation providers")
        result = await self._transport.request("POST", endpoint, json=body)
        task_id = result.get("task_id")

        if not task_id or (result.get("data") and not wait):
            return result

        handle = AsyncTaskHandle(task_id, f"/{provider}/tasks", self._transport)
        if wait:
            return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
