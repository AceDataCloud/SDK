"""Tests for the captcha resource."""

import httpx
import pytest
import respx

from acedatacloud import AceDataCloud, AsyncAceDataCloud


@pytest.fixture
def client():
    c = AceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0)
    yield c
    c.close()


@pytest.fixture
def async_client():
    return AsyncAceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0)


# ── recognition.hcaptcha ────────────────────────────────────────────────────


@respx.mock
def test_captcha_recognition_hcaptcha(client):
    mock_response = {"success": True, "token": "abc123"}
    respx.post("https://api.acedata.cloud/captcha/recognition/hcaptcha").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.captcha.recognition.hcaptcha(
        queries=["q1", "q2"],
        question="Select all cars",
    )
    assert result["token"] == "abc123"


@respx.mock
def test_captcha_recognition_hcaptcha_no_params(client):
    mock_response = {"success": True}
    route = respx.post("https://api.acedata.cloud/captcha/recognition/hcaptcha").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    client.captcha.recognition.hcaptcha()
    assert route.called


# ── recognition.image2text ──────────────────────────────────────────────────


@respx.mock
def test_captcha_recognition_image2text(client):
    mock_response = {"success": True, "text": "hello123"}
    respx.post("https://api.acedata.cloud/captcha/recognition/image2text").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.captcha.recognition.image2text(image="https://example.com/img.png")
    assert result["text"] == "hello123"


# ── recognition.recaptcha2 ──────────────────────────────────────────────────


@respx.mock
def test_captcha_recognition_recaptcha2(client):
    mock_response = {"success": True, "token": "rc2-tok"}
    respx.post("https://api.acedata.cloud/captcha/recognition/recaptcha2").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.captcha.recognition.recaptcha2(
        image="data:image/png;base64,...",
        question="Select all cars",
    )
    assert result["token"] == "rc2-tok"


# ── token.hcaptcha ──────────────────────────────────────────────────────────


@respx.mock
def test_captcha_token_hcaptcha(client):
    mock_response = {"success": True, "token": "hcap-tok"}
    route = respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.captcha.token.hcaptcha(
        website_key="key-123",
        website_url="https://example.com",
    )
    assert result["token"] == "hcap-tok"
    import json as _json
    body = _json.loads(route.calls.last.request.content)
    assert body["website_key"] == "key-123"
    assert body["website_url"] == "https://example.com"
    assert "proxy" not in body


@respx.mock
def test_captcha_token_hcaptcha_with_proxy(client):
    mock_response = {"success": True, "token": "hcap-tok"}
    route = respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    client.captcha.token.hcaptcha(
        website_key="key",
        website_url="https://example.com",
        proxy="http://proxy:8080",
    )
    import json as _json
    body = _json.loads(route.calls.last.request.content)
    assert body["proxy"] == "http://proxy:8080"


# ── token.recaptcha2 ────────────────────────────────────────────────────────


@respx.mock
def test_captcha_token_recaptcha2(client):
    mock_response = {"success": True, "token": "rc2-tok"}
    respx.post("https://api.acedata.cloud/captcha/token/recaptcha2").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.captcha.token.recaptcha2(
        website_key="rc2-key",
        website_url="https://example.com",
    )
    assert result["token"] == "rc2-tok"


# ── token.recaptcha3 ────────────────────────────────────────────────────────


@respx.mock
def test_captcha_token_recaptcha3(client):
    mock_response = {"success": True, "token": "rc3-tok"}
    route = respx.post("https://api.acedata.cloud/captcha/token/recaptcha3").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.captcha.token.recaptcha3(
        website_key="rc3-key",
        website_url="https://example.com",
        page_action="login",
    )
    assert result["token"] == "rc3-tok"
    import json as _json
    body = _json.loads(route.calls.last.request.content)
    assert body["page_action"] == "login"


# ── token.turnstile ─────────────────────────────────────────────────────────


@respx.mock
def test_captcha_token_turnstile(client):
    mock_response = {"success": True, "token": "ts-tok"}
    route = respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.captcha.token.turnstile(
        website_key="ts-key",
        website_url="https://example.com",
    )
    assert result["token"] == "ts-tok"
    import json as _json
    body = _json.loads(route.calls.last.request.content)
    assert "action" not in body
    assert "cdata" not in body


@respx.mock
def test_captcha_token_turnstile_with_optional_params(client):
    mock_response = {"success": True, "token": "ts-tok"}
    route = respx.post("https://api.acedata.cloud/captcha/token/turnstile").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    client.captcha.token.turnstile(
        website_key="ts-key",
        website_url="https://example.com",
        action="login",
        cdata="extra",
    )
    import json as _json
    body = _json.loads(route.calls.last.request.content)
    assert body["action"] == "login"
    assert body["cdata"] == "extra"


# ── async variants ───────────────────────────────────────────────────────────


@respx.mock
@pytest.mark.asyncio
async def test_async_captcha_token_hcaptcha(async_client):
    mock_response = {"success": True, "token": "async-tok"}
    respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await async_client.captcha.token.hcaptcha(
        website_key="k",
        website_url="https://example.com",
    )
    assert result["token"] == "async-tok"
    await async_client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_captcha_recognition_image2text(async_client):
    mock_response = {"success": True, "text": "async-text"}
    respx.post("https://api.acedata.cloud/captcha/recognition/image2text").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await async_client.captcha.recognition.image2text(image="data:image/png;base64,...")
    assert result["text"] == "async-text"
    await async_client.close()
