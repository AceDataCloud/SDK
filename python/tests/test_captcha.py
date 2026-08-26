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
    captcha.recognition.image2text(image="base64-image", async_=False)
    captcha.recognition.recaptcha2(image="base64-grid", question="Pick cars")
    captcha.token.hcaptcha(
        website_key="site-key",
        website_url="https://accounts.hcaptcha.com/demo",
        rqdata="rq",
        proxy="1.2.3.4:8080",
        async_=True,
    )
    captcha.token.recaptcha2(
        website_key="rc2-site-key",
        website_url="https://www.google.com/recaptcha/api2/demo",
        proxy="5.6.7.8:9090",
    )
    captcha.token.recaptcha3(
        page_action="submit",
        website_key="rc3-site-key",
        website_url="https://www.google.com/recaptcha/api3/demo",
        async_=True,
    )
    captcha.token.turnstile(
        website_key="ts-site-key",
        website_url="https://challenges.cloudflare.com/turnstile-demo",
        action="managed",
        cdata="abc123",
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
            "/captcha/recognition/image2text",
            {"image": "base64-image", "async": False},
        ),
        (
            "POST",
            "/captcha/recognition/recaptcha2",
            {"image": "base64-grid", "question": "Pick cars"},
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
        (
            "POST",
            "/captcha/token/recaptcha2",
            {
                "website_key": "rc2-site-key",
                "website_url": "https://www.google.com/recaptcha/api2/demo",
                "proxy": "5.6.7.8:9090",
            },
        ),
        (
            "POST",
            "/captcha/token/recaptcha3",
            {
                "page_action": "submit",
                "website_key": "rc3-site-key",
                "website_url": "https://www.google.com/recaptcha/api3/demo",
                "async": True,
            },
        ),
        (
            "POST",
            "/captcha/token/turnstile",
            {
                "website_key": "ts-site-key",
                "website_url": "https://challenges.cloudflare.com/turnstile-demo",
                "action": "managed",
                "cdata": "abc123",
            },
        ),
        ("POST", "/captcha/tasks", {"task_id": "task-1"}),
    ]


@pytest.mark.asyncio
async def test_async_captcha_serialization() -> None:
    transport = AsyncTransport()
    captcha = AsyncCaptcha(transport)

    await captcha.recognition.hcaptcha(async_=False)
    await captcha.recognition.image2text(image="base64-image")
    await captcha.recognition.recaptcha2(image="base64-grid", question="Pick buses", async_=True)
    await captcha.token.hcaptcha(website_key="site-key", website_url="https://accounts.hcaptcha.com/demo")
    await captcha.token.recaptcha2(
        website_key="rc2-site-key",
        website_url="https://www.google.com/recaptcha/api2/demo",
    )
    await captcha.token.recaptcha3(
        page_action="verify",
        website_key="rc3-site-key",
        website_url="https://www.google.com/recaptcha/api3/demo",
    )
    await captcha.token.turnstile(
        website_key="ts-site-key",
        website_url="https://challenges.cloudflare.com/turnstile-demo",
        async_=False,
    )
    await captcha.tasks.retrieve(task_id="task-1")

    assert transport.calls == [
        ("POST", "/captcha/recognition/hcaptcha", {"async": False}),
        ("POST", "/captcha/recognition/image2text", {"image": "base64-image"}),
        (
            "POST",
            "/captcha/recognition/recaptcha2",
            {"image": "base64-grid", "question": "Pick buses", "async": True},
        ),
        (
            "POST",
            "/captcha/token/hcaptcha",
            {
                "website_key": "site-key",
                "website_url": "https://accounts.hcaptcha.com/demo",
            },
        ),
        (
            "POST",
            "/captcha/token/recaptcha2",
            {
                "website_key": "rc2-site-key",
                "website_url": "https://www.google.com/recaptcha/api2/demo",
            },
        ),
        (
            "POST",
            "/captcha/token/recaptcha3",
            {
                "page_action": "verify",
                "website_key": "rc3-site-key",
                "website_url": "https://www.google.com/recaptcha/api3/demo",
            },
        ),
        (
            "POST",
            "/captcha/token/turnstile",
            {
                "website_key": "ts-site-key",
                "website_url": "https://challenges.cloudflare.com/turnstile-demo",
                "async": False,
            },
        ),
        ("POST", "/captcha/tasks", {"task_id": "task-1"}),
    ]
