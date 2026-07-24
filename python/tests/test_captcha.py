from unittest.mock import AsyncMock, Mock

import pytest

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle
from acedatacloud.resources.captcha import AsyncCaptcha, Captcha
from acedatacloud.resources.tasks import Tasks


def test_recaptcha3_token_uses_documented_endpoint():
    transport = Mock()
    transport.request.return_value = {"token": "captcha-token"}
    captcha = Captcha(transport)

    captcha.token.recaptcha3(
        page_action="examples/v3scores",
        website_key="site-key",
        website_url="https://example.com",
    )

    transport.request.assert_called_once_with(
        "POST",
        "/captcha/token/recaptcha3",
        json={
            "page_action": "examples/v3scores",
            "website_key": "site-key",
            "website_url": "https://example.com",
        },
    )


def test_async_captcha_returns_task_handle():
    transport = Mock()
    transport.request.return_value = {"task_id": "captcha-task"}
    captcha = Captcha(transport)

    result = captcha.recognition.image2text(image="data:image/png;base64,abc", async_=True)

    assert isinstance(result, TaskHandle)


def test_tasks_service_supports_captcha_endpoint():
    transport = Mock()
    transport.request.return_value = {"response": {"status": "succeeded", "data": {"text": "1234"}}}
    tasks = Tasks(transport)

    tasks.get("captcha-task", service="captcha")

    transport.request.assert_called_once_with(
        "POST",
        "/captcha/tasks",
        json={"id": "captcha-task", "action": "retrieve"},
    )


@pytest.mark.asyncio
async def test_async_recognition_image2text_returns_async_task_handle():
    transport = AsyncMock()
    transport.request.return_value = {"task_id": "captcha-task"}
    captcha = AsyncCaptcha(transport)

    result = await captcha.recognition.image2text(image="data:image/png;base64,abc", async_=True)

    assert isinstance(result, AsyncTaskHandle)
