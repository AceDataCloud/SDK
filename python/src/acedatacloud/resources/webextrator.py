"""WebExtrator web render & extract resources."""

from __future__ import annotations

from typing import Any, Literal


class WebExtrator:
    """Synchronous WebExtrator client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def extract(
        self,
        *,
        url: str,
        expected_type: Literal["product", "article", "general"] | None = None,
        enable_llm: bool | None = None,
        wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] | None = None,
        timeout: float | None = None,
        delay: float | None = None,
        wait_for_selector: str | None = None,
        block_resources: list[str] | None = None,
        headers: dict[str, str] | None = None,
        user_agent: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"url": url, **kwargs}
        if expected_type is not None:
            body["expected_type"] = expected_type
        if enable_llm is not None:
            body["enable_llm"] = enable_llm
        if wait_until is not None:
            body["wait_until"] = wait_until
        if timeout is not None:
            body["timeout"] = timeout
        if delay is not None:
            body["delay"] = delay
        if wait_for_selector is not None:
            body["wait_for_selector"] = wait_for_selector
        if block_resources is not None:
            body["block_resources"] = block_resources
        if headers is not None:
            body["headers"] = headers
        if user_agent is not None:
            body["user_agent"] = user_agent
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/webextrator/extract", json=body)

    def render(
        self,
        *,
        url: str,
        wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] | None = None,
        timeout: float | None = None,
        delay: float | None = None,
        wait_for_selector: str | None = None,
        block_resources: list[str] | None = None,
        headers: dict[str, str] | None = None,
        user_agent: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"url": url, **kwargs}
        if wait_until is not None:
            body["wait_until"] = wait_until
        if timeout is not None:
            body["timeout"] = timeout
        if delay is not None:
            body["delay"] = delay
        if wait_for_selector is not None:
            body["wait_for_selector"] = wait_for_selector
        if block_resources is not None:
            body["block_resources"] = block_resources
        if headers is not None:
            body["headers"] = headers
        if user_agent is not None:
            body["user_agent"] = user_agent
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/webextrator/render", json=body)


class AsyncWebExtrator:
    """Async WebExtrator client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def extract(
        self,
        *,
        url: str,
        expected_type: Literal["product", "article", "general"] | None = None,
        enable_llm: bool | None = None,
        wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] | None = None,
        timeout: float | None = None,
        delay: float | None = None,
        wait_for_selector: str | None = None,
        block_resources: list[str] | None = None,
        headers: dict[str, str] | None = None,
        user_agent: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"url": url, **kwargs}
        if expected_type is not None:
            body["expected_type"] = expected_type
        if enable_llm is not None:
            body["enable_llm"] = enable_llm
        if wait_until is not None:
            body["wait_until"] = wait_until
        if timeout is not None:
            body["timeout"] = timeout
        if delay is not None:
            body["delay"] = delay
        if wait_for_selector is not None:
            body["wait_for_selector"] = wait_for_selector
        if block_resources is not None:
            body["block_resources"] = block_resources
        if headers is not None:
            body["headers"] = headers
        if user_agent is not None:
            body["user_agent"] = user_agent
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/webextrator/extract", json=body)

    async def render(
        self,
        *,
        url: str,
        wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] | None = None,
        timeout: float | None = None,
        delay: float | None = None,
        wait_for_selector: str | None = None,
        block_resources: list[str] | None = None,
        headers: dict[str, str] | None = None,
        user_agent: str | None = None,
        callback_url: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"url": url, **kwargs}
        if wait_until is not None:
            body["wait_until"] = wait_until
        if timeout is not None:
            body["timeout"] = timeout
        if delay is not None:
            body["delay"] = delay
        if wait_for_selector is not None:
            body["wait_for_selector"] = wait_for_selector
        if block_resources is not None:
            body["block_resources"] = block_resources
        if headers is not None:
            body["headers"] = headers
        if user_agent is not None:
            body["user_agent"] = user_agent
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/webextrator/render", json=body)
