"""The three languages must expose the same provider surface.

Go drifting behind Python is what this whole generation pipeline exists to
prevent — the Go client was missing seven namespaces and pointed at a different
base URL for months without anyone noticing. These tests read the other two
languages' sources so a divergence fails here rather than in someone's
production traffic.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from acedatacloud import AceDataCloud

REPO = Path(__file__).resolve().parents[2]
TS_PROVIDERS = REPO / "typescript" / "src" / "resources" / "providers"
GO_ROOT = REPO / "go"


def _python_providers() -> set[str]:
    from acedatacloud.resources.providers import _attach

    source = (Path(_attach.__file__)).read_text()
    return set(re.findall(r"client\.(\w+) = ", source))


def _typescript_providers() -> set[str]:
    index = (TS_PROVIDERS / "index.ts").read_text()
    return set(re.findall(r"client\.(\w+) = new", index))


def _go_providers() -> set[str]:
    attach = (GO_ROOT / "providers_attach.go").read_text()
    return set(re.findall(r"return c\.providers\.(\w+)", attach))


def _normalise(names: set[str]) -> set[str]:
    """Each language spells a compound name its own way (nano_banana vs nanobanana)."""
    return {n.replace("_", "").lower() for n in names}


@pytest.mark.skipif(not TS_PROVIDERS.exists(), reason="typescript sources not present")
def test_python_and_typescript_expose_the_same_providers():
    assert _normalise(_python_providers()) == _normalise(_typescript_providers())


@pytest.mark.skipif(not GO_ROOT.exists(), reason="go sources not present")
def test_python_and_go_expose_the_same_providers():
    assert _normalise(_python_providers()) == _normalise(_go_providers())


@pytest.mark.skipif(not GO_ROOT.exists(), reason="go sources not present")
def test_base_urls_agree_across_languages():
    """Go silently pointed at api.acedata.cloud after the others moved to x402."""
    from acedatacloud import _client

    python_base = _client._API_BASE
    go_base = re.search(r'defaultAPIBase\s+= "([^"]+)"', (GO_ROOT / "options.go").read_text())
    assert go_base and go_base.group(1) == python_base

    ts_transport = (REPO / "typescript" / "src" / "runtime" / "transport.ts").read_text()
    assert python_base in ts_transport


def test_every_provider_is_reachable_from_the_client():
    client = AceDataCloud(api_token="test")
    for name in _python_providers():
        assert hasattr(client, name), f"generated {name} but the client does not expose it"
