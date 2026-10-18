"""Offline regressions for the Make universal module's documented URL input."""

import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

APP = Path(__file__).resolve().parents[2] / "examples/make"


class MakeUniversalUrlTests(unittest.TestCase):
    def test_documented_model_path_stays_on_the_authenticated_endpoint(self):
        communication = json.loads((APP / "universal-communication.json").read_text())
        url = communication["url"].replace("{{parameters.url}}", "/v1/models")
        self.assertEqual(url, "https://api.acedata.cloud/v1/models")
        self.assertEqual(urlsplit(url).path, "/v1/models")

    def test_url_field_rejects_nonrelative_and_double_slash_inputs(self):
        parameters = json.loads((APP / "universal-parameters.json").read_text())
        field = next(
            parameter for parameter in parameters if parameter["name"] == "url"
        )
        pattern = field["validate"]["pattern"]
        for path in ("/v1/models", "/v1/models?limit=1"):
            with self.subTest(path=path):
                self.assertIsNotNone(re.search(pattern, path))
        for path in ("v1/models", "//v1/models", "https://example.com/v1/models", ""):
            with self.subTest(path=path):
                self.assertIsNone(re.search(pattern, path))


if __name__ == "__main__":
    unittest.main()
