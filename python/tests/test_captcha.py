from unittest.mock import AsyncMock, Mock

import pytest

from acedatacloud.resources.captcha import AsyncCaptcha, Captcha


def test_sync_captcha_recognition_and_token_routes():
    transport = Mock()
    transport.request.return_value = {"ok": True}
    captcha = Captcha(transport)

    captcha.recognition.hcaptcha(question="pick seahorse", queries="seahorse", async_=True)
    captcha.recognition.image2text(image="base64-image")
    captcha.recognition.recaptcha2(image="base64-image", question="pick bus")
    captcha.token.recaptcha3(
        website_key="site-key",
        website_url="https://example.com",
        page_action="submit",
        async_=True,
    )

    assert transport.request.call_args_list[0].args == ("POST", "/captcha/recognition/hcaptcha")
    assert transport.request.call_args_list[0].kwargs["json"] == {
        "question": "pick seahorse",
        "queries": "seahorse",
        "async": True,
    }
    assert transport.request.call_args_list[1].args == ("POST", "/captcha/recognition/image2text")
    assert transport.request.call_args_list[1].kwargs["json"] == {"image": "base64-image"}
    assert transport.request.call_args_list[2].args == ("POST", "/captcha/recognition/recaptcha2")
    assert transport.request.call_args_list[2].kwargs["json"] == {"image": "base64-image", "question": "pick bus"}
    assert transport.request.call_args_list[3].args == ("POST", "/captcha/token/recaptcha3")
    assert transport.request.call_args_list[3].kwargs["json"] == {
        "website_key": "site-key",
        "website_url": "https://example.com",
        "page_action": "submit",
        "async": True,
    }


@pytest.mark.asyncio
async def test_async_captcha_token_hcaptcha_route():
    transport = AsyncMock()
    transport.request.return_value = {"token": "abc"}
    captcha = AsyncCaptcha(transport)

    await captcha.token.hcaptcha(
        website_key="site-key",
        website_url="https://example.com",
    )

    transport.request.assert_awaited_once_with(
        "POST",
        "/captcha/token/hcaptcha",
        json={
            "website_key": "site-key",
            "website_url": "https://example.com",
        },
    )
