"""Validate the Make local app with an offline checkout of Make's own schemas.

This checks source structure, not IML execution or installation in Make.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft7Validator
from referencing import Registry, Resource


def validate_app(app_root: Path, schema_root: Path) -> int:
    app_root = app_root.resolve()
    schema_root = schema_root.resolve()
    registry = Registry().with_resources(
        (path.as_uri(), Resource.from_contents(json.loads(path.read_text())))
        for path in schema_root.glob("syntaxes/**/schemas/*.json")
    )
    iml_schemas = schema_root / "syntaxes/imljson/schemas"
    manifest_schema = (
        schema_root / "syntaxes/local-development/schemas/makecomapp.schema.json"
    )
    checked = set()

    def check(filename: str, schema: Path) -> object:
        path = (app_root / filename).resolve()
        if not path.is_relative_to(app_root):
            raise ValueError(f"Code file is outside the app directory: {filename}")
        document = json.loads(path.read_text())
        Draft7Validator({"$ref": schema.as_uri()}, registry=registry).validate(document)
        checked.add(path)
        print(f"PASS {filename}")
        return document

    manifest = check("makecomapp.json", manifest_schema)
    general_schemas = {"base": "base", "common": "common", "groups": "groups"}
    for code_type, filename in manifest["generalCodeFiles"].items():
        if filename and code_type != "readme":
            check(filename, iml_schemas / f"{general_schemas[code_type]}.json")

    code_schemas = {
        "params": "parameters",
        "mappableParams": "parameters",
        "interface": "parameters",
        "communication": "api",
    }
    connections = manifest["components"]["connection"]
    for component_type, components in manifest["components"].items():
        for component_id, component in components.items():
            for key in ("connection", "altConnection"):
                if component.get(key) and component[key] not in connections:
                    raise ValueError(f"{component_id}: unknown {key}")
            for code_type, filename in component["codeFiles"].items():
                if not filename:
                    continue
                schema_name = code_schemas[code_type]
                if (
                    component_type == "connection"
                    and code_type == "communication"
                    and component.get("connectionType") == "oauth"
                ):
                    schema_name = "api-oauth"
                check(filename, iml_schemas / f"{schema_name}.json")

    unreferenced = set(app_root.glob("*.json")) - checked
    if unreferenced:
        raise ValueError(
            "JSON files absent from the manifest: "
            + ", ".join(sorted(path.name for path in unreferenced))
        )
    print(
        f"Validated {len(checked)} Make JSON files; runtime validation remains separate."
    )
    return len(checked)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema-root", type=Path, required=True)
    parser.add_argument(
        "--app-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "examples/make",
    )
    args = parser.parse_args()
    validate_app(args.app_root, args.schema_root)


if __name__ == "__main__":
    main()
