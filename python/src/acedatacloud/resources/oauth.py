"""OAuth 2.0 client helpers for "Sign in with Ace Data Cloud"."""

from __future__ import annotations

from typing import Any

import httpx

_AUTH_BASE = "https://auth.acedata.cloud"


class OAuth:
    """Synchronous OAuth 2.0 helper for "Sign in with Ace Data Cloud"."""

    def __init__(self, auth_base_url: str = _AUTH_BASE) -> None:
        self._auth_base_url = auth_base_url.rstrip("/")
        self._client = httpx.Client()

    def build_authorization_url(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        scope: str,
        state: str,
        code_challenge: str | None = None,
        code_challenge_method: str = "S256",
        response_type: str = "code",
    ) -> str:
        params: dict[str, str] = {
            "response_type": response_type,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
        }
        if code_challenge is not None:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method
        query = httpx.URL("", params=params).query.decode()
        return f"{self._auth_base_url}/oauth2/authorize?{query}"

    def discover(self) -> dict[str, Any]:
        resp = self._client.get(f"{self._auth_base_url}/.well-known/oauth-authorization-server")
        resp.raise_for_status()
        return resp.json()

    def exchange_code(
        self,
        *,
        client_id: str,
        code: str,
        redirect_uri: str,
        client_secret: str | None = None,
        code_verifier: str | None = None,
    ) -> dict[str, Any]:
        data: dict[str, str] = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
        }
        if client_secret is not None:
            data["client_secret"] = client_secret
        if code_verifier is not None:
            data["code_verifier"] = code_verifier
        resp = self._client.post(f"{self._auth_base_url}/oauth2/token", data=data)
        resp.raise_for_status()
        return resp.json()

    def refresh_token(
        self,
        *,
        refresh_token: str,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> dict[str, Any]:
        data: dict[str, str] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        if client_id is not None:
            data["client_id"] = client_id
        if client_secret is not None:
            data["client_secret"] = client_secret
        resp = self._client.post(f"{self._auth_base_url}/oauth2/token", data=data)
        resp.raise_for_status()
        return resp.json()

    def revoke_token(
        self,
        *,
        token: str,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        data: dict[str, str] = {"token": token}
        if client_id is not None:
            data["client_id"] = client_id
        if client_secret is not None:
            data["client_secret"] = client_secret
        self._client.post(f"{self._auth_base_url}/oauth2/revoke", data=data)

    def get_user_info(self, access_token: str) -> dict[str, Any]:
        resp = self._client.get(
            f"{self._auth_base_url}/api/v1/users/me",
            headers={"authorization": "Bearer " + access_token},
        )
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> OAuth:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncOAuth:
    """Async OAuth 2.0 helper for "Sign in with Ace Data Cloud"."""

    def __init__(self, auth_base_url: str = _AUTH_BASE) -> None:
        self._auth_base_url = auth_base_url.rstrip("/")
        self._client = httpx.AsyncClient()

    def build_authorization_url(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        scope: str,
        state: str,
        code_challenge: str | None = None,
        code_challenge_method: str = "S256",
        response_type: str = "code",
    ) -> str:
        params: dict[str, str] = {
            "response_type": response_type,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
        }
        if code_challenge is not None:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method
        query = httpx.URL("", params=params).query.decode()
        return f"{self._auth_base_url}/oauth2/authorize?{query}"

    async def discover(self) -> dict[str, Any]:
        resp = await self._client.get(f"{self._auth_base_url}/.well-known/oauth-authorization-server")
        resp.raise_for_status()
        return resp.json()

    async def exchange_code(
        self,
        *,
        client_id: str,
        code: str,
        redirect_uri: str,
        client_secret: str | None = None,
        code_verifier: str | None = None,
    ) -> dict[str, Any]:
        data: dict[str, str] = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
        }
        if client_secret is not None:
            data["client_secret"] = client_secret
        if code_verifier is not None:
            data["code_verifier"] = code_verifier
        resp = await self._client.post(f"{self._auth_base_url}/oauth2/token", data=data)
        resp.raise_for_status()
        return resp.json()

    async def refresh_token(
        self,
        *,
        refresh_token: str,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> dict[str, Any]:
        data: dict[str, str] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        if client_id is not None:
            data["client_id"] = client_id
        if client_secret is not None:
            data["client_secret"] = client_secret
        resp = await self._client.post(f"{self._auth_base_url}/oauth2/token", data=data)
        resp.raise_for_status()
        return resp.json()

    async def revoke_token(
        self,
        *,
        token: str,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        data: dict[str, str] = {"token": token}
        if client_id is not None:
            data["client_id"] = client_id
        if client_secret is not None:
            data["client_secret"] = client_secret
        await self._client.post(f"{self._auth_base_url}/oauth2/revoke", data=data)

    async def get_user_info(self, access_token: str) -> dict[str, Any]:
        resp = await self._client.get(
            f"{self._auth_base_url}/api/v1/users/me",
            headers={"authorization": "Bearer " + access_token},
        )
        resp.raise_for_status()
        return resp.json()

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncOAuth:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
