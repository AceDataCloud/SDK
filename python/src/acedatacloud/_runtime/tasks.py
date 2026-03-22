"""Task polling abstractions for long-running operations."""

from __future__ import annotations

import time
import asyncio
from typing import Any


class TaskHandle:
    """Synchronous task handle for polling long-running operations."""

    def __init__(self, task_id: str, poll_endpoint: str, transport: Any) -> None:
        self.id = task_id
        self._poll_endpoint = poll_endpoint
        self._transport = transport
        self._result: dict[str, Any] | None = None

    def get(self) -> dict[str, Any]:
        """Fetch current task state."""
        return self._transport.request(
            "POST",
            self._poll_endpoint,
            json={"id": self.id, "action": "retrieve"},
        )

    def is_completed(self) -> bool:
        state = self.get()
        response = state.get("response", state)
        status = response.get("status", "")
        return status in ("succeeded", "failed")

    def wait(
        self,
        *,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any]:
        """Poll until the task completes or max_wait is reached."""
        start = time.monotonic()
        while time.monotonic() - start < max_wait:
            state = self.get()
            response = state.get("response", state)
            status = response.get("status", "")
            if status == "succeeded":
                self._result = state
                return state
            if status == "failed":
                self._result = state
                return state
            time.sleep(poll_interval)
        raise TimeoutError(f"Task {self.id} did not complete within {max_wait}s")

    def result(self) -> dict[str, Any] | None:
        return self._result


class AsyncTaskHandle:
    """Async task handle for polling long-running operations."""

    def __init__(self, task_id: str, poll_endpoint: str, transport: Any) -> None:
        self.id = task_id
        self._poll_endpoint = poll_endpoint
        self._transport = transport
        self._result: dict[str, Any] | None = None

    async def get(self) -> dict[str, Any]:
        return await self._transport.request(
            "POST",
            self._poll_endpoint,
            json={"id": self.id, "action": "retrieve"},
        )

    async def is_completed(self) -> bool:
        state = await self.get()
        response = state.get("response", state)
        status = response.get("status", "")
        return status in ("succeeded", "failed")

    async def wait(
        self,
        *,
        poll_interval: float = 3.0,
        max_wait: float = 600.0,
    ) -> dict[str, Any]:
        start = time.monotonic()
        while time.monotonic() - start < max_wait:
            state = await self.get()
            response = state.get("response", state)
            status = response.get("status", "")
            if status == "succeeded":
                self._result = state
                return state
            if status == "failed":
                self._result = state
                return state
            await asyncio.sleep(poll_interval)
        raise TimeoutError(f"Task {self.id} did not complete within {max_wait}s")

    async def result(self) -> dict[str, Any] | None:
        return self._result


class TimeoutError(Exception):
    """Task polling timeout."""
