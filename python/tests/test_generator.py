"""Generator contract tests — Param.default() and request serialization."""

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from genlib.model import Endpoint, Param
from genlib.python_gen import _aliases


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


def test_python_enum_aliases_are_scoped_by_method():
    long_model = Param("model", {"type": "string", "enum": [f"model-{i}" for i in range(8)]}, required=False)
    short_model = Param("model", {"type": "string", "enum": ["default", "remi-v1"]}, required=True)
    service = SimpleNamespace(
        class_name="Suno",
        endpoints=[
            SimpleNamespace(method="generate", params=[long_model]),
            SimpleNamespace(method="lyrics", params=[short_model]),
        ],
    )

    aliases, lines = _aliases(service)

    assert aliases == {"generate:model": "SunoModel"}
    assert "lyrics:model" not in aliases
    assert len(lines) == 1
