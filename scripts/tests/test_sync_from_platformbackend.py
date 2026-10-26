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

    def test_maestro_pinned_contract_has_one_language_and_no_quality_tier(self):
        path = SCRIPT.parent / "specs/ab512c42-324c-42e6-8d79-49a5042f3548.json"
        spec = json.loads(path.read_text(encoding="utf-8"))
        operation = spec["paths"]["/maestro/videos"]["post"]
        properties = operation["requestBody"]["content"]["application/json"]["schema"][
            "properties"
        ]
        self.assertEqual(properties["langs"]["minItems"], 1)
        self.assertEqual(properties["langs"]["maxItems"], 1)
        self.assertEqual(properties["langs"]["default"], ["zh-cn"])
        self.assertNotIn("quality", properties)
        self.assertIn("0.7 Credits", operation["description"])
        self.assertNotIn("Fish", properties["voice"]["description"])

    def test_kling_reference_video_billing_is_documented_not_a_request_field(self):
        path = SCRIPT.parent / "specs/29187cb2-1acb-43b8-baf5-3f3f709292eb.json"
        operation = json.loads(path.read_text())["paths"]["/kling/videos"]["post"]
        properties = operation["requestBody"]["content"]["application/json"]["schema"][
            "properties"
        ]
        description = properties["video_list"]["description"]
        self.assertIn("separate billing tier", description)
        self.assertIn("actual output duration rounded", description)
        self.assertIn("feature references use the requested duration", description)
        self.assertIn("usage.reference_video_seconds", description)
        self.assertIn("Image references alone do not trigger", description)
        self.assertNotIn("reference_video_seconds", properties)

    def test_retired_embedding_model_is_not_in_pinned_contract(self):
        path = SCRIPT.parent / "specs/a0840c8a-2b9a-4407-8aaf-0057f0e1f65c.json"
        spec = json.loads(path.read_text(encoding="utf-8"))
        model = spec["paths"]["/openai/embeddings"]["post"]["requestBody"]["content"][
            "application/json"
        ]["schema"]["properties"]["model"]
        self.assertEqual(
            model["enum"], ["text-embedding-3-small", "text-embedding-3-large"]
        )

    def test_sol_fast_is_in_pinned_chat_and_responses_contracts(self):
        for api_id, path in (
            ("c9969b66-effb-4753-b504-a82c4d16f83f", "/openai/chat/completions"),
            ("ed972a38-ecef-4fcb-af33-750de42d25dc", "/openai/responses"),
        ):
            with self.subTest(path=path):
                spec = json.loads(
                    (SCRIPT.parent / "specs" / f"{api_id}.json").read_text(
                        encoding="utf-8"
                    )
                )
                models = spec["paths"][path]["post"]["requestBody"]["content"][
                    "application/json"
                ]["schema"]["properties"]["model"]["enum"]
                self.assertEqual(models.count("gpt-5.6-sol-fast"), 1)
                self.assertIn("gpt-5.6-sol", models)

    def test_suno_availability_is_synchronous_and_only_confirms_true(self):
        path = SCRIPT.parent / "specs/fba10618-85c5-498e-904e-11db87b49954.json"
        spec = json.loads(path.read_text())
        operation = spec["paths"]["/suno/availability"]["post"]
        request = operation["requestBody"]["content"]["application/json"]["schema"]
        self.assertEqual(request["required"], ["audio_id"])
        self.assertEqual(set(request["properties"]), {"audio_id"})
        self.assertFalse(request["additionalProperties"])
        self.assertEqual(request["properties"]["audio_id"]["format"], "uuid")
        response = operation["responses"]["200"]["content"]["application/json"][
            "schema"
        ]
        available = response["properties"]["data"]["properties"]["available"]
        self.assertEqual(available["enum"], [True])
        self.assertIn("not guarantee", available["description"])
        self.assertIn("not interpret", operation["responses"]["503"]["description"])
        self.assertEqual(operation["security"], [{"bearerAuth": []}])
        manifest = json.loads((SCRIPT.parent / "services.json").read_text())
        endpoint = next(
            ep
            for ep in manifest["suno"]["endpoints"]
            if ep["path"] == "/suno/availability"
        )
        self.assertFalse(endpoint.get("pollable", False))

    def test_suno_negative_tags_has_no_fixed_character_limit(self):
        path = SCRIPT.parent / "specs/09a26295-5972-4392-9318-dcd9b218f90d.json"
        operation = json.loads(path.read_text())["paths"]["/suno/audios"]["post"]
        field = operation["requestBody"]["content"]["application/json"]["schema"][
            "properties"
        ]["negative_tags"]
        self.assertEqual(field["type"], "string")
        self.assertNotIn("maxLength", field)
        self.assertIn("custom", field["description"])
        self.assertIn("No fixed character limit", field["description"])
        self.assertIn("keep it concise", field["description"])

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

    def test_fish_creation_snapshot_uses_created_status_and_public_visibility(self):
        path = SCRIPT.parent / "specs" / "82dcabe9-b1a3-541f-80f1-decb183b920c.json"
        operation = json.loads(path.read_text())["paths"]["/fish/model"]["post"]
        self.assertNotIn("200", operation["responses"])
        schema = operation["responses"]["201"]["content"]["application/json"]["schema"]
        self.assertEqual(schema["example"]["visibility"], "public")
        visibility = operation["requestBody"]["content"]["application/json"]["schema"][
            "properties"
        ]["visibility"]
        self.assertIn("does not restrict access", visibility["description"])
        self.assertNotIn("default", visibility)

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
