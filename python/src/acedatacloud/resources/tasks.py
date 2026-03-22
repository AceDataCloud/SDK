"""Cross-service task retrieval and polling."""

from __future__ import annotations

from typing import Any

from acedatacloud._runtime.tasks import AsyncTaskHandle, TaskHandle

_SERVICE_TASK_ENDPOINTS = {
    "suno": "/suno/tasks",
    "nano-banana": "/nano-banana/tasks",
    "seedream": "/seedream/tasks",
    "seedance": "/seedance/tasks",
    "sora": "/sora/tasks",
    "midjourney": "/midjourney/tasks",
    "luma": "/luma/tasks",
    "veo": "/veo/tasks",
    "flux": "/flux/tasks",
}


class Tasks:
    """Synchronous task retrieval client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def get(
        self,
        task_id: str,
        *,
        service: str = "suno",
    ) -> dict[str, Any]:
        endpoint = _SERVICE_TASK_ENDPOINTS.get(service, f"/{service}/tasks")
        return self._transport.request(
            "POST",
            endpoint,
            json={"id": task_id, "action": "retrieve"},
        )

    def wait(
        self,
        task_id: str,
        *,
        service: str = "suno",
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any]:
        endpoint = _SERVICE_TASK_ENDPOINTS.get(service, f"/{service}/tasks")
        handle = TaskHandle(task_id, endpoint, self._transport)
        return handle.wait(poll_interval=poll_interval, max_wait=max_wait)


class AsyncTasks:
    """Async task retrieval client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def get(
        self,
        task_id: str,
        *,
        service: str = "suno",
    ) -> dict[str, Any]:
        endpoint = _SERVICE_TASK_ENDPOINTS.get(service, f"/{service}/tasks")
        return await self._transport.request(
            "POST",
            endpoint,
            json={"id": task_id, "action": "retrieve"},
        )

    async def wait(
        self,
        task_id: str,
        *,
        service: str = "suno",
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any]:
        endpoint = _SERVICE_TASK_ENDPOINTS.get(service, f"/{service}/tasks")
        handle = AsyncTaskHandle(task_id, endpoint, self._transport)
        return await handle.wait(poll_interval=poll_interval, max_wait=max_wait)
