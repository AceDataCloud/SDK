"""Tests for AceDataCloud Python SDK."""

import base64
import json
from typing import get_args
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


@pytest.mark.parametrize(
    ("operation", "stream"),
    [(operation, stream) for operation in ("completions", "responses", "messages") for stream in (False, True)]
    + [("aichat", False)],
)
@respx.mock
def test_sol_fast_model_passthrough(client, operation, stream):
    from acedatacloud import AiChatModel

    assert "gpt-5.6-sol-fast" in get_args(AiChatModel)
    body = {"model": "gpt-5.6-sol-fast"}
    if operation == "responses":
        path = "/openai/responses"
        create = client.openai.responses.create
        body["input"] = "Hello"
    elif operation == "aichat":
        path = "/aichat/conversations"
        create = client.aichat.create
        body["question"] = "Hello"
    else:
        path = "/openai/chat/completions" if operation == "completions" else "/v1/messages"
        create = client.openai.chat.completions.create if operation == "completions" else client.chat.messages.create
        body["messages"] = [{"role": "user", "content": "Hello"}]
        if operation == "messages":
            body["max_tokens"] = 64
    if stream:
        body["stream"] = True
    route = respx.post(f"https://api.acedata.cloud{path}").mock(
        return_value=httpx.Response(200, text="", headers={"content-type": "text/event-stream"})
        if stream
        else httpx.Response(200, json={})
    )

    result = create(**body)
    if stream:
        assert list(result) == []

    assert route.call_count == 1
    assert json.loads(route.calls.last.request.content) == body


@pytest.mark.parametrize(
    ("operation", "stream"),
    [(operation, stream) for operation in ("completions", "responses", "messages") for stream in (False, True)]
    + [("aichat", False)],
)
@respx.mock
@pytest.mark.asyncio
async def test_async_sol_fast_model_passthrough(async_client, operation, stream):
    body = {"model": "gpt-5.6-sol-fast"}
    if operation == "responses":
        path = "/openai/responses"
        create = async_client.openai.responses.create
        body["input"] = "Hello"
    elif operation == "aichat":
        path = "/aichat/conversations"
        create = async_client.aichat.create
        body["question"] = "Hello"
    else:
        path = "/openai/chat/completions" if operation == "completions" else "/v1/messages"
        create = (
            async_client.openai.chat.completions.create
            if operation == "completions"
            else async_client.chat.messages.create
        )
        body["messages"] = [{"role": "user", "content": "Hello"}]
        if operation == "messages":
            body["max_tokens"] = 64
    if stream:
        body["stream"] = True
    route = respx.post(f"https://api.acedata.cloud{path}").mock(
        return_value=httpx.Response(200, text="", headers={"content-type": "text/event-stream"})
        if stream
        else httpx.Response(200, json={})
    )

    try:
        result = await create(**body)
        if stream:
            assert [chunk async for chunk in result] == []
    finally:
        await async_client.close()

    assert route.call_count == 1
    assert json.loads(route.calls.last.request.content) == body


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


@pytest.mark.parametrize(
    "model", ["gpt-image-2.5-flare:official", "gpt-image-2.5-sunburst:official", "nano-banana-2.1"]
)
@respx.mock
def test_openai_images_support_public_models(client, model):
    generation = respx.post("https://api.acedata.cloud/openai/images/generations").mock(
        return_value=httpx.Response(200, json={"data": []})
    )
    edit = respx.post("https://api.acedata.cloud/openai/images/edits").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    client.openai.images.generate(prompt="A cat", model=model)
    client.openai.images.edit(image="https://example.com/cat.png", prompt="Add a hat", model=model)

    assert generation.calls.last.request.content == (f'{{"prompt":"A cat","model":"{model}"}}'.encode())
    assert edit.calls.last.request.content == (
        f'{{"image":"https://example.com/cat.png","prompt":"Add a hat","model":"{model}"}}'.encode()
    )


@respx.mock
@pytest.mark.asyncio
async def test_async_openai_images_support_nano_banana_21(async_client):
    generation = respx.post("https://api.acedata.cloud/openai/images/generations").mock(
        return_value=httpx.Response(200, json={})
    )
    edit = respx.post("https://api.acedata.cloud/openai/images/edits").mock(return_value=httpx.Response(200, json={}))
    try:
        await async_client.openai.images.generate(prompt="A vase", model="nano-banana-2.1")
        await async_client.openai.images.edit(
            image="https://example.com/vase.png", prompt="Change the color", model="nano-banana-2.1"
        )
        assert json.loads(generation.calls.last.request.content) == {"prompt": "A vase", "model": "nano-banana-2.1"}
        assert json.loads(edit.calls.last.request.content) == {
            "image": "https://example.com/vase.png",
            "prompt": "Change the color",
            "model": "nano-banana-2.1",
        }
    finally:
        await async_client.close()


@pytest.mark.parametrize("model", ["text-embedding-3-small", "text-embedding-3-large"])
@respx.mock
def test_openai_embeddings(client, model):
    route = respx.post("https://api.acedata.cloud/openai/embeddings").mock(return_value=httpx.Response(200, json={}))
    body = {"model": model, "input": ["Hello!", "Goodbye!"], "encoding_format": "base64", "dimensions": 256}

    client.openai.embeddings.create(**body)

    assert json.loads(route.calls.last.request.content) == body


@pytest.mark.parametrize("model", ["text-embedding-3-small", "text-embedding-3-large"])
@respx.mock
@pytest.mark.asyncio
async def test_async_openai_embeddings(async_client, model):
    route = respx.post("https://api.acedata.cloud/openai/embeddings").mock(return_value=httpx.Response(200, json={}))
    body = {"model": model, "input": "Hello!"}
    try:
        await async_client.openai.embeddings.create(**body)
    finally:
        await async_client.close()

    assert json.loads(route.calls.last.request.content) == body


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


@respx.mock
@pytest.mark.parametrize("operation", ["create", "stream", "count_tokens"])
@pytest.mark.parametrize(
    "thinking",
    [
        {"type": "adaptive", "display": "updates"},
        {"type": "between_tools", "display": "future-display", "extension": {"enabled": True}},
        {"type": "enabled", "budget_tokens": 1},
    ],
)
def test_chat_configuration_passthrough(operation, thinking):
    path = "/v1/messages/count_tokens" if operation == "count_tokens" else "/v1/messages"
    route = respx.post(f"https://api.acedata.cloud{path}").mock(
        return_value=httpx.Response(200, json={})
        if operation != "stream"
        else httpx.Response(200, text="", headers={"content-type": "text/event-stream"})
    )
    body = {"model": "claude-sonnet-5-5", "messages": [], "thinking": thinking}
    if operation != "count_tokens":
        body.update(
            metadata={"user_id": "example-user-001"},
            output_config={"effort": "future-effort", "extension": True},
            temperature=0.7,
        )
    with AceDataCloud(
        api_token="test-token",
        base_url="https://api.acedata.cloud",
        max_retries=0,
        headers={"anthropic-beta": "thinking-display-updates-2026-08-18"},
    ) as client:
        if operation == "count_tokens":
            client.chat.messages.count_tokens(**body)
        elif operation == "stream":
            list(client.chat.messages.create(**body, stream=True))
        else:
            client.chat.messages.create(**body)

    expected = dict(body)
    if operation != "count_tokens":
        expected["max_tokens"] = 4096
    if operation == "stream":
        expected["stream"] = True
    assert json.loads(route.calls.last.request.content) == expected
    assert route.calls.last.request.headers["anthropic-beta"] == "thinking-display-updates-2026-08-18"


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize("operation", ["create", "stream", "count_tokens"])
async def test_async_chat_configuration_passthrough(operation):
    path = "/v1/messages/count_tokens" if operation == "count_tokens" else "/v1/messages"
    route = respx.post(f"https://api.acedata.cloud{path}").mock(
        return_value=httpx.Response(200, json={})
        if operation != "stream"
        else httpx.Response(200, text="", headers={"content-type": "text/event-stream"})
    )
    body = {
        "model": "claude-sonnet-5-5",
        "messages": [],
        "thinking": {"type": "between_tools", "display": "updates", "extension": True},
    }
    if operation != "count_tokens":
        body["metadata"] = {"user_id": "example-user-001"}
        body["output_config"] = {"effort": "future-effort", "extension": True}
    async with AsyncAceDataCloud(
        api_token="test-token",
        base_url="https://api.acedata.cloud",
        max_retries=0,
        headers={"anthropic-beta": "thinking-display-updates-2026-08-18"},
    ) as client:
        if operation == "count_tokens":
            await client.chat.messages.count_tokens(**body)
        elif operation == "stream":
            stream = await client.chat.messages.create(**body, stream=True)
            assert [chunk async for chunk in stream] == []
        else:
            await client.chat.messages.create(**body)

    expected = dict(body)
    if operation != "count_tokens":
        expected["max_tokens"] = 4096
    if operation == "stream":
        expected["stream"] = True
    assert json.loads(route.calls.last.request.content) == expected
    assert route.calls.last.request.headers["anthropic-beta"] == "thinking-display-updates-2026-08-18"


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


@respx.mock
def test_captcha_hcaptcha(client):
    respx.post("https://api.acedata.cloud/captcha/recognition/hcaptcha").mock(
        return_value=httpx.Response(200, json={"task_id": "captcha-1"})
    )
    respx.post("https://api.acedata.cloud/captcha/token/hcaptcha").mock(
        return_value=httpx.Response(200, json={"task_id": "captcha-2"})
    )
    respx.post("https://api.acedata.cloud/captcha/tasks").mock(
        return_value=httpx.Response(200, json={"task_id": "captcha-2", "status": "succeeded"})
    )

    recognition = client.captcha.recognition.hcaptcha(queries=["cat"], question="pick cat")
    token = client.captcha.token.hcaptcha(
        website_key="site-key",
        website_url="https://accounts.hcaptcha.com/demo",
    )
    task = client.captcha.tasks.retrieve(task_id="captcha-2")

    assert recognition["task_id"] == "captcha-1"
    assert token["task_id"] == "captcha-2"
    assert task["status"] == "succeeded"


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
