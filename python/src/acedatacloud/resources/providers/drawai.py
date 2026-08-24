"""Drawai (drawai) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

from ..._runtime.tasks import AsyncTaskHandle, TaskHandle

DrawaiTemplate = Literal[
    "male_portrait",
    "male_portrait2",
    "kindergarten",
    "logo_tshirt",
    "wedding",
    "business_photo",
    "bob_suit",
    "female_portrait",
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


class Drawai:
    """Synchronous drawai client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        mode: Literal["fast", "relax"],
        template: DrawaiTemplate,
        image_urls: list[str],
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> TaskHandle:
        """Generate"""
        body: dict[str, Any] = {}
        body["mode"] = mode
        body["template"] = template
        body["image_urls"] = image_urls
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = self._transport.request("POST", "/headshots/generate", json=body)
        handle = TaskHandle(_task_id(result), "/headshots/tasks", self._transport, submitted=result)
        if wait:
            handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle


class AsyncDrawai:
    """Asynchronous drawai client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        mode: Literal["fast", "relax"],
        template: DrawaiTemplate,
        image_urls: list[str],
        async_: bool | None = None,
        wait: bool = False,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
        callback_url: str | None = None,
        **extra: Any,
    ) -> AsyncTaskHandle:
        """Generate"""
        body: dict[str, Any] = {}
        body["mode"] = mode
        body["template"] = template
        body["image_urls"] = image_urls
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        body["async"] = True if async_ is None else async_
        result = await self._transport.request("POST", "/headshots/generate", json=body)
        handle = AsyncTaskHandle(_task_id(result), "/headshots/tasks", self._transport, submitted=result)
        if wait:
            await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
        return handle
