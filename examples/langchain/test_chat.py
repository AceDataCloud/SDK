"""Protocol checks using the real LangChain adapter and an in-memory HTTP mock."""

import asyncio
import json

import httpx
import pytest
from chat import build_model, run_chat, run_stream, run_tools
from langchain_core.messages import HumanMessage
from openai import (
    AuthenticationError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)


def completion(message, *, model="gpt-4o-mini", finish_reason="stop", usage=None):
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 1,
        "model": model,
        "choices": [{"index": 0, "message": message, "finish_reason": finish_reason}],
        "usage": usage or {"prompt_tokens": 5, "completion_tokens": 3, "total_tokens": 8},
    }


def assert_request(request, *, model="gpt-4o-mini"):
    assert request.method == "POST"
    assert request.url.path == "/v1/chat/completions"
    assert request.headers["authorization"] == "Bearer test-token"
    body = json.loads(request.content)
    assert body["model"] == model
    return body


@pytest.fixture(autouse=True)
def credentials(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "test-token")
    monkeypatch.delenv("ACEDATACLOUD_BASE_URL", raising=False)
    monkeypatch.delenv("ACEDATACLOUD_MODEL", raising=False)
    monkeypatch.setenv("LANGSMITH_TRACING", "false")
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")


@pytest.mark.parametrize("model_name", ["gpt-4o-mini", "gpt-5.5"])
def test_sync_request_and_usage(capsys, monkeypatch, model_name):
    monkeypatch.setenv("ACEDATACLOUD_MODEL", model_name)
    requests = []

    def handle(request):
        requests.append(assert_request(request, model=model_name))
        return httpx.Response(
            200,
            json=completion({"role": "assistant", "content": "Hello"}, model=model_name),
        )

    client = httpx.Client(transport=httpx.MockTransport(handle))
    run_chat(build_model(http_client=client), "Say hello")
    out = capsys.readouterr()
    assert out.out.strip() == "Hello"
    assert '"total_tokens": 8' in out.err
    assert len(requests) == 1
    assert requests[0]["messages"] == [{"content": "Say hello", "role": "user"}]
    assert not requests[0].get("stream")


def test_stream_request_and_final_usage(capsys):
    requests = []

    def event(data):
        return f"data: {json.dumps(data)}\n\n"

    chunks = [
        {
            "id": "chatcmpl-test",
            "object": "chat.completion.chunk",
            "created": 1,
            "model": "gpt-4o-mini",
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": "Hi"},
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "chatcmpl-test",
            "object": "chat.completion.chunk",
            "created": 1,
            "model": "gpt-4o-mini",
            "choices": [{"index": 0, "delta": {"content": "!"}, "finish_reason": "stop"}],
        },
        {
            "id": "chatcmpl-test",
            "object": "chat.completion.chunk",
            "created": 1,
            "model": "gpt-4o-mini",
            "choices": [],
            "usage": {"prompt_tokens": 4, "completion_tokens": 2, "total_tokens": 6},
        },
    ]

    def handle(request):
        requests.append(assert_request(request))
        stream = "".join(event(chunk) for chunk in chunks) + "data: [DONE]\n\n"
        return httpx.Response(200, text=stream, headers={"content-type": "text/event-stream"})

    client = httpx.Client(transport=httpx.MockTransport(handle))
    run_stream(build_model(stream_usage=True, http_client=client), "Say hi")
    out = capsys.readouterr()
    assert out.out.strip() == "Hi!"
    assert '"total_tokens": 6' in out.err
    assert len(requests) == 1
    assert requests[0]["stream"] is True
    assert requests[0]["stream_options"] == {"include_usage": True}


def test_tool_call_round_trip(capsys):
    requests = []

    def handle(request):
        body = assert_request(request)
        requests.append(body)
        if len(requests) == 1:
            message = {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call_add",
                        "type": "function",
                        "function": {
                            "name": "add_numbers",
                            "arguments": '{"a":2,"b":3}',
                        },
                    }
                ],
            }
            return httpx.Response(200, json=completion(message, finish_reason="tool_calls"))
        return httpx.Response(200, json=completion({"role": "assistant", "content": "5"}))

    client = httpx.Client(transport=httpx.MockTransport(handle))
    run_tools(build_model(http_client=client))
    out = capsys.readouterr()
    assert out.out.strip() == "5"
    assert out.err.count("tokens:") == 2
    assert len(requests) == 2
    assert requests[0]["tool_choice"] == "required"
    assert requests[0]["tools"][0]["function"]["name"] == "add_numbers"
    assert requests[1]["messages"][-1] == {
        "content": "5",
        "role": "tool",
        "tool_call_id": "call_add",
    }


@pytest.mark.parametrize(
    "status,error_type",
    [
        (401, AuthenticationError),
        (403, PermissionDeniedError),
        (404, NotFoundError),
        (429, RateLimitError),
        (500, InternalServerError),
    ],
)
def test_http_error_does_not_retry(status, error_type):
    attempts = 0

    def handle(request):
        nonlocal attempts
        assert_request(request)
        attempts += 1
        return httpx.Response(status, json={"error": {"message": "test error", "type": "test_error"}})

    client = httpx.Client(transport=httpx.MockTransport(handle))
    with pytest.raises(error_type):
        build_model(http_client=client).invoke([HumanMessage(content="hello")])
    assert attempts == 1


def test_async_chat_completions():
    requests = []

    def handle(request):
        requests.append(assert_request(request))
        return httpx.Response(200, json=completion({"role": "assistant", "content": "Async OK"}))

    client = httpx.AsyncClient(transport=httpx.MockTransport(handle))
    model = build_model(http_async_client=client)
    reply = asyncio.run(model.ainvoke([HumanMessage(content="hello")]))
    assert reply.content == "Async OK"
    assert reply.usage_metadata["total_tokens"] == 8
    assert len(requests) == 1
