"""Generator contract tests — Param.default() and request serialization."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from genlib.model import Param


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
