"""Error hierarchy for AceDataCloud SDK."""

from __future__ import annotations

from typing import Any


class AceDataCloudError(Exception):
    """Base exception for all AceDataCloud SDK errors."""


class TransportError(AceDataCloudError):
    """Network-level transport failures."""


class APIError(AceDataCloudError):
    """Base class for API-level errors returned by the server."""

    def __init__(
        self,
        message: str = "",
        status_code: int = 0,
        code: str = "",
        trace_id: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        self.trace_id = trace_id
        self.body = body or {}
        super().__init__(message)


class AuthenticationError(APIError):
    """Invalid or missing API token."""


class TokenMismatchError(APIError):
    """Token does not match the requested resource."""


class PermissionError(APIError):
    """Insufficient permissions."""


class RateLimitError(APIError):
    """Request rate limit exceeded."""


class ValidationError(APIError):
    """Invalid request parameters."""


class InsufficientBalanceError(APIError):
    """Account balance insufficient for this request."""


class ResourceDisabledError(APIError):
    """The requested resource is disabled."""


class ModerationError(APIError):
    """Content blocked by moderation policy."""


class TimeoutError(APIError):
    """Request timed out."""


class InternalServerError(APIError):
    """Server-side error."""
