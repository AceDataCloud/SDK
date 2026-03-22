"""Management-plane resources (applications, credentials, models, config)."""

from __future__ import annotations

from typing import Any


class _Applications:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def list(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/api/v1/applications/", params=params, platform=True)

    def create(self, *, service_id: str, **kwargs: Any) -> dict[str, Any]:
        body = {"service_id": service_id, **kwargs}
        return self._transport.request("POST", "/api/v1/applications/", json=body, platform=True)

    def get(self, application_id: str) -> dict[str, Any]:
        return self._transport.request("GET", f"/api/v1/applications/{application_id}/", platform=True)


class _AsyncApplications:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/v1/applications/", params=params, platform=True)

    async def create(self, *, service_id: str, **kwargs: Any) -> dict[str, Any]:
        body = {"service_id": service_id, **kwargs}
        return await self._transport.request("POST", "/api/v1/applications/", json=body, platform=True)

    async def get(self, application_id: str) -> dict[str, Any]:
        return await self._transport.request("GET", f"/api/v1/applications/{application_id}/", platform=True)


class _Credentials:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def list(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/api/v1/credentials/", params=params, platform=True)

    def create(self, *, application_id: str, **kwargs: Any) -> dict[str, Any]:
        body = {"application_id": application_id, **kwargs}
        return self._transport.request("POST", "/api/v1/credentials/", json=body, platform=True)

    def rotate(self, credential_id: str) -> dict[str, Any]:
        return self._transport.request("POST", f"/api/v1/credentials/{credential_id}/rotate/", platform=True)

    def delete(self, credential_id: str) -> dict[str, Any]:
        return self._transport.request("DELETE", f"/api/v1/credentials/{credential_id}/", platform=True)


class _AsyncCredentials:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/v1/credentials/", params=params, platform=True)

    async def create(self, *, application_id: str, **kwargs: Any) -> dict[str, Any]:
        body = {"application_id": application_id, **kwargs}
        return await self._transport.request("POST", "/api/v1/credentials/", json=body, platform=True)

    async def rotate(self, credential_id: str) -> dict[str, Any]:
        return await self._transport.request("POST", f"/api/v1/credentials/{credential_id}/rotate/", platform=True)

    async def delete(self, credential_id: str) -> dict[str, Any]:
        return await self._transport.request("DELETE", f"/api/v1/credentials/{credential_id}/", platform=True)


class _Models:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def list(self, **params: Any) -> dict[str, Any]:
        return self._transport.request("GET", "/api/v1/models/", params=params, platform=True)


class _AsyncModels:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/v1/models/", params=params, platform=True)


class _Config:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def get(self) -> dict[str, Any]:
        return self._transport.request("GET", "/api/v1/config/", platform=True)


class _AsyncConfig:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    async def get(self) -> dict[str, Any]:
        return await self._transport.request("GET", "/api/v1/config/", platform=True)


class Platform:
    """Synchronous management-plane client."""

    def __init__(self, transport: Any) -> None:
        self.applications = _Applications(transport)
        self.credentials = _Credentials(transport)
        self.models = _Models(transport)
        self.config = _Config(transport)


class AsyncPlatform:
    """Async management-plane client."""

    def __init__(self, transport: Any) -> None:
        self.applications = _AsyncApplications(transport)
        self.credentials = _AsyncCredentials(transport)
        self.models = _AsyncModels(transport)
        self.config = _AsyncConfig(transport)
