"""Pluggable payment handler hook for the SDK transport.

When the API returns ``402 Payment Required``, the transport calls the
configured payment handler to obtain the extra headers (typically
``X-Payment``) to attach to the retry. This keeps the SDK free of any
chain-specific signing logic, and lets callers plug in an x402
implementation when one becomes available.
"""

from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable, TypedDict, Union


class PaymentRequirement(TypedDict, total=False):
    scheme: str
    network: str
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
