"""Unified protocol entrypoints preserve explicit models and HTTP contracts."""

import json

import httpx
import pytest
import respx

from acedatacloud import AceDataCloud, AsyncAceDataCloud

CASES = [
    ("completions", "/v1/chat/completions", "gemini-4-argon"),
    ("completions", "/v1/chat/completions", "gpt-4o-image"),
    ("responses", "/v1/responses", "gpt-5-pro"),
    ("messages", "/v1/messages", "claude-sonnet-5-5"),
    ("messages", "/v1/messages", "claude-opus-5-5"),
]


def options(protocol, model):
    if protocol == "responses":
        return {"model": model, "input": "Fixture", "max_output_tokens": 12}
    return {"model": model, "messages": [{"role": "user", "content": "Fixture"}], "max_tokens": 12}


def resource(client, protocol):
    return client.responses if protocol == "responses" else getattr(client.chat, protocol)


def response(stream, model):
    data = {"model": model, "type": "fixture"}
    if stream:
        return httpx.Response(
            200, text="data: " + json.dumps(data) + "\n\n", headers={"content-type": "text/event-stream"}
        )
    return httpx.Response(200, json=data)


def assert_request(route, payload, stream):
    assert len(route.calls) == 1
    request = route.calls[0].request
    assert request.headers["authorization"] == "Bearer test-token"
    assert "x-api-key" not in request.headers
    assert json.loads(request.content) == {**payload, **({"stream": True} if stream else {})}


@respx.mock
@pytest.mark.parametrize("protocol,path,model", CASES)
@pytest.mark.parametrize("stream", [False, True])
def test_unified_protocol(protocol, path, model, stream):
    route = respx.post("https://api.acedata.cloud" + path).mock(return_value=response(stream, model))
    with AceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0) as client:
        payload = options(protocol, model)
        result = resource(client, protocol).create(**payload, stream=stream)
        assert (list(result)[0] if stream else result) == {"model": model, "type": "fixture"}
    assert_request(route, payload, stream)


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize("protocol,path,model", CASES)
@pytest.mark.parametrize("stream", [False, True])
async def test_async_unified_protocol(protocol, path, model, stream):
    route = respx.post("https://api.acedata.cloud" + path).mock(return_value=response(stream, model))
    async with AsyncAceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0) as client:
        payload = options(protocol, model)
        result = await resource(client, protocol).create(**payload, stream=stream)
        assert ([chunk async for chunk in result][0] if stream else result) == {"model": model, "type": "fixture"}
    assert_request(route, payload, stream)


@respx.mock
@pytest.mark.parametrize(
    "protocol,path", [("completions", "/openai/chat/completions"), ("responses", "/openai/responses")]
)
def test_existing_openai_entrypoints_keep_their_paths(protocol, path):
    route = respx.post("https://api.acedata.cloud" + path).respond(200, json={})
    with AceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0) as client:
        target = client.openai.responses if protocol == "responses" else client.openai.chat.completions
        target.create(**options(protocol, "gpt-4.1"))
    assert_request(route, options(protocol, "gpt-4.1"), False)
