import json
import subprocess
import unittest
from pathlib import Path

from test_make_suno_contract import EVALUATOR

APP = Path(__file__).resolve().parents[2] / "examples/make/acemusic"


def read(name):
    return json.loads((APP / name).read_text())


class AceMusicMakeTests(unittest.TestCase):
    def test_manifest_loads_all_local_files_and_fixed_routes(self):
        manifest = read("makecomapp.json")
        self.assertEqual(manifest["origins"], [])
        modules = manifest["components"]["module"]
        self.assertEqual(len(modules), 9)
        for module in modules.values():
            files = module["codeFiles"]
            communication = read(files["communication"])
            self.assertIn(
                communication["url"],
                ["/acemusic/audios", "/acemusic/tasks", "/acemusic/lyrics"],
            )
            self.assertEqual(module["connection"], "apiKey")
            self.assertEqual(
                set(communication["response"]["output"]),
                {field["name"] for field in read(files["interface"])},
            )
            self.assertIsInstance(read(files["mappableParams"]), list)
        custom = read("custom-communication.json")["body"]
        self.assertTrue(custom["custom"])
        self.assertEqual(custom["lyric"], "{{parameters.lyric}}")
        self.assertEqual(
            read("mashup-communication.json")["body"]["mashup_audio_ids"],
            ["{{parameters.first_audio_id}}", "{{parameters.second_audio_id}}"],
        )

    def test_task_state_and_delivered_audio(self):
        for status, urls in [
            ("partial_failed", ["https://example.com/done.mp3"]),
            ("processing", []),
            ("failed", []),
        ]:
            response = {
                "id": "saved",
                "state": status,
                "response": {
                    "status": status,
                    "task_id": "saved",
                    "data": [
                        {
                            "state": "succeeded",
                            "audio_url": "https://example.com/done.mp3",
                        },
                        {
                            "state": "failed",
                            "audio_url": "https://example.com/rejected.mp3",
                        },
                    ],
                },
            }
            result = subprocess.run(
                ["node", "-e", EVALUATOR],
                check=True,
                capture_output=True,
                text=True,
                input=json.dumps(
                    {
                        "taskId": "saved",
                        "body": response,
                        "communication": read("retrieve-communication.json"),
                    }
                ),
            )
            output = json.loads(result.stdout)
            self.assertEqual(
                output["status"], "pending" if status == "processing" else status
            )
            self.assertFalse(output["success"])
            self.assertEqual(output["audio_urls"], urls)
