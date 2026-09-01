from acedatacloud.resources.gemini import Gemini


class Transport:
    def __init__(self):
        self.calls = []

    def request(self, method, path, *, json):
        self.calls.append((method, path, json))
        return {"task_id": "gemini-task"}


def test_gemini_video_uses_documented_defaults_and_task_endpoint():
    transport = Transport()
    task = Gemini(transport).generate_video(prompt="A cat", image_urls=["https://example.com/cat.png"])

    assert transport.calls == [
        (
            "POST",
            "/gemini/videos",
            {
                "prompt": "A cat",
                "model": "omni-flash",
                "aspect_ratio": "16:9",
                "resolution": "720p",
                "image_urls": ["https://example.com/cat.png"],
                "async": True,
            },
        )
    ]
    assert task.id == "gemini-task"
