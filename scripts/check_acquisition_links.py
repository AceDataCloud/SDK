#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- canonical-acquisition -->"
TARGETS = {
    Path("README.md"): "sdk-catalog",
    Path("python/README.md"): "sdk-python",
    Path("typescript/README.md"): "sdk-typescript",
    Path("go/README.md"): "sdk-go",
}


def main() -> int:
    errors: list[str] = []
    for relative, campaign in TARGETS.items():
        text = (ROOT / relative).read_text()
        url = (
            "https://platform.acedata.cloud/"
            f"?utm_source=github&utm_medium=repo&utm_campaign={campaign}"
        )
        expected = f"{MARKER}\n[Get an API key]({url})"
        if text.count(MARKER) != 1:
            errors.append(f"{relative}: expected one acquisition marker")
        if text.count(url) != 1 or expected not in text:
            errors.append(f"{relative}: missing canonical {campaign} acquisition link")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"SDK acquisition links match {len(TARGETS)} canonical campaigns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
