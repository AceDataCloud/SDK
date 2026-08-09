"""Search resources."""

from __future__ import annotations

from typing import Any, Literal

SearchType = Literal["search", "images", "news", "maps", "places", "videos"]
SearchRange = Literal["h", "d", "w", "m", "y", "qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"]
ImageSize = Literal[
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
_SEARCH_TYPES = {"search", "images", "news", "maps", "places", "videos"}
_SEARCH_RANGES = {"h", "d", "w", "m", "y", "qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"}
_IMAGE_SIZES = {"large", "medium", "icon", "2mp", "4mp", "6mp", "8mp", "10mp", "12mp", "15mp", "20mp", "40mp", "70mp"}


def _build_google_search_body(
    *,
    query: str,
    type: SearchType,
    page: int | None,
    range: SearchRange | None,
    number: int | None,
    country: str | None,
    language: str | None,
    image_size: ImageSize | None,
    extra: dict[str, Any],
) -> dict[str, Any]:
    if not 1 <= len(query) <= 2048 or not query.strip():
        raise ValueError("query must be 1 to 2048 characters and contain at least one non-whitespace character")
    if type not in _SEARCH_TYPES:
        raise ValueError(f"unsupported search type: {type}")
    if page is not None and not 1 <= page <= 100:
        raise ValueError("page must be between 1 and 100")
    if number is not None and not 1 <= number <= 100:
        raise ValueError("number must be between 1 and 100")
    if range is not None and range not in _SEARCH_RANGES:
        raise ValueError(f"unsupported search range: {range}")
    if country is not None and not 1 <= len(country) <= 32:
        raise ValueError("country must be 1 to 32 characters")
    if language is not None and not 1 <= len(language) <= 32:
        raise ValueError("language must be 1 to 32 characters")
    if image_size is not None and image_size not in _IMAGE_SIZES:
        raise ValueError(f"unsupported image size: {image_size}")
    if image_size is not None and type != "images":
        raise ValueError("image_size is only valid when type is 'images'")

    body: dict[str, Any] = {"query": query, "type": type, **extra}
    for key, value in {
        "page": page,
        "range": range,
        "number": number,
        "country": country,
        "language": language,
        "image_size": image_size,
    }.items():
        if value is not None:
            body[key] = value
    return body


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
        image_size: ImageSize | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = _build_google_search_body(
            query=query,
            type=type,
            country=country,
            language=language,
            page=page,
            range=range,
            number=number,
            image_size=image_size,
            extra=kwargs,
        )
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
        image_size: ImageSize | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = _build_google_search_body(
            query=query,
            type=type,
            country=country,
            language=language,
            page=page,
            range=range,
            number=number,
            image_size=image_size,
            extra=kwargs,
        )
        return await self._transport.request("POST", "/serp/google", json=body)
