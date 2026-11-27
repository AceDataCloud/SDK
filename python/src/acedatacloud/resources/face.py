"""Face transformation resources (``/face/*``)."""

from __future__ import annotations

from typing import Any


class Face:
    """Synchronous face transformation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def _call(self, action: str, body: dict[str, Any]) -> dict[str, Any]:
        return self._transport.request("POST", f"/face/{action}", json=body)

    def analyze(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._call("analyze", {"image_url": image_url, **kwargs})

    def beautify(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._call("beautify", {"image_url": image_url, **kwargs})

    def change_age(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._call("change-age", {"image_url": image_url, **kwargs})

    def change_gender(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._call("change-gender", {"image_url": image_url, **kwargs})

    def detect_live(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._call("detect-live", {"image_url": image_url, **kwargs})

    def swap(self, *, source_image_url: str, target_image_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._call(
            "swap", {"source_image_url": source_image_url, "target_image_url": target_image_url, **kwargs}
        )

    def cartoon(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return self._call("cartoon", {"image_url": image_url, **kwargs})


class AsyncFace:
    """Async face transformation client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def _call(self, action: str, body: dict[str, Any]) -> dict[str, Any]:
        return await self._transport.request("POST", f"/face/{action}", json=body)

    async def analyze(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._call("analyze", {"image_url": image_url, **kwargs})

    async def beautify(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._call("beautify", {"image_url": image_url, **kwargs})

    async def change_age(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._call("change-age", {"image_url": image_url, **kwargs})

    async def change_gender(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._call("change-gender", {"image_url": image_url, **kwargs})

    async def detect_live(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._call("detect-live", {"image_url": image_url, **kwargs})

    async def swap(self, *, source_image_url: str, target_image_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._call(
            "swap", {"source_image_url": source_image_url, "target_image_url": target_image_url, **kwargs}
        )

    async def cartoon(self, *, image_url: str, **kwargs: Any) -> dict[str, Any]:
        return await self._call("cartoon", {"image_url": image_url, **kwargs})
