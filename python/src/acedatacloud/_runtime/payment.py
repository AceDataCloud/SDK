"""Pluggable payment handler hook for the SDK transport.

When the API returns ``402 Payment Required``, the transport calls the
configured payment handler to obtain the extra headers (typically
``PAYMENT-SIGNATURE``) to attach to the retry. This keeps the SDK free of any
chain-specific signing logic, and lets callers plug in an x402
implementation when one becomes available.
"""

from __future__ import annotations

import base64
import json
from collections.abc import Awaitable, Mapping
from typing import Any, Callable, TypedDict, Union


class PaymentRequirement(TypedDict, total=False):
    scheme: str
    network: str
    amount: str
    maxAmountRequired: str
    maxTimeoutSeconds: int
    resource: str
    description: str
    payTo: str
    asset: str
    extra: dict[str, Any]


class PaymentRequiredBody(TypedDict, total=False):
    x402Version: int
    accepts: list[PaymentRequirement]
    error: str


class PaymentHandlerContext(TypedDict):
    url: str
    method: str
    body: Any
    accepts: list[PaymentRequirement]


class PaymentHandlerResult(TypedDict):
    headers: dict[str, str]


SyncPaymentHandler = Callable[[PaymentHandlerContext], PaymentHandlerResult]
AsyncPaymentHandler = Callable[[PaymentHandlerContext], Awaitable[PaymentHandlerResult]]
PaymentHandler = Union[SyncPaymentHandler, AsyncPaymentHandler]


def parse_payment_required(headers: Mapping[str, str], body: Any) -> dict[str, Any]:
    encoded = headers.get("PAYMENT-REQUIRED") or headers.get("payment-required")
    if encoded:
        try:
            value = json.loads(base64.b64decode(encoded).decode("utf-8"))
        except Exception as exc:
            raise ValueError("Invalid PAYMENT-REQUIRED header") from exc
        if isinstance(value, dict):
            return value
        raise ValueError("Invalid PAYMENT-REQUIRED header")
    if isinstance(body, dict):
        return body
    if isinstance(body, (bytes, bytearray)):
        body = body.decode("utf-8", errors="replace")
    if isinstance(body, str):
        try:
            value = json.loads(body)
        except Exception:
            return {}
        if isinstance(value, dict):
            return value
    return {}
