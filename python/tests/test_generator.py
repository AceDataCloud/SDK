"""Generator contract tests — Param.default() and request serialization."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from genlib.model import Endpoint, Param


def test_default_only_reads_schema_default():
    """example is illustrative, not a fallback — don't send it."""
    p = Param("size", {"type": "string", "example": "2K"}, required=False)
    assert p.default() is None


def test_default_returns_schema_default():
    p = Param("mode", {"type": "string", "default": "fast"}, required=False)
    assert p.default() == "fast"


def test_default_rejects_default_not_in_enum():
    """A default that contradicts the enum is invalid."""
    p = Param("size", {"type": "string", "enum": ["1K", "4K"], "default": "adaptive"}, required=False)
    assert p.default() is None


def test_default_accepts_default_in_enum():
    p = Param("size", {"type": "string", "enum": ["1K", "2K", "4K"], "default": "2K"}, required=False)
    assert p.default() == "2K"


def test_required_param_has_no_default():
    """Required means the caller must supply it."""
    p = Param("prompt", {"type": "string", "example": "a cat"}, required=True)
    assert p.default() is None


def test_endpoint_is_pollable_only_when_schema_or_manifest_declares_it():
    sync_spec = {
        "paths": {
            "/suno/persona": {
                "post": {
                    "requestBody": {"content": {"application/json": {"schema": {"type": "object", "properties": {}}}}}
                }
            }
        }
    }
    async_spec = {
        "paths": {
            "/suno/audios": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"type": "object", "properties": {"async": {"type": "boolean"}}}
                            }
                        }
                    }
                }
            }
        }
    }

    assert not Endpoint("suno", "/suno/persona", sync_spec).pollable
    assert Endpoint("suno", "/suno/audios", async_spec).pollable
    assert Endpoint("maestro", "/maestro/videos", sync_spec, pollable=True).pollable


def test_endpoint_models_get_query_and_path_parameters():
    spec = {
        "paths": {
            "/fish/model": {
                "get": {
                    "parameters": [
                        {"in": "query", "name": "page_size", "schema": {"type": "integer", "default": 10}},
                        {"in": "query", "name": "self", "schema": {"type": "boolean"}},
                        {"in": "header", "name": "accept", "schema": {"type": "string"}},
                    ]
                }
            },
            "/fish/model/{id}": {"get": {"parameters": [{"in": "path", "name": "id", "schema": {"type": "string"}}]}},
        }
    }

    listing = Endpoint("fish", "/fish/model", spec)
    detail = Endpoint("fish", "/fish/model/{id}", spec)

    assert listing.http_method == "get"
    assert [p.name for p in listing.query_params] == ["page_size", "self"]
    assert [p.name for p in listing.callable_params] == ["page_size", "self"]
    assert detail.method == "model_by_id"
    assert [p.name for p in detail.path_params] == ["id"]


def test_array_of_object_union_stays_structured_in_all_languages():
    schema = {
        "type": "array",
        "items": {
            "oneOf": [
                {"type": "object", "properties": {"text": {"type": "string"}}},
                {"type": "object", "properties": {"image_url": {"type": "string"}}},
            ]
        },
    }
    param = Param("content", schema, required=True)

    assert param.py_type() == "list[dict[str, Any]]"
    assert param.ts_type() == "Array<Record<string, unknown>>"
    assert param.go_type() == "[]map[string]any"


def test_schema_can_request_optional_pointer_in_go():
    param = Param("layer_decomposition", {"type": "boolean", "x-go-optional-pointer": True}, required=False)
    assert param.go_type() == "*bool"


def test_plain_optional_boolean_preserves_go_value_type():
    param = Param("watermark", {"type": "boolean"}, required=False)
    assert param.go_type() == "bool"


def test_pattern_string_becomes_precise_typescript_literals():
    param = Param("size", {"type": "string", "pattern": r"^(1K|1\.5K|auto|[0-9]+x[0-9]+)$"}, required=False)
    assert param.py_type() == 'Literal["1K", "1.5K", "auto"] | str'
    assert param.ts_type() == '"1K" | "1.5K" | "auto" | `${number}x${number}`'


def test_string_or_array_union_stays_typed():
    param = Param(
        "image",
        {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
        required=False,
    )
    assert param.py_type() == "str | list[str]"
    assert param.ts_type() == "string | string[]"


def test_optional_union_uses_nil_aware_go_any_type():
    param = Param(
        "image",
        {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
        required=False,
    )
    assert param.go_type() == "any"
