"""Host guides must keep source attribution and honest screenshot/task boundaries."""

import importlib.util
import json
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "render_onboarding", ROOT / "scripts/render_onboarding.py"
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class OnboardingTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(
            (ROOT / "docs/integration-onboarding/profiles/suno-cli.json").read_text()
        )

    def test_bilingual_guides_keep_host_specific_key_and_same_task_steps(self):
        for language in ("en", "zh-CN"):
            text = module.render(self.profile, language)
            self.assertIn("suno models", text)
            self.assertIn("ACEDATACLOUD_API_TOKEN", text)
            self.assertIn("suno wait <task-id>", text)
            self.assertIn(
                "not an official" if language == "en" else "不是模型方官方", text
            )
            self.assertIn("Dify tutorial", text)

    def test_source_is_existing_contract_and_all_four_tags_are_present(self):
        import re

        text = module.render(self.profile)
        urls = re.findall(r"https://platform\.acedata\.cloud[^)\s]+", text)
        self.assertEqual(len(urls), 2)
        for url in urls:
            query = parse_qs(urlsplit(url).query)
            self.assertEqual(
                set(query), {"utm_source", "utm_medium", "utm_campaign", "utm_content"}
            )
            self.assertEqual(query["utm_source"], ["opensource"])
            self.assertEqual(query["utm_medium"], ["referral"])
            self.assertEqual(query["utm_campaign"], ["evergreen"])

    def test_host_screenshot_cannot_be_inserted_without_source_and_date(self):
        self.profile["host_image_url"] = "https://example.com/screenshot.png"
        with self.assertRaises(ValueError):
            module.render(self.profile)

    def test_missing_host_credential_location_is_rejected(self):
        del self.profile["credential_location"]
        with self.assertRaises(ValueError):
            module.render(self.profile)

    def test_unapproved_source_cannot_invent_a_channel(self):
        self.profile["utm_source"] = "invented-campaign"
        with self.assertRaises(ValueError):
            module.render(self.profile)
