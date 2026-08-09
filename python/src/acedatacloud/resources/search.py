"""Search resources."""

from __future__ import annotations

from typing import Any, Literal

SearchType = Literal["search", "images", "news", "maps", "places", "videos"]
SearchRange = Literal["h", "d", "w", "m", "y", "qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"]
SearchImageSize = Literal[
    "large",
    "medium",
    "icon",
    "2mp",
    "4mp",
    "6mp",
    "8mp",
    "10mp",
    "12mp",
    "15mp",
    "20mp",
    "40mp",
    "70mp",
]


class Search:
    """Synchronous search client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def google(
        self,
        *,
        query: str,
        type: SearchType = "search",
        country: str | None = None,
        language: str | None = None,
        page: int | None = None,
        range: SearchRange | None = None,
        number: int | None = None,
        image_size: SearchImageSize | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query, "type": type, **kwargs}
        if country is not None:
            body["country"] = country
        if language is not None:
            body["language"] = language
        if page is not None:
            body["page"] = page
        if range is not None:
            body["range"] = range
        if number is not None:
            body["number"] = number
        if image_size is not None:
            body["image_size"] = image_size
        return self._transport.request("POST", "/serp/google", json=body)


class AsyncSearch:
    """Async search client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def google(
        self,
        *,
        query: str,
        type: SearchType = "search",
        country: str | None = None,
        language: str | None = None,
        page: int | None = None,
        range: SearchRange | None = None,
        number: int | None = None,
        image_size: SearchImageSize | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query, "type": type, **kwargs}
        if country is not None:
            body["country"] = country
        if language is not None:
            body["language"] = language
        if page is not None:
            body["page"] = page
        if range is not None:
            body["range"] = range
        if number is not None:
            body["number"] = number
        if image_size is not None:
            body["image_size"] = image_size
        return await self._transport.request("POST", "/serp/google", json=body)
