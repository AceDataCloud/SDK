#!/usr/bin/env python3
"""Generate the SDK's provider-axis clients from the platform's OpenAPI specs.

    python scripts/generate_providers.py --manifest specs/services.json --specs specs/

The manifest lists which services and endpoints to expose (derived from the
platform's own service→api mapping). The specs are the localized OpenAPI
documents from `/api/v1/apis/<id>?lang=en`.

Hand-syncing this surface is what let Go drift, `model` enums go stale, and
Midjourney get deleted rather than modeled. Generating it means the three
languages cannot disagree.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from genlib import go_gen, python_gen, ts_gen  # noqa: E402
from genlib.model import load  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def _format_python(path: Path) -> None:
    import shutil
    import subprocess

    ruff = shutil.which("ruff")
    if not ruff:
        print("ruff not on PATH; generated Python files left unformatted", file=sys.stderr)
        return
    subprocess.run([ruff, "check", "--fix", "--quiet", str(path)], check=False)
    subprocess.run([ruff, "format", "--quiet", str(path)], check=False)


def _format_go(path: Path) -> None:
    import shutil
    import subprocess

    gofmt = shutil.which("gofmt")
    if not gofmt:
        print("gofmt not on PATH; generated Go files left unformatted", file=sys.stderr)
        return
    subprocess.run([gofmt, "-w", str(path)], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--specs", required=True, type=Path)
    parser.add_argument("--languages", default="python", help="comma-separated: python,typescript,go")
    args = parser.parse_args()

    services = load(args.manifest, args.specs)
    if not services:
        print("no services found in manifest", file=sys.stderr)
        return 1

    languages = {lang.strip() for lang in args.languages.split(",") if lang.strip()}
    total = 0

    if "python" in languages:
        root = ROOT / "python" / "src" / "acedatacloud"
        written = python_gen.write_all(services, root)
        written.append(python_gen.write_mixin(services, root))
        total += len(written)
        print(f"python: {len(written)} files + _client.py")

    # Generated source goes through the repo's own formatter so a human reading
    # a diff sees house style, not generator quirks.
    # CI checks formatting across the whole package, so format the package —
    # formatting only the generated subtree leaves the check red.
    _format_python(ROOT / "python")

    if "typescript" in languages:
        written = ts_gen.write_all(services, ROOT / "typescript" / "src")
        total += len(written)
        print(f"typescript: {len(written)} files")

    if "go" in languages:
        written = go_gen.write_all(services, ROOT / "go")
        for path in written:
            _format_go(path)
        total += len(written)
        print(f"go: {len(written)} files")

    endpoints = sum(len(s.endpoints) for s in services)
    print(f"generated {len(services)} services / {endpoints} endpoints ({total} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
