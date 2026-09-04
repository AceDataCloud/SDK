#!/usr/bin/env python3
"""Generate the SDK's provider-axis classes from the platform's OpenAPI specs.

The SDK was kept in sync by hand (in practice, by an LLM agent reading Docs),
which is why Go drifted, why Midjourney was deleted rather than modeled, and why
`model` enums went stale. The specs already describe every parameter precisely;
this turns them into code so the three languages cannot disagree.

Usage:
    python scripts/generate_providers.py --manifest <services.json> --specs <dir>

The manifest is produced from `cost/service_api_mapping.json` — it says which
services and endpoints to expose. The specs are the localized OpenAPI documents
served by `/api/v1/apis/<id>?lang=en` (read over HTTP, never off disk: the
on-disk copies still carry raw `$t(...)` tokens).
"""

from __future__ import annotations

import argparse
import json
import keyword
import re
from pathlib import Path
from typing import Any

# Parameters the SDK owns rather than the caller.
CONTROL = {"async", "callback_url", "webhook_url"}

PY_TYPES = {"string": "str", "integer": "int", "number": "float", "boolean": "bool"}
TS_TYPES = {"string": "string", "integer": "number", "number": "number", "boolean": "boolean"}
GO_TYPES = {"string": "string", "integer": "int", "number": "float64", "boolean": "bool"}


def snake(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def camel(name: str) -> str:
    head, *rest = snake(name).split("_")
    return head + "".join(p.title() for p in rest)


def pascal(name: str) -> str:
    return "".join(p.title() for p in snake(name).split("_"))


def py_param(name: str) -> str:
    """`async` and friends are reserved; the SDK's convention is a trailing _."""
    return f"{name}_" if keyword.iskeyword(name) else name


def post_operation(spec: dict, path: str) -> dict:
    """Return the POST operation for ``path`` from a per-endpoint or service spec."""
    paths = spec.get("paths") or {}
    methods = paths.get(path) or {}
    op = methods.get("post") or methods.get("POST")
    if isinstance(op, dict):
        return op
    for _path, fallback_methods in paths.items():
        for method, fallback in (fallback_methods or {}).items():
            if method.lower() == "post" and isinstance(fallback, dict):
                return fallback
    return {}


def request_schema(op: dict) -> dict:
    content = (op.get("requestBody") or {}).get("content") or {}
    return (content.get("application/json") or {}).get("schema") or {}


def summary(op: dict) -> str:
    text = op.get("summary") or op.get("description") or ""
    if text and not text.startswith("$t("):
        return " ".join(text.split())[:200]
    return ""


def _array_items_are_objects(schema: dict[str, Any]) -> bool:
    items = schema.get("items") or {}
    if items.get("type") == "object":
        return True
    for union in ("oneOf", "anyOf"):
        variants = items.get(union)
        if isinstance(variants, list) and variants and all(
            isinstance(variant, dict) and variant.get("type") == "object" for variant in variants
        ):
            return True
    return False


class Param:
    def __init__(self, name: str, schema: dict, required: bool, *, location: str = "body") -> None:
        self.name = name
        self.schema = schema or {}
        self.required = required
        self.location = location
        self.type = self.schema.get("type")
        self.enum = [e for e in (self.schema.get("enum") or []) if isinstance(e, str)]
        self.description = " ".join(str(self.schema.get("description") or "").split())

    @property
    def is_control(self) -> bool:
        return self.name in CONTROL

    def default(self) -> Any:
        """Return a valid schema default, never an illustrative example."""
        enum = self.enum
        if "default" in self.schema and (not enum or self.schema["default"] in enum):
            return self.schema["default"]
        return None

    def py_type(self) -> str:
        if self.enum:
            return "Literal[" + ", ".join(json.dumps(e) for e in self.enum) + "]"
        if self.type == "array":
            item = (self.schema.get("items") or {}).get("type")
            if _array_items_are_objects(self.schema):
                return "list[dict[str, Any]]"
            return f"list[{PY_TYPES.get(item, 'Any')}]"
        if self.type == "object":
            return "dict[str, Any]"
        return PY_TYPES.get(self.type, "Any")

    def ts_type(self) -> str:
        if self.enum:
            return " | ".join(json.dumps(e) for e in self.enum)
        if self.type == "array":
            item = (self.schema.get("items") or {}).get("type")
            if _array_items_are_objects(self.schema):
                return "Array<Record<string, unknown>>"
            return f"{TS_TYPES.get(item, 'unknown')}[]"
        if self.type == "object":
            return "Record<string, unknown>"
        return TS_TYPES.get(self.type, "unknown")

    def go_type(self) -> str:
        if self.type == "array":
            item = (self.schema.get("items") or {}).get("type")
            if _array_items_are_objects(self.schema):
                return "[]map[string]any"
            return f"[]{GO_TYPES.get(item, 'any')}"
        if self.type == "object":
            return "map[string]any"
        return GO_TYPES.get(self.type, "any")


# The last path segment names the artifact ("/flux/images"), but a method reads
# better as a verb. Exactly one endpoint per service becomes `generate`; the
# others keep their own noun, which is what distinguishes them.
_PRIMARY = {"images", "videos", "audios", "tts"}

# Which artifact a service is really about. Producer exposes /producer/videos
# (render a finished track to video) alongside /producer/audios (write the
# music) — picking whichever came first in the spec listing made
# `producer.generate` mean "render a video", so calling it demanded an audio_id
# the caller had no way to have.
_MODALITY_PRIMARY = {
    "AI Image": "images",
    "AI Video": "videos",
    "AI Audio": "audios",
}


def _method_name(path: str) -> str:
    tail = snake(path.rsplit("/", 1)[-1])
    return "generate" if tail in _PRIMARY else (tail or "generate")


class Endpoint:
    def __init__(self, alias: str, path: str, spec: dict, *, pollable: bool = False) -> None:
        self.alias = alias
        self.path = path
        self.method = _method_name(path)
        op = post_operation(spec, path)
        schema = request_schema(op)
        required = set(schema.get("required") or [])
        props: dict[str, dict] = schema.get("properties") or {}
        self.summary = summary(op)
        params = [Param(n, s, n in required) for n, s in props.items()]
        for raw in op.get("parameters") or []:
            location = raw.get("in")
            if location not in {"path", "query"}:
                continue
            name = raw.get("name")
            if not isinstance(name, str) or not name:
                continue
            params.append(Param(name, raw.get("schema") or {}, bool(raw.get("required")), location=location))
        self.params = params
        self.pollable = "async" in props or pollable

    @property
    def callable_params(self) -> list[Param]:
        """Required first — a Python signature cannot put a defaulted arg before one."""
        usable = [p for p in self.params if not p.is_control]
        return sorted(usable, key=lambda p: not p.required)

    @property
    def body_params(self) -> list[Param]:
        return [p for p in self.callable_params if p.location == "body"]

    @property
    def path_params(self) -> list[Param]:
        return [p for p in self.params if p.location == "path"]

    @property
    def query_params(self) -> list[Param]:
        return [p for p in self.params if p.location == "query"]


class Service:
    def __init__(self, alias: str, meta: dict, specs: Path) -> None:
        self.alias = alias
        self.category = meta.get("category") or ""
        self.tasks_path = meta.get("tasks")
        self.endpoints: list[Endpoint] = []
        for ep in meta["endpoints"]:
            spec_file = specs / f"{ep['id']}.json"
            if not spec_file.exists():
                continue
            self.endpoints.append(
                Endpoint(
                    alias,
                    ep["path"],
                    json.loads(spec_file.read_text()),
                    pollable=bool(ep.get("pollable")),
                )
            )
        self._name_methods()

    def _name_methods(self) -> None:
        """Give exactly one endpoint the name `generate`, and make it the right one."""
        want = _MODALITY_PRIMARY.get(self.category)
        primary = None
        if want:
            primary = next(
                (e for e in self.endpoints if snake(e.path.rsplit("/", 1)[-1]) == want), None
            )
        if primary is None:
            primary = next((e for e in self.endpoints if e.method == "generate"), None)

        for ep in self.endpoints:
            if ep is primary:
                ep.method = "generate"
            elif ep.method == "generate":
                # Lost the claim; fall back to its own noun.
                ep.method = snake(ep.path.rsplit("/", 1)[-1]) or snake(ep.path.replace("/", "_"))

        seen: set[str] = set()
        for ep in self.endpoints:
            # Two endpoints under one service can still end in the same word.
            if ep.method in seen:
                ep.method = snake(ep.path.replace("/", "_"))
            seen.add(ep.method)

    @property
    def py_module(self) -> str:
        return snake(self.alias)

    @property
    def class_name(self) -> str:
        return pascal(self.alias)

    @property
    def attr(self) -> str:
        return snake(self.alias)


# Services whose hand-written class knows things the spec does not — Kling's
# cross-field validation ("4k mode requires kling-v3"), OpenAI's chat/embeddings
# surface, Veo's upsample/extend/reshoot/objects endpoints (absent from the
# generation manifest), the search and shortener helpers. Generating over them
# would trade real knowledge for a mechanical translation.
HAND_WRITTEN = {"kling", "openai", "serp", "shorturl", "webextrator", "veo"}


def load(manifest: Path, specs: Path) -> list[Service]:
    data = json.loads(manifest.read_text())
    services = [
        Service(a, m, specs) for a, m in sorted(data.items()) if a not in HAND_WRITTEN
    ]
    return [s for s in services if s.endpoints]
