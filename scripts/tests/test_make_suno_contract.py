"""Offline Make Suno contract regressions; does not run Make's IML engine."""

import json
import subprocess
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[2] / "examples/make/suno"

# Evaluate the expressions as documented JavaScript-like IML, with only the
# built-ins they use. Make's actual parser, lazy evaluation, and schema casting
# still need account-side acceptance. No network calls are made here.
EVALUATOR = r"""
const vm = require('node:vm');
let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  const { communication, body, taskId } = JSON.parse(input);
  const get = (value, path) => path.split('.').reduce((v, k) => v?.[k], value);
  const context = {
    body, parameters: { task_id: taskId }, temp: {}, emptyarray: [],
    get,
    ifempty: (v, fallback) => v === undefined || v === null || v === '' ? fallback : v,
    choose: (condition, yes, no) => condition ? yes : no,
    length: value => value?.length ?? 0,
    contains: (values, value) => values.includes(value),
    map: (values, key, filter, value) => (values ?? [])
      .filter(item => filter === undefined || get(item, filter) === value)
      .map(item => get(item, key)),
  };
  const evaluate = text => typeof text !== 'string' || !text.startsWith('{{')
    ? text : vm.runInNewContext(text.slice(2, -2).replace(/\bif\(/g, 'choose('), context);
  if (!evaluate(communication.response.valid.condition)) {
    process.stdout.write(JSON.stringify({ rejected: true })); return;
  }
  for (const [key, expression] of Object.entries(communication.response.temp))
    context.temp[key] = evaluate(expression);
  const output = Object.fromEntries(Object.entries(communication.response.output)
    .map(([key, expression]) => [key, evaluate(expression)]));
  process.stdout.write(JSON.stringify(output));
});
"""


class MakeSunoTests(unittest.TestCase):
    def read(self, filename):
        return json.loads((APP / filename).read_text())

    def evaluate(self, body, task_id="same-task"):
        result = subprocess.run(
            ["node", "-e", EVALUATOR],
            input=json.dumps(
                {
                    "communication": self.read("task-communication.json"),
                    "body": body,
                    "taskId": task_id,
                }
            ),
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_generate_submits_one_async_request_without_callback_or_fallback(self):
        request = self.read("generate-communication.json")
        self.assertEqual(request["url"], "/suno/audios")
        self.assertEqual(request["method"], "POST")
        self.assertIs(request["body"]["async"], True)
        self.assertEqual(request["body"]["action"], "generate")
        self.assertEqual(request["body"]["model"], "{{parameters.model}}")
        self.assertNotIn("callback_url", request["body"])
        self.assertNotIn("repeat", request)
        self.assertEqual(request["response"]["output"]["status"], "pending")
        self.assertIs(request["response"]["output"]["success"], False)

    def test_standalone_app_preserves_shared_credential_and_universal_contract(self):
        for filename in [
            "connection-parameters.json",
            "connection-communication.json",
            "universal-parameters.json",
            "universal-communication.json",
            "universal-interface.json",
        ]:
            with self.subTest(filename=filename):
                self.assertEqual(
                    self.read(filename), json.loads((APP.parent / filename).read_text())
                )
        manifest = self.read("makecomapp.json")
        self.assertEqual(manifest["origins"], [])
        self.assertEqual(
            set(manifest["components"]["module"]),
            {"generateMusic", "getTask", "makeAnApiCall"},
        )

    def test_output_interfaces_match_modules(self):
        for prefix in ["generate", "task", "universal"]:
            with self.subTest(prefix=prefix):
                self.assertEqual(
                    set(
                        self.read(prefix + "-communication.json")["response"]["output"]
                    ),
                    {field["name"] for field in self.read(prefix + "-interface.json")},
                )

    def test_lookup_uses_same_id_and_publishes_only_safe_fields(self):
        request = self.read("task-communication.json")
        self.assertEqual(request["url"], "/suno/tasks")
        self.assertEqual(
            request["body"], {"action": "retrieve", "id": "{{parameters.task_id}}"}
        )
        self.assertEqual(
            set(request["response"]["output"]),
            {"task_id", "status", "success", "trace_id", "audio_urls", "titles"},
        )
        self.assertEqual(
            self.read("base.json")["response"]["error"]["429"]["type"],
            "RuntimeError",
        )

    def test_pending_preview_and_partial_tracks_never_publish_media(self):
        for finished_at, states in [
            (None, ["succeeded"]),
            (1, ["succeeded", "running"]),
        ]:
            with self.subTest(finished_at=finished_at, states=states):
                output = self.evaluate(
                    {
                        "id": "same-task",
                        "finished_at": finished_at,
                        "response": {
                            "success": True,
                            "data": [
                                {
                                    "state": state,
                                    "audio_url": "https://example.com/a.mp3",
                                }
                                for state in states
                            ],
                        },
                    }
                )
                self.assertEqual(output["status"], "pending")
                self.assertIs(output["success"], False)
                self.assertEqual(output["audio_urls"], [])

    def test_completed_tracks_return_urls_without_internal_envelope(self):
        output = self.evaluate(
            {
                "id": "same-task",
                "finished_at": 1,
                "request": {"private_prompt": "do not expose"},
                "credential_id": "private",
                "response": {
                    "success": True,
                    "data": [
                        {
                            "state": "succeeded",
                            "audio_url": "https://example.com/final.mp3",
                            "title": "Track",
                            "supplier": "private",
                        }
                    ],
                },
            }
        )
        self.assertEqual(output["status"], "succeeded")
        self.assertIs(output["success"], True)
        self.assertEqual(output["audio_urls"], ["https://example.com/final.mp3"])
        self.assertNotIn("private", json.dumps(output))

    def test_failed_task_hides_previews(self):
        output = self.evaluate(
            {
                "id": "same-task",
                "finished_at": 1,
                "response": {
                    "success": False,
                    "error": {"message": "private detail"},
                    "data": [{"state": "failed", "audio_url": "https://example.com/p"}],
                },
            }
        )
        self.assertEqual(output["status"], "failed")
        self.assertEqual(output["audio_urls"], [])
        self.assertNotIn("private", json.dumps(output))

    def test_unknown_or_wrong_id_does_not_look_successful(self):
        self.assertEqual(self.evaluate({"id": "another-task"}), {"rejected": True})
        self.assertEqual(
            self.evaluate({"id": "same-task", "response": '{"success":true}'}),
            {"rejected": True},
        )
        output = self.evaluate({"id": "same-task", "response": None})
        self.assertEqual(output["status"], "pending")
        self.assertEqual(output["audio_urls"], [])


if __name__ == "__main__":
    unittest.main()
