"""Tests for AceDataCloud Python SDK."""

import base64
import json
from unittest.mock import Mock

import httpx
import pytest
import respx

from acedatacloud import AceDataCloud, AsyncAceDataCloud
from acedatacloud._runtime.errors import (
    APIError,
    AuthenticationError,
    InsufficientBalanceError,
    RateLimitError,
    ValidationError,
)


@pytest.fixture
def client():
    c = AceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0)
    yield c
    c.close()


@pytest.fixture
def async_client():
    return AsyncAceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0)


@respx.mock
def test_default_api_base_uses_x402_host():
    route = respx.post("https://x402.acedata.cloud/openai/chat/completions").mock(
        return_value=httpx.Response(200, json={"choices": []})
    )
    client = AceDataCloud(api_token="test-token", max_retries=0)

    client.openai.chat.completions.create(model="test", messages=[])

    assert route.called
    client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_default_api_base_uses_x402_host():
    route = respx.post("https://x402.acedata.cloud/openai/chat/completions").mock(
        return_value=httpx.Response(200, json={"choices": []})
    )
    client = AsyncAceDataCloud(api_token="test-token", max_retries=0)

    await client.openai.chat.completions.create(model="test", messages=[])

    assert route.called
    await client.close()


@respx.mock
def test_x402_payment_retry_does_not_use_retry_budget():
    payment_handler = Mock(return_value={"headers": {"X-Payment": "signed-payment"}})
    route = respx.post("https://x402.acedata.cloud/openai/chat/completions").mock(
        side_effect=[
            httpx.Response(402, json={"accepts": [{"network": "base", "scheme": "exact"}]}),
            httpx.Response(200, json={"choices": []}),
        ]
    )
    client = AceDataCloud(payment_handler=payment_handler, max_retries=0)

    client.openai.chat.completions.create(model="test", messages=[])

    assert route.call_count == 2
    assert route.calls.last.request.headers["X-Payment"] == "signed-payment"
    client.close()


@respx.mock
def test_x402_payment_retry_parses_payment_required_header():
    required = {
        "x402Version": 2,
        "accepts": [{"network": "eip155:8453", "scheme": "exact", "amount": "1"}],
    }
    encoded = base64.b64encode(json.dumps(required).encode()).decode()
    payment_handler = Mock(return_value={"headers": {"PAYMENT-SIGNATURE": "signed-payment"}})
    route = respx.post("https://x402.acedata.cloud/openai/chat/completions").mock(
        side_effect=[
            httpx.Response(
                402,
                content=b"",
                headers={"PAYMENT-REQUIRED": encoded},
            ),
            httpx.Response(200, json={"choices": []}),
        ]
    )
    client = AceDataCloud(payment_handler=payment_handler, max_retries=0)

    client.openai.chat.completions.create(model="test", messages=[])

    assert payment_handler.call_args.args[0]["accepts"] == required["accepts"]
    assert route.calls.last.request.headers["PAYMENT-SIGNATURE"] == "signed-payment"
    client.close()


@respx.mock
def test_x402_paid_request_is_not_retried_with_same_signature():
    payment_handler = Mock(return_value={"headers": {"X-Payment": "signed-payment"}})
    route = respx.post("https://x402.acedata.cloud/openai/chat/completions").mock(
        side_effect=[
            httpx.Response(402, json={"accepts": [{"network": "base", "scheme": "exact"}]}),
            httpx.Response(500, json={"error": {"message": "upstream failed"}}),
            httpx.Response(200, json={"choices": []}),
        ]
    )
    client = AceDataCloud(payment_handler=payment_handler, max_retries=2)

    with pytest.raises(APIError, match="upstream failed"):
        client.openai.chat.completions.create(model="test", messages=[])

    assert route.call_count == 2
    client.close()


@pytest.mark.parametrize("body", [None, [], "error", {"accepts": "base"}, {"accepts": [None]}])
@respx.mock
def test_x402_rejects_malformed_payment_requirement_shapes(body):
    payment_handler = Mock(return_value={"headers": {"X-Payment": "signed-payment"}})
    respx.post("https://x402.acedata.cloud/openai/chat/completions").mock(return_value=httpx.Response(402, json=body))
    client = AceDataCloud(payment_handler=payment_handler, max_retries=0)

    with pytest.raises(APIError) as exc_info:
        client.openai.chat.completions.create(model="test", messages=[])

    assert exc_info.value.code == "invalid_402"
    payment_handler.assert_not_called()
    client.close()


@respx.mock
def test_x402_payment_handler_supports_streaming():
    payment_handler = Mock(return_value={"headers": {"X-Payment": "signed-payment"}})
    route = respx.post("https://x402.acedata.cloud/openai/chat/completions").mock(
        side_effect=[
            httpx.Response(402, json={"accepts": [{"network": "base", "scheme": "exact"}]}),
            httpx.Response(200, text='data: {"delta":"ok"}\n\ndata: [DONE]\n\n'),
        ]
    )
    client = AceDataCloud(payment_handler=payment_handler, max_retries=0)

    chunks = list(client.openai.chat.completions.create(model="test", messages=[], stream=True))

    assert chunks == [{"delta": "ok"}]
    assert route.call_count == 2
    assert route.calls.last.request.headers["X-Payment"] == "signed-payment"
    client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_x402_payment_handler_supports_streaming():
    async def payment_handler(_context):
        return {"headers": {"X-Payment": "signed-payment"}}

    route = respx.post("https://x402.acedata.cloud/openai/chat/completions").mock(
        side_effect=[
            httpx.Response(402, json={"accepts": [{"network": "base", "scheme": "exact"}]}),
            httpx.Response(200, text='data: {"delta":"ok"}\n\ndata: [DONE]\n\n'),
        ]
    )
    client = AsyncAceDataCloud(payment_handler=payment_handler, max_retries=0)

    stream = await client.openai.chat.completions.create(model="test", messages=[], stream=True)
    chunks = [chunk async for chunk in stream]

    assert chunks == [{"delta": "ok"}]
    assert route.call_count == 2
    assert route.calls.last.request.headers["X-Payment"] == "signed-payment"
    await client.close()


# ── OpenAI Chat Completions ──────────────────────────────────────────


@respx.mock
def test_openai_chat_completions(client):
    mock_response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "model": "claude-sonnet-4-20250514",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "Hello!"},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }
    respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.openai.chat.completions.create(
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": "Hi"}],
    )
    assert result["choices"][0]["message"]["content"] == "Hello!"
    assert result["usage"]["total_tokens"] == 15


# ── OpenAI Responses ─────────────────────────────────────────────────


@respx.mock
def test_openai_responses(client):
    mock_response = {
        "id": "resp-123",
        "output": [{"type": "message", "content": [{"type": "output_text", "text": "Hi there"}]}],
    }
    respx.post("https://api.acedata.cloud/openai/responses").mock(return_value=httpx.Response(200, json=mock_response))

    result = client.openai.responses.create(
        model="gpt-4o",
        input="Hello",
    )
    assert result["id"] == "resp-123"


# ── Chat Messages (Claude Native) ────────────────────────────────────


@respx.mock
def test_chat_messages(client):
    mock_response = {
        "id": "msg-123",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": "Hi!"}],
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }
    respx.post("https://api.acedata.cloud/v1/messages").mock(return_value=httpx.Response(200, json=mock_response))

    result = client.chat.messages.create(
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=1024,
    )
    assert result["content"][0]["text"] == "Hi!"


@respx.mock
def test_chat_count_tokens(client):
    mock_response = {"input_tokens": 42}
    respx.post("https://api.acedata.cloud/v1/messages/count_tokens").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.chat.messages.count_tokens(
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": "Hello"}],
    )
    assert result["input_tokens"] == 42


# ── Image Generation ──────────────────────────────────────────────────


@respx.mock
def test_images_generate(client):
    mock_response = {
        "success": True,
        "task_id": "task-abc",
        "data": [{"prompt": "A cat", "image_url": "https://cdn.acedata.cloud/cat.png"}],
    }
    respx.post("https://api.acedata.cloud/nano-banana/images").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = client.images.generate(prompt="A cat")
    assert result["data"][0]["image_url"] == "https://cdn.acedata.cloud/cat.png"


# ── Audio Generation ──────────────────────────────────────────────────


@respx.mock
def test_audio_generate(client):
    mock_response = {
        "success": True,
        "task_id": "task-audio",
        "data": [{"title": "My Song", "audio_url": "https://cdn.acedata.cloud/song.mp3"}],
    }
    respx.post("https://api.acedata.cloud/suno/audios").mock(return_value=httpx.Response(200, json=mock_response))

    result = client.audio.generate(prompt="A happy song")
    assert result["data"][0]["title"] == "My Song"


@respx.mock
def test_audio_generate_fish_uses_tts_endpoint(client):
    def _handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["text"] == "Hello fish"
        assert "prompt" not in payload
        assert request.headers["model"] == "speech-1"
        return httpx.Response(200, json={"success": True, "task_id": "task-fish"})

    respx.post("https://api.acedata.cloud/fish/tts").mock(side_effect=_handler)

    result = client.audio.generate(prompt="Hello fish", provider="fish", model="speech-1")
    assert hasattr(result, "wait")


@respx.mock
def test_audio_generate_fish_supports_explicit_tts_options(client):
    def _handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["reference_id"] == "voice-1"
        assert payload["sample_rate"] == 32000
        assert payload["mp3_bitrate"] == 128
        assert payload["chunk_length"] == 200
        assert payload["min_chunk_length"] == 100
        assert payload["top_p"] == 0.8
        assert payload["repetition_penalty"] == 1.1
        assert payload["max_new_tokens"] == 512
        assert payload["normalize"] is True
        return httpx.Response(200, json={"success": True, "task_id": "task-fish"})

    respx.post("https://api.acedata.cloud/fish/tts").mock(side_effect=_handler)

    result = client.audio.generate(
        prompt="Hello fish",
        provider="fish",
        reference_id="voice-1",
        sample_rate=32000,
        mp3_bitrate=128,
        chunk_length=200,
        min_chunk_length=100,
        top_p=0.8,
        repetition_penalty=1.1,
        max_new_tokens=512,
        normalize=True,
    )
    assert hasattr(result, "wait")


@respx.mock
def test_audio_fish_model_endpoints(client):
    respx.get("https://api.acedata.cloud/fish/model").mock(return_value=httpx.Response(200, json={"data": []}))
    respx.get("https://api.acedata.cloud/fish/model/model-1").mock(
        return_value=httpx.Response(200, json={"id": "model-1"})
    )

    model_list = client.audio.list_fish_models(page_size=10, page_number=2, self_only=True)
    model_detail = client.audio.get_fish_model("model-1")

    assert model_list["data"] == []
    assert model_detail["id"] == "model-1"


# ── Video Generation ──────────────────────────────────────────────────


@respx.mock
def test_video_generate(client):
    mock_response = {
        "success": True,
        "task_id": "task-video",
        "data": [{"video_url": "https://cdn.acedata.cloud/video.mp4"}],
    }
    respx.post("https://api.acedata.cloud/sora/videos").mock(return_value=httpx.Response(200, json=mock_response))

    result = client.video.generate(prompt="A sunset timelapse")
    assert result["data"][0]["video_url"] == "https://cdn.acedata.cloud/video.mp4"


# ── Search ────────────────────────────────────────────────────────────


@respx.mock
def test_search_google(client):
    mock_response = {
        "organic": [{"title": "Example", "link": "https://example.com", "snippet": "An example", "position": 1}],
    }
    respx.post("https://api.acedata.cloud/serp/google").mock(return_value=httpx.Response(200, json=mock_response))

    result = client.search.google(query="example")
    assert result["organic"][0]["title"] == "Example"


# ── Tasks ─────────────────────────────────────────────────────────────


@respx.mock
def test_tasks_get(client):
    mock_response = {
        "id": "task-abc",
        "response": {"status": "succeeded", "data": [{"image_url": "https://cdn.acedata.cloud/ok.png"}]},
    }
    respx.post("https://api.acedata.cloud/nano-banana/tasks").mock(return_value=httpx.Response(200, json=mock_response))

    result = client.tasks.get("task-abc", service="nano-banana")
    assert result["response"]["status"] == "succeeded"


# ── Platform Management ───────────────────────────────────────────────


@respx.mock
def test_platform_applications_list(client):
    mock = {"count": 1, "results": [{"id": "app-1", "service_id": "svc-1"}]}
    respx.get("https://platform.acedata.cloud/api/v1/applications/").mock(return_value=httpx.Response(200, json=mock))
    result = client.platform.applications.list()
    assert result["count"] == 1


@respx.mock
def test_platform_credentials_list(client):
    mock = {"count": 1, "results": [{"id": "cred-1", "token": "platform-abc"}]}
    respx.get("https://platform.acedata.cloud/api/v1/credentials/").mock(return_value=httpx.Response(200, json=mock))
    result = client.platform.credentials.list()
    assert result["results"][0]["token"] == "platform-abc"


@respx.mock
def test_platform_credentials_rotate(client):
    mock = {"id": "cred-1", "token": "platform-new"}
    respx.post("https://platform.acedata.cloud/api/v1/credentials/cred-1/rotate/").mock(
        return_value=httpx.Response(200, json=mock)
    )
    result = client.platform.credentials.rotate("cred-1")
    assert result["token"] == "platform-new"


@respx.mock
def test_platform_models_list(client):
    mock = {"data": [{"id": "claude-sonnet-4-20250514", "owned_by": "anthropic"}]}
    respx.get("https://platform.acedata.cloud/api/v1/models/").mock(return_value=httpx.Response(200, json=mock))
    result = client.platform.models.list()
    assert result["data"][0]["id"] == "claude-sonnet-4-20250514"


@respx.mock
def test_platform_config_get(client):
    mock = {"features": {"DISCOUNT_FOR_X402": 0.9}}
    respx.get("https://platform.acedata.cloud/api/v1/config/").mock(return_value=httpx.Response(200, json=mock))
    result = client.platform.config.get()
    assert result["features"]["DISCOUNT_FOR_X402"] == 0.9


# ── Error Mapping ─────────────────────────────────────────────────────


@respx.mock
def test_auth_error(client):
    respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
        return_value=httpx.Response(
            401, json={"error": {"code": "invalid_token", "message": "Bad token"}, "trace_id": "t-1"}
        )
    )
    with pytest.raises(AuthenticationError) as exc_info:
        client.openai.chat.completions.create(model="test", messages=[{"role": "user", "content": "hi"}])
    assert exc_info.value.status_code == 401
    assert exc_info.value.trace_id == "t-1"


@respx.mock
def test_balance_error(client):
    respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
        return_value=httpx.Response(
            403, json={"error": {"code": "used_up", "message": "Balance insufficient"}, "trace_id": "t-2"}
        )
    )
    with pytest.raises(InsufficientBalanceError):
        client.openai.chat.completions.create(model="test", messages=[{"role": "user", "content": "hi"}])


@respx.mock
def test_rate_limit_error(client):
    respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
        return_value=httpx.Response(
            429, json={"error": {"code": "too_many_requests", "message": "Slow down"}, "trace_id": "t-3"}
        )
    )
    with pytest.raises(RateLimitError):
        client.openai.chat.completions.create(model="test", messages=[{"role": "user", "content": "hi"}])


@respx.mock
def test_validation_error(client):
    respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
        return_value=httpx.Response(
            400, json={"error": {"code": "bad_request", "message": "Invalid model"}, "trace_id": "t-4"}
        )
    )
    with pytest.raises(ValidationError):
        client.openai.chat.completions.create(model="bad", messages=[{"role": "user", "content": "hi"}])


# ── Async Tests ───────────────────────────────────────────────────────


@respx.mock
@pytest.mark.asyncio
async def test_async_openai_completions(async_client):
    mock_response = {
        "id": "chatcmpl-async",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": "Async!"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 5, "completion_tokens": 3, "total_tokens": 8},
    }
    respx.post("https://api.acedata.cloud/openai/chat/completions").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await async_client.openai.chat.completions.create(
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": "Hi"}],
    )
    assert result["choices"][0]["message"]["content"] == "Async!"
    await async_client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_search(async_client):
    mock_response = {"organic": [{"title": "Async Example", "link": "https://example.com"}]}
    respx.post("https://api.acedata.cloud/serp/google").mock(return_value=httpx.Response(200, json=mock_response))

    result = await async_client.search.google(query="async test")
    assert result["organic"][0]["title"] == "Async Example"
    await async_client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_images(async_client):
    mock_response = {
        "success": True,
        "task_id": "task-async",
        "data": [{"image_url": "https://cdn.acedata.cloud/async.png"}],
    }
    respx.post("https://api.acedata.cloud/nano-banana/images").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    result = await async_client.images.generate(prompt="Test async")
    assert result["data"][0]["image_url"] == "https://cdn.acedata.cloud/async.png"
    await async_client.close()


# ── No Token Error ────────────────────────────────────────────────────


def test_no_token_error(monkeypatch):
    monkeypatch.delenv("ACEDATACLOUD_API_TOKEN", raising=False)
    with pytest.raises(AuthenticationError, match="api_token is required"):
        AceDataCloud()
