"""Offline behavior tests for importing canonical SDK snapshots."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "sync_from_platformbackend.py"
SPEC = importlib.util.spec_from_file_location("sync_from_platformbackend", SCRIPT)
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)

A = "00000000-0000-4000-8000-000000000001"
B = "00000000-0000-4000-8000-000000000002"


class SnapshotSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.backend = self.root / "backend"
        self.snapshots = self.root / "snapshots"
        (self.backend / "openapi").mkdir(parents=True)
        self.snapshots.mkdir()
        self.manifest = self.root / "services.json"
        self.write(
            self.manifest,
            {
                "alpha": {"endpoints": [{"id": A, "path": "/alpha"}]},
                "beta": {"endpoints": [{"id": B, "path": "/beta"}]},
            },
        )
        for api_id, path in [(A, "/alpha"), (B, "/beta")]:
            spec = {
                "openapi": "3.0.0",
                "paths": {
                    path: {
                        "post": {
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "model": {
                                                    "type": "string",
                                                    "enum": ["old"],
                                                }
                                            },
                                        }
                                    }
                                },
                            }
                        }
                    }
                },
            }
            self.write(self.snapshots / f"{api_id}.json", spec)
            self.write(self.backend / "openapi" / f"{api_id}.json", spec)
        self.normalizer = patch.object(
            sync, "load_normalizer", return_value=copy.deepcopy
        )
        self.normalizer.start()
        self.addCleanup(self.normalizer.stop)

    def write(self, path, value):
        path.write_text(json.dumps(value), encoding="utf-8")

    def change(self, api_id):
        path = self.backend / "openapi" / f"{api_id}.json"
        spec = json.loads(path.read_text())
        spec["info"] = {"title": "Updated contract"}
        self.write(path, spec)
        return spec

    def run_sync(self, services=None):
        return sync.sync_specs(
            self.backend, self.manifest, self.snapshots, services or ["all"]
        )

    def test_only_selected_service_is_updated_and_rerun_is_noop(self):
        self.change(A)
        self.change(B)
        before = (self.snapshots / f"{B}.json").read_bytes()
        self.assertEqual(self.run_sync(["alpha"]), [A])
        self.assertEqual(self.run_sync(["alpha"]), [])
        self.assertEqual((self.snapshots / f"{B}.json").read_bytes(), before)

    def test_schema_enums_defaults_and_examples_are_preserved(self):
        spec = self.change(A)
        model = spec["paths"]["/alpha"]["post"]["requestBody"]["content"][
            "application/json"
        ]["schema"]["properties"]["model"]
        model.update(enum=["old", "new"], default="old", example="new")
        self.write(self.backend / "openapi" / f"{A}.json", spec)
        self.run_sync()
        self.assertEqual(json.loads((self.snapshots / f"{A}.json").read_text()), spec)

    def test_go_representation_hint_survives_snapshot_refresh(self):
        old = {
            "properties": {
                "flag": {
                    "type": "boolean",
                    "x-go-optional-pointer": True,
                    "enum": [True],
                }
            }
        }
        new = {"properties": {"flag": {"type": "boolean"}}}
        sync.preserve_client_hints(old, new)
        self.assertEqual(
            new["properties"]["flag"],
            {"type": "boolean", "x-go-optional-pointer": True},
        )

    def test_missing_source_does_not_partially_write_or_delete(self):
        before = (self.snapshots / f"{A}.json").read_bytes()
        self.change(A)
        (self.backend / "openapi" / f"{B}.json").unlink()
        with self.assertRaisesRegex(ValueError, "missing source"):
            self.run_sync()
        self.assertEqual((self.snapshots / f"{A}.json").read_bytes(), before)
        self.assertTrue((self.snapshots / f"{B}.json").exists())

    def test_http_method_change_requires_review(self):
        spec = self.change(A)
        spec["paths"]["/alpha"]["get"] = spec["paths"]["/alpha"].pop("post")
        self.write(self.backend / "openapi" / f"{A}.json", spec)
        with self.assertRaisesRegex(ValueError, "HTTP operations changed"):
            self.run_sync()

    def test_moved_path_requires_review(self):
        spec = self.change(A)
        spec["paths"]["/new"] = spec["paths"].pop("/alpha")
        self.write(self.backend / "openapi" / f"{A}.json", spec)
        with self.assertRaisesRegex(ValueError, "endpoint moved"):
            self.run_sync()

    def test_unmapped_service_does_not_expand_curated_manifest(self):
        self.change(A)
        self.assertEqual(self.run_sync(["new-provider"]), [])

    def test_manifest_cannot_escape_snapshot_directory(self):
        self.write(
            self.manifest,
            {"alpha": {"endpoints": [{"id": "../../escape", "path": "/alpha"}]}},
        )
        with self.assertRaisesRegex(ValueError, "Invalid API ID"):
            self.run_sync()


if __name__ == "__main__":
    unittest.main()
