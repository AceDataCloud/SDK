"""Regression tests for _map_error body-shape handling."""

from __future__ import annotations

import pytest

from acedatacloud import APIError
from acedatacloud._runtime.transport import _map_error


def test_error_as_string_is_used_as_message():
    # The x402 facilitator occasionally returns ``{"error": "<string>"}``.
    exc = _map_error(402, {"error": "Facilitator verify returned empty body"})
    assert isinstance(exc, APIError)
    assert exc.status_code == 402
    assert exc.code == ""
    assert "Facilitator verify" in (exc.message or "")


def test_error_missing_uses_empty_defaults():
    exc = _map_error(500, {})
    assert isinstance(exc, APIError)
    assert exc.status_code == 500
    assert exc.code == ""


def test_error_as_dict_unchanged():
    exc = _map_error(
        400,
        {"error": {"code": "bad_request", "message": "missing field"}, "trace_id": "t-1"},
    )
    assert exc.status_code == 400
    assert exc.code == "bad_request"
    assert "missing field" in (exc.message or "")
    assert exc.trace_id == "t-1"


def test_error_as_non_mapping_non_string_falls_back():
    # Defensive: if the server returns a list under "error", don't crash.
    exc = _map_error(502, {"error": ["a", "b"]})
    assert isinstance(exc, APIError)
    assert exc.code == ""


@pytest.mark.parametrize(
    ("code", "message"),
    [
        ("api_error", "the account may have been offline"),
        ("suno_processing_unavailable", "Music processing is unavailable. Contact support with the trace ID."),
        (
            "suno_model_unavailable",
            "The selected model is unavailable for this operation. Contact support with the trace ID.",
        ),
        ("suno_processing_failed", "Music processing returned no audio. Contact support with the trace ID."),
    ],
)
def test_suno_processing_error_preserves_support_details(code, message):
    body = {"error": {"code": code, "message": message}, "trace_id": "test-trace"}

    exc = _map_error(500, body)

    assert isinstance(exc, APIError)
    assert exc.status_code == 500
    assert exc.code == code
    assert exc.message == message
    assert exc.trace_id == body["trace_id"]
    assert exc.body == body


def test_error_as_none_falls_back():
    exc = _map_error(400, {"error": None})
    assert isinstance(exc, APIError)
    assert exc.message == ""
