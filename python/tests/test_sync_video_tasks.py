import httpx
import respx

from acedatacloud import AceDataCloud


@respx.mock
def test_video_generate_gemini():
    client = AceDataCloud(api_token="test-token", max_retries=0)
    try:
        respx.post("https://api.acedata.cloud/gemini/videos").mock(
            return_value=httpx.Response(200, json={"success": True, "task_id": "task-gemini"})
        )

        result = client.video.generate(
            prompt="A waterfall",
            provider="gemini",
            model="omni-flash",
            image_urls=["https://example.com/1.png"],
            aspect_ratio="16:9",
        )

        assert hasattr(result, "wait")
    finally:
        client.close()


@respx.mock
def test_tasks_get_gemini():
    client = AceDataCloud(api_token="test-token", max_retries=0)
    try:
        respx.post("https://api.acedata.cloud/gemini/tasks").mock(
            return_value=httpx.Response(200, json={"id": "task-gemini"})
        )

        result = client.tasks.get("task-gemini", service="gemini")

        assert result["id"] == "task-gemini"
    finally:
        client.close()
