"""HTTP transport layer for AceDataCloud SDK."""

from __future__ import annotations

import inspect
import os
import random
import time
from collections.abc import Iterator
from typing import Any

import httpx

from acedatacloud._runtime.errors import (
    APIError,
    AuthenticationError,
    InsufficientBalanceError,
    ModerationError,
    RateLimitError,
    ResourceDisabledError,
    TimeoutError,
    TokenMismatchError,
    TransportError,
    ValidationError,
)
from acedatacloud._runtime.payment import (
    PaymentHandler,
    SyncPaymentHandler,
)

_ERROR_CODE_MAP = {
    "invalid_token": AuthenticationError,
    "token_expired": AuthenticationError,
    "no_token": AuthenticationError,
    "token_mismatched": TokenMismatchError,
    "used_up": InsufficientBalanceError,
    "disabled": ResourceDisabledError,
    "too_many_requests": RateLimitError,
    "bad_request": ValidationError,
}

_RETRY_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}


def _map_error(status_code: int, body: dict[str, Any]) -> APIError:
    """Map an API error response to the appropriate exception class."""
    error_data = body.get("error", {})
    code = error_data.get("code", "")
    message = error_data.get("message", "")
    trace_id = body.get("trace_id")

    exc_class = _ERROR_CODE_MAP.get(code)
    if exc_class is None:
        if status_code == 403:
            exc_class = ModerationError
        elif status_code == 401:
            exc_class = AuthenticationError
        elif status_code == 429:
            exc_class = RateLimitError
        elif status_code == 400:
            exc_class = ValidationError
        else:
            exc_class = APIError

    return exc_class(
        message=message,
        status_code=status_code,
        code=code,
        trace_id=trace_id,
        body=body,
    )


def _should_retry(status_code: int) -> bool:
    return status_code in _RETRY_STATUS_CODES


def _backoff_delay(attempt: int) -> float:
    base = min(2**attempt, 8)
    jitter = random.random() * 0.5  # noqa: S311
    return base + jitter


class SyncTransport:
    """Synchronous HTTP transport using httpx."""

    def __init__(
        self,
        api_token: str | None,
        base_url: str,
        platform_base_url: str,
        timeout: float,
        max_retries: int,
        extra_headers: dict[str, str],
        payment_handler: SyncPaymentHandler | None = None,
    ) -> None:
        token = api_token or os.environ.get("ACEDATACLOUD_API_TOKEN", "")
        if not token and payment_handler is None:
            raise AuthenticationError(
                message=(
                    "api_token is required (or provide a payment_handler). "
                    "Pass it to the client or set ACEDATACLOUD_API_TOKEN."
                ),
                status_code=0,
                code="no_token",
            )
        self._base_url = base_url.rstrip("/")
        self._platform_base_url = platform_base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._payment_handler = payment_handler
        headers: dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": "acedatacloud-python/0.1.0",
            **extra_headers,
        }
        if token:
            headers["authorization"] = f"Bearer {token}"
        self._headers = headers
        self._client = httpx.Client(timeout=timeout)

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        platform: bool = False,
        timeout: float | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        base = self._platform_base_url if platform else self._base_url
        url = f"{base}{path}"
        headers = {**self._headers, **(extra_headers or {})}
        extra_auth_headers: dict[str, str] = {}
        payment_attempted = False

        last_exc: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                resp = self._client.request(
                    method,
                    url,
                    json=json,
                    params=params,
                    headers={**headers, **extra_auth_headers},
                    timeout=timeout or self._timeout,
                )
            except httpx.TimeoutException as exc:
                last_exc = TimeoutError(
                    message=f"Request timed out: {exc}",
                    status_code=0,
                    code="timeout",
                )
                if attempt < self._max_retries:
                    time.sleep(_backoff_delay(attempt))
                    continue
                raise last_exc from exc
            except httpx.TransportError as exc:
                last_exc = TransportError(str(exc))
                if attempt < self._max_retries:
                    time.sleep(_backoff_delay(attempt))
                    continue
                raise last_exc from exc

            if (
                resp.status_code == 402
                and self._payment_handler is not None
                and not payment_attempted
            ):
                try:
                    body = resp.json()
                except Exception as exc:
                    raise _map_error(
                        402,
                        {"error": {"code": "invalid_402", "message": resp.text}},
                    ) from exc
                accepts = body.get("accepts") or []
                if not accepts:
                    raise _map_error(
                        402,
                        {"error": {"code": "invalid_402", "message": "No payment requirements"}},
                    )
                result = self._payment_handler(
                    {"url": url, "method": method, "body": json, "accepts": accepts}
                )
                extra_auth_headers.update(result.get("headers", {}))
                payment_attempted = True
                continue

            if resp.status_code >= 400:
                try:
                    body = resp.json()
                except Exception:
                    body = {"error": {"code": "unknown", "message": resp.text}}

                if _should_retry(resp.status_code) and attempt < self._max_retries:
                    time.sleep(_backoff_delay(attempt))
                    continue
                raise _map_error(resp.status_code, body)

            return resp.json()

        raise last_exc or TransportError("Request failed after retries")

    def request_stream(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        timeout: float | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> Iterator[str]:
        """Send a request and yield SSE data lines."""
        base = self._base_url
        url = f"{base}{path}"
        headers = {
            **self._headers,
            "accept": "text/event-stream",
            **(extra_headers or {}),
        }

        with self._client.stream(
            method,
            url,
            json=json,
            headers=headers,
            timeout=timeout or self._timeout,
        ) as resp:
            if resp.status_code >= 400:
                body_bytes = resp.read()
                try:
                    import json as _json

                    body = _json.loads(body_bytes)
                except Exception:
                    body = {"error": {"code": "unknown", "message": body_bytes.decode(errors="replace")}}
                raise _map_error(resp.status_code, body)

            for line in resp.iter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        return
                    yield data

    def upload(
        self,
        path: str,
        file_data: bytes,
        filename: str,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        url = f"{self._platform_base_url}{path}"
        headers = {k: v for k, v in self._headers.items() if k != "content-type"}

        resp = self._client.post(
            url,
            files={"file": (filename, file_data)},
            headers=headers,
            timeout=timeout or self._timeout,
        )
        if resp.status_code >= 400:
            try:
                body = resp.json()
            except Exception:
                body = {"error": {"code": "unknown", "message": resp.text}}
            raise _map_error(resp.status_code, body)
        return resp.json()

    def close(self) -> None:
        self._client.close()


class AsyncTransport:
    """Asynchronous HTTP transport using httpx."""

    def __init__(
        self,
        api_token: str | None,
        base_url: str,
        platform_base_url: str,
        timeout: float,
        max_retries: int,
        extra_headers: dict[str, str],
        payment_handler: PaymentHandler | None = None,
    ) -> None:

        token = api_token or os.environ.get("ACEDATACLOUD_API_TOKEN", "")
        if not token and payment_handler is None:
            raise AuthenticationError(
                message=(
                    "api_token is required (or provide a payment_handler). "
                    "Pass it to the client or set ACEDATACLOUD_API_TOKEN."
                ),
                status_code=0,
                code="no_token",
            )
        self._base_url = base_url.rstrip("/")
        self._platform_base_url = platform_base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._payment_handler = payment_handler
        headers: dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": "acedatacloud-python/0.1.0",
            **extra_headers,
        }
        if token:
            headers["authorization"] = f"Bearer {token}"
        self._headers = headers
        self._client = httpx.AsyncClient(timeout=timeout)

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        platform: bool = False,
        timeout: float | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        import asyncio

        base = self._platform_base_url if platform else self._base_url
        url = f"{base}{path}"
        headers = {**self._headers, **(extra_headers or {})}
        extra_auth_headers: dict[str, str] = {}
        payment_attempted = False

        last_exc: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                resp = await self._client.request(
                    method,
                    url,
                    json=json,
                    params=params,
                    headers={**headers, **extra_auth_headers},
                    timeout=timeout or self._timeout,
                )
            except httpx.TimeoutException as exc:
                last_exc = TimeoutError(
                    message=f"Request timed out: {exc}",
                    status_code=0,
                    code="timeout",
                )
                if attempt < self._max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue
                raise last_exc from exc
            except httpx.TransportError as exc:
                last_exc = TransportError(str(exc))
                if attempt < self._max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue
                raise last_exc from exc

            if (
                resp.status_code == 402
                and self._payment_handler is not None
                and not payment_attempted
            ):
                try:
                    body = resp.json()
                except Exception as exc:
                    raise _map_error(
                        402,
                        {"error": {"code": "invalid_402", "message": resp.text}},
                    ) from exc
                accepts = body.get("accepts") or []
                if not accepts:
                    raise _map_error(
                        402,
                        {"error": {"code": "invalid_402", "message": "No payment requirements"}},
                    )
                handler_result = self._payment_handler(
                    {"url": url, "method": method, "body": json, "accepts": accepts}
                )
                if inspect.isawaitable(handler_result):
                    handler_result = await handler_result
                extra_auth_headers.update(handler_result.get("headers", {}))
                payment_attempted = True
                continue

            if resp.status_code >= 400:
                try:
                    body = resp.json()
                except Exception:
                    body = {"error": {"code": "unknown", "message": resp.text}}

                if _should_retry(resp.status_code) and attempt < self._max_retries:
                    await asyncio.sleep(_backoff_delay(attempt))
                    continue
                raise _map_error(resp.status_code, body)

            return resp.json()

        raise last_exc or TransportError("Request failed after retries")

    async def request_stream(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        timeout: float | None = None,
        extra_headers: dict[str, str] | None = None,
    ):
        """Send a request and yield SSE data lines asynchronously."""
        base = self._base_url
        url = f"{base}{path}"
        headers = {
            **self._headers,
            "accept": "text/event-stream",
            **(extra_headers or {}),
        }

        async with self._client.stream(
            method,
            url,
            json=json,
            headers=headers,
            timeout=timeout or self._timeout,
        ) as resp:
            if resp.status_code >= 400:
                body_bytes = await resp.aread()
                try:
                    import json as _json

                    body = _json.loads(body_bytes)
                except Exception:
                    body = {"error": {"code": "unknown", "message": body_bytes.decode(errors="replace")}}
                raise _map_error(resp.status_code, body)

            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        return
                    yield data

    async def upload(
        self,
        path: str,
        file_data: bytes,
        filename: str,
        *,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        url = f"{self._platform_base_url}{path}"
        headers = {k: v for k, v in self._headers.items() if k != "content-type"}

        resp = await self._client.post(
            url,
            files={"file": (filename, file_data)},
            headers=headers,
            timeout=timeout or self._timeout,
        )
        if resp.status_code >= 400:
            try:
                body = resp.json()
            except Exception:
                body = {"error": {"code": "unknown", "message": resp.text}}
            raise _map_error(resp.status_code, body)
        return resp.json()

    async def close(self) -> None:
        await self._client.aclose()
