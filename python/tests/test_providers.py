"""The provider axis: one namespace per service, generated from the specs."""

from __future__ import annotations

import inspect
import typing
from unittest.mock import Mock

import pytest

from acedatacloud import AceDataCloud, AsyncAceDataCloud
from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle
from acedatacloud.resources.aichat import AiChat2Model, AiChatModel
from acedatacloud.resources.glm import GlmModel

# Every service the platform exposes as a non-private generation API.
GENERATED = (
    "flux",
    "seedream",
    "nano_banana",
    "seedance",
    "suno",
    "producer",
    "fish",
    "hailuo",
    "wan",
    "luma",
    "happyhorse",
    "maestro",
    "minimax",
    "digitalhuman",
    "dreamina",
    "localization",
)
HAND_WRITTEN = ("kling", "veo", "openai", "webextrator", "shorturl")


@pytest.fixture
def client():
    return AceDataCloud(api_token="test-token")


@pytest.mark.parametrize("name", GENERATED + HAND_WRITTEN)
def test_provider_namespace_exists(client, name):
    assert hasattr(client, name), f"client.{name} is missing"


@pytest.mark.parametrize("name", GENERATED + HAND_WRITTEN)
def test_async_client_has_the_same_namespaces(name):
    assert hasattr(AsyncAceDataCloud(api_token="test-token"), name)


def test_updated_chat_model_enums_include_docs_models():
    assert "gpt-5.6-luna" in typing.get_args(AiChatModel)
    assert "deepseek-v4-pro" in typing.get_args(AiChatModel)
    assert "claude-opus-4-6" in typing.get_args(AiChat2Model)
    assert "glm-5.3" in typing.get_args(GlmModel)


def test_aichat_v2_serializes_latest_parameters(client):
    transport = Mock()
    transport.request.return_value = {"id": "conversation-1"}
    client.aichat._transport = transport

    client.aichat.create_v2(
        model="claude-opus-4-6",
        action="chat",
        message={"role": "user", "content": "hi"},
        allowed_skills=["web_search"],
        allowed_mcp_servers=["docs"],
        model_group="claude",
        async_=True,
    )

    assert transport.request.call_args.args == ("POST", "/aichat2/conversations")
    assert transport.request.call_args.kwargs["json"] == {
        "model": "claude-opus-4-6",
        "action": "chat",
        "message": {"role": "user", "content": "hi"},
        "allowed_skills": ["web_search"],
        "allowed_mcp_servers": ["docs"],
        "model_group": "claude",
        "async": True,
    }


def test_openai_responses_serializes_latest_parameters(client):
    transport = Mock()
    transport.request.return_value = {"id": "resp-1"}
    client.openai.responses._transport = transport

    client.openai.responses.create(
        model="gpt-5.6-luna",
        input="hi",
        parallel_tool_calls=False,
        include=["file_search_call.results"],
        reasoning={"effort": "medium"},
        text={"format": {"type": "text"}},
        max_output_tokens=128,
        stream_options={"include_usage": True},
    )

    assert transport.request.call_args.args == ("POST", "/openai/responses")
    assert transport.request.call_args.kwargs["json"] == {
        "model": "gpt-5.6-luna",
        "input": "hi",
        "parallel_tool_calls": False,
        "include": ["file_search_call.results"],
        "reasoning": {"effort": "medium"},
        "text": {"format": {"type": "text"}},
        "max_output_tokens": 128,
        "stream_options": {"include_usage": True},
    }


def test_openai_models_list_endpoint(client):
    transport = Mock()
    transport.request.return_value = {"object": "list", "data": []}
    client.openai.models._transport = transport

    assert client.openai.models.list() == {"object": "list", "data": []}
    assert transport.request.call_args.args == ("GET", "/openai/models")


@pytest.mark.parametrize("name", GENERATED)
def test_sync_and_async_bind_different_classes(client, name):
    """A sync client holding an async provider would fail only at call time."""
    sync_class = type(getattr(client, name)).__name__
    async_class = type(getattr(AsyncAceDataCloud(api_token="t"), name)).__name__
    assert async_class == f"Async{sync_class}"


def test_generation_returns_a_task_handle(client):
    """Consistently a handle — never sometimes a dict, which is what the old
    modality methods did depending on the server's runtime response shape."""
    transport = Mock()
    transport.request.return_value = {"success": True, "task_id": "t-1"}
    client.flux._transport = transport

    result = client.flux.generate(action="generate", prompt="a cat", size="1024x1024")
    assert isinstance(result, TaskHandle)
    assert result.id == "t-1"


@pytest.mark.asyncio
async def test_async_generation_returns_an_async_handle():
    client = AsyncAceDataCloud(api_token="t")

    async def request(*_args, **_kwargs):
        return {"success": True, "task_id": "t-2"}

    client.flux._transport = Mock(request=request)
    assert isinstance(await client.flux.generate(action="generate", prompt="a cat", size="1024x1024"), AsyncTaskHandle)


def test_required_flux_size_is_sent(client):
    transport = Mock()
    transport.request.return_value = {"task_id": "t-1"}
    client.flux._transport = transport

    client.flux.generate(action="generate", prompt="a cat", size="1024x1024")
    body = transport.request.call_args.kwargs["json"]
    assert body["size"] == "1024x1024"


def test_caller_value_beats_the_spec_default(client):
    transport = Mock()
    transport.request.return_value = {"task_id": "t-1"}
    client.flux._transport = transport

    client.flux.generate(action="generate", prompt="a cat", size="512x512")
    assert transport.request.call_args.kwargs["json"]["size"] == "512x512"


def test_seedance_25_serializes_public_contract(client):
    transport = Mock()
    transport.request.return_value = {"task_id": "seedance-25"}
    client.seedance._transport = transport

    client.seedance.generate(
        model="doubao-seedance-2-5-260628",
        content=[{"type": "text", "text": "Extend the scene"}],
        duration=30,
        camerafixed=True,
        omni_reference_task_type="extend",
        output_format="mov",
        tools=[{"type": "web_search"}],
    )

    body = transport.request.call_args.kwargs["json"]
    assert body["model"] == "doubao-seedance-2-5-260628"
    assert body["omni_reference_task_type"] == "extend"
    assert body["output_format"] == "mov"
    assert body["tools"] == [{"type": "web_search"}]
    assert body["camerafixed"] is True
    assert "camera_fixed" not in body


def test_seedance_20_does_not_receive_25_defaults(client):
    transport = Mock()
    transport.request.return_value = {"task_id": "seedance-20"}
    client.seedance._transport = transport
    client.seedance.generate(
        model="doubao-seedance-2-0-260128",
        content=[{"type": "text", "text": "A scene"}],
    )
    assert "output_format" not in transport.request.call_args.kwargs["json"]


def test_seedream_omits_example_only_size(client):
    transport = Mock()
    transport.request.return_value = {
        "success": True,
        "task_id": "seedream-1",
        "data": [{"image_url": "https://cdn.example.com/seedream.png"}],
    }
    client.seedream._transport = transport

    handle = client.seedream.generate(model="doubao-seedream-5-0-260128", prompt="a cat")

    body = transport.request.call_args.kwargs["json"]
    assert "size" not in body
    assert handle.done
    assert handle.urls() == ["https://cdn.example.com/seedream.png"]


def test_seedream_sends_explicit_size(client):
    transport = Mock()
    transport.request.return_value = {"task_id": "seedream-1"}
    client.seedream._transport = transport

    client.seedream.generate(model="doubao-seedream-5-0-260128", prompt="a cat", size="4K")

    assert transport.request.call_args.kwargs["json"]["size"] == "4K"


def test_seedream_size_type_excludes_adaptive(client):
    hints = typing.get_type_hints(type(client.seedream).generate)
    size = hints["size"]
    literal = next((arg for arg in typing.get_args(size) if typing.get_origin(arg) is typing.Literal), None)
    assert literal is not None
    assert "adaptive" not in typing.get_args(literal)


def test_async_is_requested_by_default(client):
    """Otherwise a slow generation holds the HTTP connection open."""
    transport = Mock()
    transport.request.return_value = {"task_id": "t-1"}
    client.flux._transport = transport

    client.flux.generate(action="generate", prompt="a cat", size="1024x1024")
    assert transport.request.call_args.kwargs["json"]["async"] is True


def test_minimax_generate_builds_a_task_handle(client):
    transport = Mock()
    transport.request.return_value = {"task_id": "minimax-1"}
    client.minimax._transport = transport

    handle = client.minimax.generate(
        model="MiniMax-H3",
        content=[{"type": "text", "text": "A cat"}],
        resolution="2K",
        duration=5,
        ratio="16:9",
    )

    assert isinstance(handle, TaskHandle)
    assert handle.id == "minimax-1"
    assert transport.request.call_args.args == ("POST", "/minimax/videos")
    assert transport.request.call_args.kwargs["json"] == {
        "model": "MiniMax-H3",
        "content": [{"type": "text", "text": "A cat"}],
        "resolution": "2K",
        "duration": 5,
        "ratio": "16:9",
        "async": True,
    }


def test_model_enum_is_typed(client):
    """A wrong model name should be a type error, not a runtime 400."""
    hints = typing.get_type_hints(type(client.flux).generate)
    model = hints["model"]
    args = typing.get_args(model)
    literal = next((a for a in args if typing.get_origin(a) is typing.Literal), None)
    assert literal is not None, "model should be a Literal of the spec's enum"
    assert "flux-dev" in typing.get_args(literal)


def test_extra_parameters_pass_through(client):
    """A parameter added upstream must be reachable before the SDK is regenerated."""
    transport = Mock()
    transport.request.return_value = {"task_id": "t-1"}
    client.flux._transport = transport

    client.flux.generate(action="generate", prompt="a cat", size="1024x1024", brand_new_flag=True)
    assert transport.request.call_args.kwargs["json"]["brand_new_flag"] is True


@pytest.mark.parametrize("name", GENERATED)
def test_every_provider_has_a_callable_method(client, name):
    provider = getattr(client, name)
    methods = [m for m, _ in inspect.getmembers(provider, inspect.ismethod) if not m.startswith("_")]
    assert methods, f"client.{name} exposes no methods"


def test_suno_keeps_its_secondary_endpoints(client):
    """A service with many endpoints must not collapse to just `generate`."""
    for method in ("generate", "lyrics", "wav", "mp4"):
        assert hasattr(client.suno, method), f"suno.{method} is missing"


def test_handle_is_born_complete_when_the_server_answered_synchronously(client):
    """Some endpoints return the artifact inline. `.wait()` must not then poll
    for a task that already finished — which is what made the documented
    `task.wait()` raise AttributeError before."""
    transport = Mock()
    transport.request.return_value = {
        "success": True,
        "task_id": "t-1",
        "data": [{"image_url": "https://cdn.example.com/a.png"}],
    }
    client.flux._transport = transport

    handle = client.flux.generate(action="generate", prompt="a cat", size="1024x1024")
    assert handle.done
    assert handle.wait() is not None
    assert handle.urls() == ["https://cdn.example.com/a.png"]
    assert transport.request.call_count == 1, "wait() must not poll a finished task"


def test_success_false_with_an_artifact_is_a_failure():
    """A finished-but-unsuccessful response must not be delivered as a success.

    `success: false` alone is ambiguous — some services use it for a retryable
    hiccup mid-run — but paired with an artifact the job has clearly ended.
    """
    from acedatacloud._runtime.tasks import task_status

    state = {"response": {"success": False, "video_url": "https://cdn.example.com/x.mp4"}}
    assert task_status(state) == "failed"


def test_success_false_without_an_artifact_keeps_waiting():
    from acedatacloud._runtime.tasks import task_status

    assert task_status({"response": {"success": False, "error": "temporary"}}) == ""


def test_get_records_a_terminal_state(client):
    """A caller driving its own poll loop only ever calls get().

    Without recording here, urls() and result() stay empty after a task has
    plainly finished — the failure looks like "generation succeeded but produced
    nothing", which is worse than an error.
    """
    from unittest.mock import Mock

    transport = Mock()
    transport.request.return_value = {"task_id": "t-1"}
    client.flux._transport = transport
    handle = client.flux.generate(action="generate", prompt="a cat", size="1024x1024")
    assert not handle.done

    transport.request.return_value = {
        "response": {
            "success": True,
            "finished_at": 1785145121.0,
            "data": [{"image_url": "https://cdn.example.com/a.png"}],
        }
    }
    handle.get()

    assert handle.done
    assert handle.urls() == ["https://cdn.example.com/a.png"]
    assert handle.result() is not None


def test_get_leaves_a_running_task_alone(client):
    from unittest.mock import Mock

    transport = Mock()
    transport.request.return_value = {"task_id": "t-1"}
    client.flux._transport = transport
    handle = client.flux.generate(action="generate", prompt="a cat", size="1024x1024")

    transport.request.return_value = {"response": {"status": "processing"}}
    handle.get()

    assert not handle.done
    assert handle.urls() == []


def test_a_structured_error_is_terminal_even_without_finished_at():
    """hailuo answers an unavailable-model request with success:false plus an
    error object and no finished_at. Reading that as "still running" makes the
    caller poll until timeout instead of showing the upstream's own reason."""
    from acedatacloud._runtime.tasks import task_status

    state = {
        "response": {
            "success": False,
            "error": {"code": "api_error", "message": "no channel available for minimax-t2v"},
            "task_id": "x",
        },
        "finished_at": None,
    }
    assert task_status(state) == "failed"


def test_a_transient_string_error_still_keeps_waiting():
    """Some services set success:false mid-run with a bare string and carry on.
    Only a structured error — a dict with a code — is the upstream's last word."""
    from acedatacloud._runtime.tasks import task_status

    assert task_status({"response": {"success": False, "error": "temporary"}}) == ""
    assert task_status({"response": {"success": False, "error": None}}) == ""
