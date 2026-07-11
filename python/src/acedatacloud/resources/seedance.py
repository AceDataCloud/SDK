"""Seedance-specific video generation resources."""

from __future__ import annotations

from typing import Any, Literal

SeedanceModel = Literal[
    "doubao-seedance-1-0-pro-250528",
    "doubao-seedance-1-0-pro-fast-251015",
    "doubao-seedance-1-5-pro-251215",
    "doubao-seedance-1-0-lite-t2v-250428",
    "doubao-seedance-1-0-lite-i2v-250428",
    "doubao-seedance-2-0-260128",
    "doubao-seedance-2-0-fast-260128",
    "doubao-seedance-2-0-mini-260615",
]


class Seedance:
    """Synchronous Seedance video client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def generate(
        self,
        *,
        model: SeedanceModel | str,
        content: list[dict[str, Any]],
        resolution: Literal["480p", "720p", "1080p", "4k"] | None = None,
        ratio: Literal["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"] | None = None,
        duration: int | None = None,
        frames: int | None = None,
        seed: int | None = None,
        camerafixed: bool | None = None,
        watermark: bool | None = None,
        generate_audio: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        return_last_frame: bool | None = None,
        execution_expires_after: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, "content": content, **kwargs}
        if resolution is not None:
            body["resolution"] = resolution
        if ratio is not None:
            body["ratio"] = ratio
        if duration is not None:
            body["duration"] = duration
        if frames is not None:
            body["frames"] = frames
        if seed is not None:
            body["seed"] = seed
        if camerafixed is not None:
            body["camerafixed"] = camerafixed
        if watermark is not None:
            body["watermark"] = watermark
        if generate_audio is not None:
            body["generate_audio"] = generate_audio
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        if return_last_frame is not None:
            body["return_last_frame"] = return_last_frame
        if execution_expires_after is not None:
            body["execution_expires_after"] = execution_expires_after
        return self._transport.request("POST", "/seedance/videos", json=body)


class AsyncSeedance:
    """Async Seedance video client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def generate(
        self,
        *,
        model: SeedanceModel | str,
        content: list[dict[str, Any]],
        resolution: Literal["480p", "720p", "1080p", "4k"] | None = None,
        ratio: Literal["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"] | None = None,
        duration: int | None = None,
        frames: int | None = None,
        seed: int | None = None,
        camerafixed: bool | None = None,
        watermark: bool | None = None,
        generate_audio: bool | None = None,
        callback_url: str | None = None,
        async_: bool | None = None,
        return_last_frame: bool | None = None,
        execution_expires_after: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, "content": content, **kwargs}
        if resolution is not None:
            body["resolution"] = resolution
        if ratio is not None:
            body["ratio"] = ratio
        if duration is not None:
            body["duration"] = duration
        if frames is not None:
            body["frames"] = frames
        if seed is not None:
            body["seed"] = seed
        if camerafixed is not None:
            body["camerafixed"] = camerafixed
        if watermark is not None:
            body["watermark"] = watermark
        if generate_audio is not None:
            body["generate_audio"] = generate_audio
        if callback_url is not None:
            body["callback_url"] = callback_url
        if async_ is not None:
            body["async"] = async_
        if return_last_frame is not None:
            body["return_last_frame"] = return_last_frame
        if execution_expires_after is not None:
            body["execution_expires_after"] = execution_expires_after
        return await self._transport.request("POST", "/seedance/videos", json=body)
