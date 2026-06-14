"""ADSL Direct Connection Proxy resources."""

from __future__ import annotations

from typing import Any, Literal


class Adsl:
    """Synchronous ADSL proxy client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def extract(
        self,
        *,
        isp: Literal["电信", "联通", "移动"] | str | None = None,
        city: str | None = None,
        type: Literal["http", "socks"] | None = None,
        dedup: bool | None = None,
        number: int | None = None,
        duration: Literal[60, 180, 300] | None = None,
        province: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if isp is not None:
            body["isp"] = isp
        if city is not None:
            body["city"] = city
        if type is not None:
            body["type"] = type
        if dedup is not None:
            body["dedup"] = dedup
        if number is not None:
            body["number"] = number
        if duration is not None:
            body["duration"] = duration
        if province is not None:
            body["province"] = province
        return self._transport.request("POST", "/adsl/extract", json=body)

    def whitelist(
        self,
        *,
        ip: str | None = None,
        action: Literal["add", "delete"] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if ip is not None:
            body["ip"] = ip
        if action is not None:
            body["action"] = action
        return self._transport.request("POST", "/adsl/whitelist", json=body)


class AsyncAdsl:
    """Async ADSL proxy client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def extract(
        self,
        *,
        isp: Literal["电信", "联通", "移动"] | str | None = None,
        city: str | None = None,
        type: Literal["http", "socks"] | None = None,
        dedup: bool | None = None,
        number: int | None = None,
        duration: Literal[60, 180, 300] | None = None,
        province: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if isp is not None:
            body["isp"] = isp
        if city is not None:
            body["city"] = city
        if type is not None:
            body["type"] = type
        if dedup is not None:
            body["dedup"] = dedup
        if number is not None:
            body["number"] = number
        if duration is not None:
            body["duration"] = duration
        if province is not None:
            body["province"] = province
        return await self._transport.request("POST", "/adsl/extract", json=body)

    async def whitelist(
        self,
        *,
        ip: str | None = None,
        action: Literal["add", "delete"] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if ip is not None:
            body["ip"] = ip
        if action is not None:
            body["action"] = action
        return await self._transport.request("POST", "/adsl/whitelist", json=body)
