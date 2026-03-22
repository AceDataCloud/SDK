"""Search resources."""

from __future__ import annotations

from typing import Any


class Search:
    """Synchronous search client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def google(
        self,
        *,
        query: str,
        type: str = "search",
        country: str | None = None,
        language: str | None = None,
        page: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query, "type": type, **kwargs}
        if country is not None:
            body["country"] = country
        if language is not None:
            body["language"] = language
        if page is not None:
            body["page"] = page
        return self._transport.request("POST", "/serp/google", json=body)


class AsyncSearch:
    """Async search client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def google(
        self,
        *,
        query: str,
        type: str = "search",
        country: str | None = None,
        language: str | None = None,
        page: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query, "type": type, **kwargs}
        if country is not None:
            body["country"] = country
        if language is not None:
            body["language"] = language
        if page is not None:
            body["page"] = page
        return await self._transport.request("POST", "/serp/google", json=body)
