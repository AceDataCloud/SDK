"""Make model choices use SDK API snapshots, not a second short model table."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sync_from_platformbackend import sync_make_choices

ROOT = Path(__file__).resolve().parents[2]


class MakeModelChoicesTests(unittest.TestCase):
    def test_gpt_image_choices_match_the_image_endpoint(self):
        snapshot = ROOT / "scripts/specs/8f01fe72-8a3e-4872-8d8d-330cde179b3a.json"
        properties = json.loads(snapshot.read_text())["paths"][
            "/openai/images/generations"
        ]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]
        fields = json.loads(
            (ROOT / "examples/make/gpt-image/generate-parameters.json").read_text()
        )
        for field in fields:
            enum = properties.get(field["name"], {}).get("enum")
            if field["type"] == "select" and enum:
                self.assertEqual([item["value"] for item in field["options"]], enum)

    def test_refresh_adds_new_models_and_removes_retired_choices(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            app = root / "apps/image"
            app.mkdir(parents=True)
            (app / "generate-communication.json").write_text(
                json.dumps({"url": "/images"})
            )
            params = app / "generate-parameters.json"
            params.write_text(
                json.dumps(
                    [
                        {
                            "name": "model",
                            "type": "select",
                            "options": [
                                {"label": "Current", "value": "current"},
                                {"label": "Old", "value": "old"},
                            ],
                        }
                    ]
                )
            )
            manifest = root / "services.json"
            manifest.write_text(
                json.dumps(
                    {"images": {"endpoints": [{"id": "image-api", "path": "/images"}]}}
                )
            )
            (root / "image-api.json").write_text(
                json.dumps(
                    {
                        "paths": {
                            "/images": {
                                "post": {
                                    "requestBody": {
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "properties": {
                                                        "model": {
                                                            "enum": ["current", "new"]
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                )
            )
            self.assertEqual(
                sync_make_choices(manifest, root, root / "apps", ["images"]),
                [str(params)],
            )
            self.assertEqual(
                json.loads(params.read_text())[0]["options"],
                [
                    {"label": "Current", "value": "current"},
                    {"label": "new", "value": "new"},
                ],
            )
            self.assertEqual(
                sync_make_choices(manifest, root, root / "apps", ["images"]), []
            )
