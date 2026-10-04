#!/usr/bin/env python3
"""Refresh curated SDK snapshots from a checked-out PlatformBackend commit.

The existing provider generator owns code generation. This adapter only maps
the SDK's existing API IDs to canonical specs and applies the backend's own
OpenAPI normalization. New endpoints and hand-written clients remain reviewed
changes; missing or moved operations must not silently remove SDK methods.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from collections.abc import Callable
from pathlib import Path

HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


def load_normalizer(backend: Path) -> Callable[[dict], dict]:
    path = backend / "scripts/ecosystem_contracts.py"
    spec = importlib.util.spec_from_file_location("ecosystem_contracts", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load canonical OpenAPI normalizer: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return lambda value: module.clean_openapi_spec(module.resolve_t_keys(value))


def operations(spec: dict) -> set[tuple[str, str]]:
    return {
        (path, method)
        for path, item in spec.get("paths", {}).items()
        for method in item
        if method in HTTP_METHODS
    }


def preserve_client_hints(current: object, incoming: object) -> None:
    """Keep representation hints owned by the SDK, never stale API constraints."""
    if isinstance(current, dict) and isinstance(incoming, dict):
        if (
            current.get("x-go-optional-pointer") is True
            and incoming.get("type") == "boolean"
        ):
            incoming["x-go-optional-pointer"] = True
        for key in current.keys() & incoming.keys():
            preserve_client_hints(current[key], incoming[key])


def sync_specs(
    backend: Path, manifest: Path, snapshots: Path, requested: list[str]
) -> list[str]:
    services = json.loads(manifest.read_text(encoding="utf-8"))
    selected = set(services) if requested == ["all"] else set(requested) & set(services)
    normalize = load_normalizer(backend)
    updates: dict[Path, dict] = {}
    for alias in sorted(selected):
        for endpoint in services[alias]["endpoints"]:
            api_id = endpoint["id"]
            if not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", api_id):
                raise ValueError(f"Invalid API ID in SDK manifest: {api_id}")
            source = backend / "openapi" / f"{api_id}.json"
            target = snapshots / f"{api_id}.json"
            if not source.is_file() or not target.is_file():
                raise ValueError(
                    f"{alias}/{api_id}: missing source or pinned snapshot; review the manifest"
                )
            current = json.loads(target.read_text(encoding="utf-8"))
            incoming = normalize(json.loads(source.read_text(encoding="utf-8")))
            preserve_client_hints(current, incoming)
            if endpoint["path"] == "/flux/videos":
                for schema in (
                    incoming.get("components", {}).get("schemas", {}).values()
                ):
                    for field in ("generate_audio", "draft"):
                        value = schema.get("properties", {}).get(field)
                        if isinstance(value, dict) and value.get("type") == "boolean":
                            value["x-go-optional-pointer"] = True
                            value.pop("default", None)
            if endpoint["path"] not in incoming.get("paths", {}):
                raise ValueError(
                    f"{alias}/{api_id}: endpoint moved; review the SDK method mapping"
                )
            if operations(current) != operations(incoming):
                raise ValueError(
                    f"{alias}/{api_id}: HTTP operations changed; review the SDK method mapping"
                )
            if incoming != current:
                updates[target] = incoming
    # Validate the full selection before writing any snapshot.
    for target, value in updates.items():
        target.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return sorted(path.stem for path in updates)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=Path("scripts/services.json"))
    parser.add_argument("--specs", type=Path, default=Path("scripts/specs"))
    parser.add_argument("--services", default="all")
    args = parser.parse_args()
    requested = [value.strip() for value in args.services.split(",") if value.strip()]
    if not requested or ("all" in requested and requested != ["all"]):
        parser.error(
            "--services must be 'all' or a nonempty comma-separated service list"
        )
    changed = sync_specs(args.backend_dir, args.manifest, args.specs, requested)
    print(f"Updated {len(changed)} pinned API snapshots.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
