"""Captcha resource contract tests."""

from typing import Any

import pytest

from acedatacloud.resources.captcha import AsyncCaptcha, Captcha


class SyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"ok": True}


class AsyncTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    async def request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((method, path, json))
        return {"ok": True}


def test_sync_captcha_serialization() -> None:
    transport = SyncTransport()
    captcha = Captcha(transport)

    captcha.recognition.hcaptcha(queries=["cat"], question="Pick cats", async_=True)
    captcha.token.hcaptcha(
        website_key="site-key",
        website_url="https://accounts.hcaptcha.com/demo",
        rqdata="rq",
        proxy="1.2.3.4:8080",
        async_=True,
    )
    captcha.tasks.retrieve(task_id="task-1")

    assert transport.calls == [
        (
            "POST",
            "/captcha/recognition/hcaptcha",
            {"queries": ["cat"], "question": "Pick cats", "async": True},
        ),
        (
            "POST",
            "/captcha/token/hcaptcha",
            {
                "website_key": "site-key",
                "website_url": "https://accounts.hcaptcha.com/demo",
                "rqdata": "rq",
                "proxy": "1.2.3.4:8080",
                "async": True,
            },
        ),
        ("POST", "/captcha/tasks", {"task_id": "task-1"}),
    ]


@pytest.mark.asyncio
async def test_async_captcha_serialization() -> None:
    transport = AsyncTransport()
    captcha = AsyncCaptcha(transport)

    await captcha.recognition.hcaptcha(async_=False)
    await captcha.token.hcaptcha(website_key="site-key", website_url="https://accounts.hcaptcha.com/demo")
    await captcha.tasks.retrieve(task_id="task-1")

    assert transport.calls == [
        ("POST", "/captcha/recognition/hcaptcha", {"async": False}),
        (
            "POST",
            "/captcha/token/hcaptcha",
            {
                "website_key": "site-key",
                "website_url": "https://accounts.hcaptcha.com/demo",
            },
        ),
        ("POST", "/captcha/tasks", {"task_id": "task-1"}),
    ]
