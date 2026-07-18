from unittest.mock import AsyncMock, Mock

import pytest

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle


def test_wait_accepts_success_data_without_status():
    pending = {"response": {"success": True, "task_id": "task-1"}}
    completed = {
        "finished_at": "2026-07-18T08:16:11Z",
        "response": {
            "success": True,
            "task_id": "task-1",
            "data": [{"image_url": "https://cdn.example/image.png"}],
        },
    }
    transport = Mock()
    transport.request.side_effect = [pending, completed]
    handle = TaskHandle("task-1", "/nano-banana/tasks", transport)

    result = handle.wait(poll_interval=0, max_wait=1)

    assert result == completed
    assert transport.request.call_count == 2


def test_is_completed_accepts_explicit_status():
    transport = Mock()
    transport.request.return_value = {"response": {"status": "succeeded"}}

    assert TaskHandle("task-1", "/tasks", transport).is_completed() is True


@pytest.mark.parametrize(
    "state",
    [
        {"response": {"success": True, "data": []}},
        {"response": {"success": True, "data": None}},
        {"response": {"success": False, "error": "temporary"}},
        {"response": {"success": False, "error": None}},
        {"response": None},
        {"finished_at": "2026-07-18T08:16:11Z", "response": {"status": "processing", "success": True}},
    ],
)
def test_is_completed_waits_without_terminal_status_or_finished_at(state):
    transport = Mock()
    transport.request.return_value = state

    assert TaskHandle("task-1", "/tasks", transport).is_completed() is False


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        ({"finished_at": "2026-07-18T08:16:11Z", "response": {"success": True, "data": None}}, True),
        ({"response": {"finished_at": "2026-07-18T08:16:11Z", "success": False}}, True),
        ({"finished_at": "2026-07-18T08:16:11Z", "response": {"success": None}}, False),
        ({"finished_at": "2026-07-18T08:16:11Z", "response": {"status": "succeeded", "success": False}}, True),
        ({"response": None, "status": "succeeded"}, True),
    ],
)
def test_is_completed_handles_statusless_terminal_shapes(state, expected):
    transport = Mock()
    transport.request.return_value = state

    assert TaskHandle("task-1", "/tasks", transport).is_completed() is expected


@pytest.mark.asyncio
async def test_async_wait_accepts_success_data_without_status():
    pending = {"response": {"success": True, "task_id": "task-1"}}
    completed = {
        "finished_at": "2026-07-18T08:16:11Z",
        "response": {
            "success": True,
            "data": [{"image_url": "https://cdn.example/image.png"}],
        },
    }
    transport = AsyncMock()
    transport.request.side_effect = [pending, completed]
    handle = AsyncTaskHandle("task-1", "/nano-banana/tasks", transport)

    result = await handle.wait(poll_interval=0, max_wait=1)

    assert result == completed
    assert transport.request.await_count == 2
