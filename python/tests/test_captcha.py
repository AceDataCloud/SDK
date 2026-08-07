from unittest.mock import Mock

import pytest

from acedatacloud import AceDataCloud, AsyncAceDataCloud
from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle, task_status


def test_captcha_token_hcaptcha_body_and_sync_result():
    client = AceDataCloud(api_token="t")
    transport = Mock()
    transport.request.return_value = {"token": "solved"}
    client.captcha.token._transport = transport

    result = client.captcha.token.hcaptcha(
        website_key="site-key",
        website_url="https://example.com",
        rqdata="rq",
        proxy="http://proxy",
    )

    assert result == {"token": "solved"}
    transport.request.assert_called_once_with(
        "POST",
        "/captcha/token/hcaptcha",
        json={
            "website_key": "site-key",
            "website_url": "https://example.com",
            "rqdata": "rq",
            "proxy": "http://proxy",
            "async": False,
        },
    )


def test_captcha_async_handle_polls_with_task_id_body():
    client = AceDataCloud(api_token="t")
    transport = Mock()
    transport.request.side_effect = [{"task_id": "task-1", "status": "processing"}, {"status": "ready", "token": "ok"}]
    client.captcha.token._transport = transport

    handle = client.captcha.token.hcaptcha(
        website_key="site-key",
        website_url="https://example.com",
        async_=True,
    )
    assert isinstance(handle, TaskHandle)

    state = handle.get()

    assert state["token"] == "ok"
    assert transport.request.call_args.kwargs["json"] == {"task_id": "task-1"}
    assert handle.done


def test_captcha_recognition_hcaptcha_body():
    client = AceDataCloud(api_token="t")
    transport = Mock()
    transport.request.return_value = {"solution": {"label": "cat"}}
    client.captcha.recognition._transport = transport

    client.captcha.recognition.hcaptcha(queries=["image"], question="Click cats")

    assert transport.request.call_args.args[:2] == ("POST", "/captcha/recognition/hcaptcha")
    assert transport.request.call_args.kwargs["json"] == {
        "queries": ["image"],
        "question": "Click cats",
        "async": False,
    }


async def _async_request(*_args, **_kwargs):
    return {"task_id": "task-2"}


@pytest.mark.asyncio
async def test_async_captcha_returns_async_handle():
    client = AsyncAceDataCloud(api_token="t")
    client.captcha.token._transport = Mock(request=_async_request)

    handle = await client.captcha.token.hcaptcha(
        website_key="site-key",
        website_url="https://example.com",
        async_=True,
    )

    assert isinstance(handle, AsyncTaskHandle)


def test_ready_captcha_task_is_terminal_success():
    assert task_status({"status": "ready", "token": "ok"}) == "succeeded"
