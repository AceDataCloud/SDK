"""ACE Music wire contract and no-duplicate-submit behavior."""

from unittest.mock import Mock

import httpx
import pytest
import respx

from acedatacloud import AceDataCloud
from acedatacloud._runtime.errors import TimeoutError
from acedatacloud._runtime.tasks import TaskHandle, task_status


def test_provider_generation_and_idempotency_header():
    client = AceDataCloud(api_token="token")
    transport = Mock()
    transport.request.return_value = {"task_id": "original"}
    client.acemusic._transport = transport
    task = client.acemusic.generate(prompt="folk", idempotency_key="stable-key")
    assert isinstance(task, TaskHandle) and task.id == "original"
    args = transport.request.call_args
    assert args.args == ("POST", "/acemusic/audios")
    assert args.kwargs["extra_headers"] == {"Idempotency-Key": "stable-key"}
    assert args.kwargs["json"] == {
        "action": "generate",
        "model": "acemusic-v1.1",
        "custom": False,
        "prompt": "folk",
        "async": True,
    }


def test_group_state_outranks_one_song_and_partial_is_terminal():
    pending = {
        "state": "processing",
        "response": {"data": [{"state": "succeeded", "audio_url": "https://cdn.acedata.cloud/one.mp3"}]},
    }
    assert task_status(pending) == ""
    pending["state"] = "partial_failed"
    assert task_status(pending) == "failed"
    pending["state"] = "succeeded"
    pending["response"]["data"].append({"state": "failed"})
    assert task_status(pending) == "succeeded"


@respx.mock
def test_timeout_never_resubmits_generation():
    route = respx.post("https://api.acedata.cloud/acemusic/audios").mock(side_effect=httpx.ReadTimeout("lost response"))
    client = AceDataCloud(api_token="token", base_url="https://api.acedata.cloud", max_retries=2)
    with pytest.raises(TimeoutError):
        client.acemusic.generate(prompt="folk")
    assert route.call_count == 1


def test_typed_task_filters_do_not_mix_pagination_modes():
    client = AceDataCloud(api_token="token")
    transport = Mock()
    transport.request.return_value = {"items": [], "count": 0}
    client.acemusic._transport = transport
    client.acemusic.tasks(action="list", type="audios", limit=10, offset=20, created_at_min=100.0, created_at_max=200.0)
    assert transport.request.call_args.kwargs["json"] == {
        "action": "list",
        "type": "audios",
        "limit": 10,
        "offset": 20,
        "created_at_min": 100.0,
        "created_at_max": 200.0,
    }
    client.acemusic.tasks(action="list", page=2, page_size=5)
    assert transport.request.call_args.kwargs["json"] == {"action": "list", "page": 2, "page_size": 5}
    client.acemusic.tasks(action="retrieve", id="original")
    assert transport.request.call_args.kwargs["json"] == {"action": "retrieve", "id": "original"}
