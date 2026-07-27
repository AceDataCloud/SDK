"""Localization (localization) — generated from the platform OpenAPI spec.

Do not edit by hand: run ``python scripts/generate_providers.py``. Parameter
names, types, enums and required-ness all come from the live spec, so adding a
model upstream reaches the SDK without anyone retyping it.
"""

from __future__ import annotations

from typing import Any, Literal  # noqa: F401

LocalizationLocale = Literal[
    "en",
    "de",
    "pt",
    "es",
    "fr",
    "zh-CN",
    "zh-TW",
    "it",
    "ko",
    "ja",
    "ru",
    "pl",
    "fi",
    "sv",
    "el",
    "uk",
    "ar",
    "sr",
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


class Localization:
    """Synchronous localization client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def translate(
        self,
        *,
        input: dict[str, Any],
        locale: LocalizationLocale,
        extension: Literal["json", "md"],
        model: Literal["gpt-3.5", "gpt-4"] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Translate a JSON input into any localized file"""
        body: dict[str, Any] = {}
        body["input"] = input
        body["locale"] = locale
        body["extension"] = extension
        if model is not None:
            body["model"] = model
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return self._transport.request("POST", "/localization/translate", json=body)


class AsyncLocalization:
    """Asynchronous localization client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def translate(
        self,
        *,
        input: dict[str, Any],
        locale: LocalizationLocale,
        extension: Literal["json", "md"],
        model: Literal["gpt-3.5", "gpt-4"] | None = None,
        callback_url: str | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Translate a JSON input into any localized file"""
        body: dict[str, Any] = {}
        body["input"] = input
        body["locale"] = locale
        body["extension"] = extension
        if model is not None:
            body["model"] = model
        body.update(extra)
        if callback_url is not None:
            body["callback_url"] = callback_url
        return await self._transport.request("POST", "/localization/translate", json=body)
