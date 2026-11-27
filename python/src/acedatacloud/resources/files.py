"""File upload resources."""

from __future__ import annotations

import os
from typing import Any


class Files:
    """Synchronous file upload client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def upload(
        self,
        file: str | bytes,
        *,
        filename: str | None = None,
    ) -> dict[str, Any]:
        if isinstance(file, str):
            path = file
            fname = filename or os.path.basename(path)
            with open(path, "rb") as f:
                data = f.read()
        else:
            data = file
            fname = filename or "upload"

        return self._transport.upload("/api/v1/files/", data, fname)


class AsyncFiles:
    """Async file upload client."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def upload(
        self,
        file: str | bytes,
        *,
        filename: str | None = None,
    ) -> dict[str, Any]:
        if isinstance(file, str):
            path = file
            fname = filename or os.path.basename(path)
            with open(path, "rb") as f:
                data = f.read()
        else:
            data = file
            fname = filename or "upload"

        return await self._transport.upload("/api/v1/files/", data, fname)
