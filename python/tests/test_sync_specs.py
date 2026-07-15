import httpx
import respx

from acedatacloud import AceDataCloud


@respx.mock
def test_video_generate_gemini_fields():
    def _handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/gemini/videos"
        assert request.content
        assert b'"image_urls":["https://example.com/1.png"]' in request.content
        assert b'"video_urls":["https://example.com/1.mp4"]' in request.content
        assert b'"aspect_ratio":"16:9"' in request.content
        assert b'"resolution":"1080p"' in request.content
        return httpx.Response(200, json={"task_id": "task-gemini"})

    respx.post("https://api.acedata.cloud/gemini/videos").mock(side_effect=_handler)

    client = AceDataCloud(api_token="test-token", max_retries=0)
    try:
        result = client.video.generate(
            prompt="hello",
            provider="gemini",
            image_urls=["https://example.com/1.png"],
            video_urls=["https://example.com/1.mp4"],
            aspect_ratio="16:9",
            resolution="1080p",
        )
    finally:
        client.close()

    assert hasattr(result, "wait")


@respx.mock
def test_tasks_get_uses_gemini_endpoint():
    respx.post("https://api.acedata.cloud/gemini/tasks").mock(
        return_value=httpx.Response(200, json={"id": "task-gemini"})
    )

    client = AceDataCloud(api_token="test-token", max_retries=0)
    try:
        result = client.tasks.get("task-gemini", service="gemini")
    finally:
        client.close()

    assert result["id"] == "task-gemini"


@respx.mock
def test_kling_generate_uses_image_list_and_legacy_alias():
    calls = []

    def _handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.content)
        return httpx.Response(200, json={"task_id": "task-kling"})

    respx.post("https://api.acedata.cloud/kling/videos").mock(side_effect=_handler)

    client = AceDataCloud(api_token="test-token", max_retries=0)
    try:
        client.kling.generate(action="image2video", image_list=[{"image_url": "https://example.com/a.png"}])
        client.kling.generate(action="image2video", video_list=[{"image_url": "https://example.com/b.png"}])
    finally:
        client.close()

    assert b'"image_list":[{"image_url":"https://example.com/a.png"}]' in calls[0]
    assert b'"image_list":[{"image_url":"https://example.com/b.png"}]' in calls[1]


@respx.mock
def test_kling_motion_supports_model_name_and_watermark_info():
    def _handler(request: httpx.Request) -> httpx.Response:
        assert b'"model_name":"kling-v3"' in request.content
        assert b'"watermark_info":true' in request.content
        return httpx.Response(200, json={"task_id": "task-motion"})

    respx.post("https://api.acedata.cloud/kling/motion").mock(side_effect=_handler)

    client = AceDataCloud(api_token="test-token", max_retries=0)
    try:
        result = client.kling.motion(
            mode="pro",
            image_url="https://example.com/source.png",
            video_url="https://example.com/driver.mp4",
            character_orientation="image",
            model_name="kling-v3",
            watermark_info=True,
        )
    finally:
        client.close()

    assert "wait" not in result
