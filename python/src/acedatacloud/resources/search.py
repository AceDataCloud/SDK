"""Search resources."""

from __future__ import annotations

from typing import Any, Literal

SerpRange = Literal[
    "h",
    "d",
    "w",
    "m",
    "y",
    "qdr:h",
    "qdr:d",
    "qdr:w",
    "qdr:m",
    "qdr:y",
]
SerpImageSize = Literal[
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

_SERP_RANGES = {"h", "d", "w", "m", "y", "qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"}
_SERP_IMAGE_SIZES = {
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
}


def _build_google_body(
    *,
    query: str,
    type: str,
    country: str | None,
    language: str | None,
    page: int | None,
    number: int | None,
    range: SerpRange | None,
    image_size: SerpImageSize | None,
    extra: dict[str, Any],
) -> dict[str, Any]:
    if not query.strip() or len(query) > 2048:
        raise ValueError("query must contain 1 to 2048 characters and cannot be blank")
    page = 1 if page is None else page
    number = 10 if number is None else number
    if isinstance(page, bool) or not isinstance(page, int) or not 1 <= page <= 100:
        raise ValueError("page must be an integer between 1 and 100")
    if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= 100:
        raise ValueError("number must be an integer between 1 and 100")
    if country is not None and not 1 <= len(country) <= 32:
        raise ValueError("country must contain 1 to 32 characters")
    if language is not None and not 1 <= len(language) <= 32:
        raise ValueError("language must contain 1 to 32 characters")
    if range is not None and range not in _SERP_RANGES:
        raise ValueError(f"range must be one of: {', '.join(sorted(_SERP_RANGES))}")
    if image_size is not None and image_size not in _SERP_IMAGE_SIZES:
        raise ValueError(f"image_size must be one of: {', '.join(sorted(_SERP_IMAGE_SIZES))}")

    body: dict[str, Any] = {
        "query": query,
        "type": type,
        "page": page,
        "number": number,
        **extra,
    }
    if country is not None:
        body["country"] = country
    if language is not None:
        body["language"] = language
    if range is not None:
        body["range"] = range
    if image_size is not None:
        body["image_size"] = image_size
    return body


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
        page: int | None = 1,
        number: int | None = 10,
        range: SerpRange | None = None,
        image_size: SerpImageSize | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = _build_google_body(
            query=query,
            type=type,
            country=country,
            language=language,
            page=page,
            number=number,
            range=range,
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
        type: str = "search",
        country: str | None = None,
        language: str | None = None,
        page: int | None = 1,
        number: int | None = 10,
        range: SerpRange | None = None,
        image_size: SerpImageSize | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = _build_google_body(
            query=query,
            type=type,
            country=country,
            language=language,
            page=page,
            number=number,
            range=range,
            image_size=image_size,
            extra=kwargs,
        )
        return await self._transport.request("POST", "/serp/google", json=body)
