"""Service-specific Make media contracts; no generation or network calls."""

import json
import re
import unittest
from pathlib import Path

from make_iml_fixture import evaluate_task

ROOT = Path(__file__).resolve().parents[2]
APPS = ROOT / "examples/make"
CONTRACTS = json.loads(
    (Path(__file__).parent / "fixtures/make_media_contracts.json").read_text()
)
SERVICES = ["seedance", "happyhorse", "gpt-image", "nano-banana"]
FINAL_URL = "https://example.com/completed-media"


def read(service, filename):
    return json.loads((APPS / service / filename).read_text())


def validate_subset(value, schema):
    """Assert the pinned request subset without a new test dependency.

    The GPT prompt enum is a list of example prompts in the source OpenAPI,
    while the service guide accepts free text; the test uses its first example.
    """
    if "oneOf" in schema:
        matches = 0
        for branch in schema["oneOf"]:
            try:
                validate_subset(value, branch)
                matches += 1
            except AssertionError:
                pass
        assert matches == 1, (value, schema)
        return
    kind = schema.get("type")
    if kind == "object":
        assert isinstance(value, dict)
        assert all(key in value for key in schema.get("required", []))
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            assert not (set(value) - set(properties))
        for key, item in value.items():
            assert key in properties, key
            validate_subset(item, properties[key])
    elif kind == "array":
        assert isinstance(value, list)
        for item in value:
            validate_subset(item, schema["items"])
    elif kind == "string":
        assert isinstance(value, str)
        assert len(value) <= schema.get("maxLength", float("inf"))
        if "pattern" in schema:
            assert re.search(schema["pattern"], value)
    elif kind == "integer":
        assert type(value) is int
        assert schema.get("minimum", value) <= value <= schema.get("maximum", value)
    elif kind == "boolean":
        assert type(value) is bool
    if "enum" in schema:
        assert value in schema["enum"], (value, schema["enum"])


class MakeMediaTests(unittest.TestCase):
    def final_payload(self, service):
        if service == "seedance":
            data = {"status": "succeeded", "content": {"video_url": FINAL_URL}}
        elif service == "happyhorse":
            data = [{"state": "succeeded", "video_url": FINAL_URL}]
        elif service == "gpt-image":
            data = [{"url": FINAL_URL}]
        else:
            data = [{"image_url": FINAL_URL, "prompt": "illustration"}]
        return {
            "id": "same-task",
            "trace_id": "test-trace",
            "finished_at": 1,
            "response": {"success": True, "data": data},
        }

    def test_each_generation_request_matches_its_pinned_backend_contract(self):
        for service in SERVICES:
            with self.subTest(service=service):
                request = read(service, "generate-communication.json")
                contract = CONTRACTS[service]
                self.assertEqual(request["url"], contract["path"])
                self.assertEqual(request["method"], "POST")
                self.assertIs(request["body"]["async"], True)
                self.assertNotIn("callback_url", request["body"])
                self.assertNotIn("repeat", request)
                fields = read(service, "generate-parameters.json")
                values = {
                    field["name"]: (
                        field["options"][0]["value"]
                        if field["type"] == "select"
                        else field.get("default", "A cute baby sea otter")
                    )
                    for field in fields
                }

                def render(value, values=values):
                    if isinstance(value, dict):
                        return {key: render(item) for key, item in value.items()}
                    if isinstance(value, list):
                        return [render(item) for item in value]
                    if isinstance(value, str) and value.startswith("{{parameters."):
                        return values[value[13:-2]]
                    return value

                validate_subset(render(request["body"]), contract["schema"])
                model = next(field for field in fields if field["name"] == "model")
                supported = contract["schema"]["properties"]["model"]["enum"]
                self.assertTrue(
                    all(option["value"] in supported for option in model["options"])
                )

    def test_seedance_content_and_resolution_are_not_suno_or_happyhorse_fields(self):
        request = read("seedance", "generate-communication.json")
        self.assertEqual(
            request["body"]["content"],
            [{"type": "text", "text": "{{parameters.prompt}}"}],
        )
        self.assertNotIn("prompt", request["body"])
        self.assertNotIn("action", request["body"])
        resolution = next(
            field
            for field in read("seedance", "generate-parameters.json")
            if field["name"] == "resolution"
        )
        self.assertEqual(
            {option["value"] for option in resolution["options"]}, {"480p", "720p"}
        )

    def test_happyhorse_t2v_models_uppercase_resolution_and_duration(self):
        fields = read("happyhorse", "generate-parameters.json")
        by_name = {field["name"]: field for field in fields}
        self.assertTrue(
            all(
                option["value"].endswith("-t2v")
                for option in by_name["model"]["options"]
            )
        )
        self.assertEqual(
            {option["value"] for option in by_name["resolution"]["options"]},
            {"720P", "1080P"},
        )
        self.assertTrue(
            all(3 <= option["value"] <= 15 for option in by_name["duration"]["options"])
        )
        self.assertEqual(
            read("happyhorse", "generate-communication.json")["body"]["action"],
            "generate",
        )

    def test_image_apps_keep_different_counts_paths_and_url_fields(self):
        gpt = read("gpt-image", "generate-communication.json")
        nano = read("nano-banana", "generate-communication.json")
        self.assertEqual(gpt["body"]["n"], 1)
        self.assertEqual(gpt["body"]["response_format"], "url")
        self.assertNotIn("count", gpt["body"])
        self.assertEqual(nano["body"]["count"], 1)
        self.assertEqual(nano["body"]["action"], "generate")
        self.assertNotIn("n", nano["body"])
        self.assertEqual(
            read("gpt-image", "task-communication.json")["url"], "/openai/tasks"
        )
        self.assertEqual(
            read("nano-banana", "task-communication.json")["url"], "/nano-banana/tasks"
        )

    def test_all_queries_keep_same_id_and_hide_unfinished_preview(self):
        for service in SERVICES:
            with self.subTest(service=service):
                communication = read(service, "task-communication.json")
                self.assertEqual(
                    communication["body"],
                    {"action": "retrieve", "id": "{{parameters.task_id}}"},
                )
                pending = self.final_payload(service)
                pending["finished_at"] = None
                output = evaluate_task(communication, pending)
                self.assertEqual(output["status"], "pending")
                self.assertIs(output["success"], False)
                self.assertEqual(output.get("video_url", output.get("image_url")), "")

    def test_each_final_contract_exposes_only_completed_media_and_safe_fields(self):
        for service in SERVICES:
            with self.subTest(service=service):
                body = self.final_payload(service)
                body.update(
                    {"request": {"private": "hidden"}, "credential_id": "hidden"}
                )
                body["response"]["supplier"] = "hidden"
                communication = read(service, "task-communication.json")
                output = evaluate_task(communication, body)
                self.assertEqual(output["status"], "succeeded")
                self.assertIs(output["success"], True)
                self.assertEqual(
                    output.get("video_url", output.get("image_url")), FINAL_URL
                )
                self.assertNotIn("hidden", json.dumps(output))
                self.assertEqual(
                    set(output),
                    {
                        "task_id",
                        "status",
                        "success",
                        "trace_id",
                        "video_url"
                        if service in ["seedance", "happyhorse"]
                        else "image_url",
                    },
                )

    def test_failed_and_empty_envelopes_do_not_expose_media(self):
        for service in SERVICES:
            communication = read(service, "task-communication.json")
            for response in [
                None,
                {},
                {"success": False, "error": {"message": "hidden"}},
            ]:
                with self.subTest(service=service, response=response):
                    output = evaluate_task(
                        communication,
                        {"id": "same-task", "finished_at": 1, "response": response},
                    )
                    self.assertEqual(
                        output["status"], "failed" if response else "pending"
                    )
                    self.assertEqual(
                        output.get("video_url", output.get("image_url")), ""
                    )
                    self.assertNotIn("hidden", json.dumps(output))
            self.assertEqual(
                evaluate_task(communication, {"id": "wrong-task"}), {"rejected": True}
            )
            self.assertEqual(
                evaluate_task(
                    communication, {"id": "same-task", "response": '{"success":true}'}
                ),
                {"rejected": True},
            )

    def test_seedance_flat_url_and_running_state(self):
        body = self.final_payload("seedance")
        body["response"]["data"] = {"status": "succeeded", "video_url": FINAL_URL}
        communication = read("seedance", "task-communication.json")
        self.assertEqual(evaluate_task(communication, body)["video_url"], FINAL_URL)
        body["response"]["data"]["status"] = "running"
        self.assertEqual(evaluate_task(communication, body)["video_url"], "")

    def test_happyhorse_pending_track_and_image_partial_cardinality(self):
        body = self.final_payload("happyhorse")
        body["response"]["data"][0]["state"] = "pending"
        self.assertEqual(
            evaluate_task(read("happyhorse", "task-communication.json"), body)[
                "status"
            ],
            "pending",
        )
        for service in ["gpt-image", "nano-banana"]:
            body = self.final_payload(service)
            body["response"]["data"] *= 2
            self.assertEqual(
                evaluate_task(read(service, "task-communication.json"), body)[
                    "image_url"
                ],
                "",
            )

    def test_terminal_video_failure_states_override_preview_urls(self):
        for service in ["seedance", "happyhorse"]:
            for state in ["failed", "error", "cancelled", "canceled"]:
                with self.subTest(service=service, state=state):
                    body = self.final_payload(service)
                    if service == "seedance":
                        body["response"]["data"]["status"] = state
                    else:
                        body["response"]["data"][0]["state"] = state
                    output = evaluate_task(
                        read(service, "task-communication.json"), body
                    )
                    self.assertEqual(output["status"], "failed")
                    self.assertIs(output["success"], False)
                    self.assertEqual(output["video_url"], "")

    def test_standalone_interfaces_and_shared_credential_contract(self):
        for service in SERVICES:
            with self.subTest(service=service):
                manifest = read(service, "makecomapp.json")
                self.assertEqual(manifest["origins"], [])
                self.assertEqual(
                    set(manifest["components"]["module"]),
                    {"generateMedia", "getTask", "makeAnApiCall"},
                )
                for prefix in ["generate", "task", "universal"]:
                    self.assertEqual(
                        set(
                            read(service, prefix + "-communication.json")["response"][
                                "output"
                            ]
                        ),
                        {
                            field["name"]
                            for field in read(service, prefix + "-interface.json")
                        },
                    )
                for filename in [
                    "connection-parameters.json",
                    "connection-communication.json",
                    "universal-parameters.json",
                    "universal-communication.json",
                    "universal-interface.json",
                ]:
                    self.assertEqual(
                        read(service, filename),
                        json.loads((APPS / filename).read_text()),
                    )
                self.assertEqual(
                    read(service, "base.json")["response"]["error"]["429"]["type"],
                    "RuntimeError",
                )


if __name__ == "__main__":
    unittest.main()
