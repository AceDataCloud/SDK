"""Tests for DiscordBotClient and AsyncDiscordBotClient."""

from __future__ import annotations

import httpx
import pytest
import respx

from acedatacloud.resources.discord_bot import AsyncDiscordBotClient, DiscordBotClient

BASE = "https://discord-bot-test.app.acedata.cloud"
TOKEN = "test-access-token"


@pytest.fixture
def client():
    c = DiscordBotClient(BASE, TOKEN)
    yield c
    c.close()


@pytest.fixture
def async_client():
    return AsyncDiscordBotClient(BASE, TOKEN)


# ── health ────────────────────────────────────────────────────────────


@respx.mock
def test_health(client):
    respx.get(f"{BASE}/health").mock(
        return_value=httpx.Response(200, json={"status": "ok", "gateway_ready": True})
    )
    result = client.health()
    assert result["status"] == "ok"
    assert result["gateway_ready"] is True


# ── whoami ────────────────────────────────────────────────────────────


@respx.mock
def test_whoami(client):
    respx.get(f"{BASE}/api/whoami").mock(
        return_value=httpx.Response(200, json={"data": {"id": "123", "username": "bot"}})
    )
    result = client.whoami()
    assert result["id"] == "123"
    assert result["username"] == "bot"


# ── guilds ────────────────────────────────────────────────────────────


@respx.mock
def test_list_guilds(client):
    respx.get(f"{BASE}/api/guilds").mock(
        return_value=httpx.Response(200, json={"data": [{"id": "g1", "name": "My Server"}]})
    )
    result = client.list_guilds()
    assert result[0]["id"] == "g1"


@respx.mock
def test_list_channels(client):
    respx.get(f"{BASE}/api/guilds/g1/channels").mock(
        return_value=httpx.Response(200, json={"data": [{"id": "c1", "name": "general"}]})
    )
    result = client.list_channels("g1")
    assert result[0]["name"] == "general"


@respx.mock
def test_create_channel(client):
    def handler(request):
        body = request.content.decode()
        assert '"name": "announcements"' in body or "announcements" in body
        return httpx.Response(200, json={"data": {"id": "c2", "name": "announcements"}})

    respx.post(f"{BASE}/api/guilds/g1/channels").mock(side_effect=handler)
    result = client.create_channel("g1", name="announcements")
    assert result["name"] == "announcements"


@respx.mock
def test_list_members(client):
    respx.get(f"{BASE}/api/guilds/g1/members").mock(
        return_value=httpx.Response(200, json={"data": [{"id": "u1", "username": "alice"}]})
    )
    result = client.list_members("g1", limit=50)
    assert result[0]["username"] == "alice"


# ── messages ──────────────────────────────────────────────────────────


@respx.mock
def test_send_message(client):
    def handler(request):
        import json
        body = json.loads(request.content)
        assert body["channel_id"] == "c1"
        assert body["content"] == "hello"
        assert "reply_to" not in body
        return httpx.Response(200, json={"data": {"id": "m1"}})

    respx.post(f"{BASE}/api/messages").mock(side_effect=handler)
    result = client.send_message(channel_id="c1", content="hello")
    assert result["id"] == "m1"


@respx.mock
def test_send_message_with_reply(client):
    import json as _json

    def handler(request):
        body = _json.loads(request.content)
        assert body["reply_to"] == "m0"
        return httpx.Response(200, json={"data": {"id": "m2"}})

    respx.post(f"{BASE}/api/messages").mock(side_effect=handler)
    result = client.send_message(channel_id="c1", content="reply", reply_to="m0")
    assert result["id"] == "m2"


@respx.mock
def test_list_messages(client):
    respx.get(f"{BASE}/api/channels/c1/messages").mock(
        return_value=httpx.Response(200, json={"data": [{"id": "m1", "content": "hi"}]})
    )
    result = client.list_messages("c1")
    assert result[0]["content"] == "hi"


@respx.mock
def test_search_messages(client):
    respx.get(f"{BASE}/api/channels/c1/messages/search").mock(
        return_value=httpx.Response(200, json={"data": [{"id": "m1"}]})
    )
    result = client.search_messages("c1", q="hello")
    assert len(result) == 1


@respx.mock
def test_edit_message(client):
    respx.patch(f"{BASE}/api/channels/c1/messages/m1").mock(
        return_value=httpx.Response(200, json={"data": {"id": "m1", "content": "updated"}})
    )
    result = client.edit_message("c1", "m1", content="updated")
    assert result["content"] == "updated"


@respx.mock
def test_delete_message(client):
    respx.delete(f"{BASE}/api/channels/c1/messages/m1").mock(
        return_value=httpx.Response(200, json={"data": {}})
    )
    result = client.delete_message("c1", "m1")
    assert result == {}


@respx.mock
def test_add_reaction(client):
    respx.post(f"{BASE}/api/channels/c1/messages/m1/reactions").mock(
        return_value=httpx.Response(200, json={"data": {}})
    )
    result = client.add_reaction("c1", "m1", emoji="👍")
    assert result == {}


@respx.mock
def test_pin_message(client):
    respx.post(f"{BASE}/api/channels/c1/messages/m1/pin").mock(
        return_value=httpx.Response(200, json={"data": {}})
    )
    result = client.pin_message("c1", "m1")
    assert result == {}


# ── DMs ───────────────────────────────────────────────────────────────


@respx.mock
def test_create_dm(client):
    respx.post(f"{BASE}/api/dms").mock(
        return_value=httpx.Response(200, json={"data": {"id": "dm1"}})
    )
    result = client.create_dm(recipient_id="u1")
    assert result["id"] == "dm1"


@respx.mock
def test_send_dm(client):
    respx.post(f"{BASE}/api/dms/send").mock(
        return_value=httpx.Response(200, json={"data": {"id": "m3"}})
    )
    result = client.send_dm(recipient_id="u1", content="hey")
    assert result["id"] == "m3"


# ── auth header ───────────────────────────────────────────────────────


@respx.mock
def test_auth_header_is_sent(client):
    def handler(request):
        assert request.headers["authorization"] == TOKEN
        return httpx.Response(200, json={"data": {"id": "123"}})

    respx.get(f"{BASE}/api/whoami").mock(side_effect=handler)
    client.whoami()


# ── context manager ───────────────────────────────────────────────────


def test_context_manager():
    with DiscordBotClient(BASE, TOKEN) as c:
        assert c is not None


# ── async ─────────────────────────────────────────────────────────────


@respx.mock
@pytest.mark.asyncio
async def test_async_whoami(async_client):
    respx.get(f"{BASE}/api/whoami").mock(
        return_value=httpx.Response(200, json={"data": {"id": "456"}})
    )
    result = await async_client.whoami()
    assert result["id"] == "456"
    await async_client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_send_message(async_client):
    respx.post(f"{BASE}/api/messages").mock(
        return_value=httpx.Response(200, json={"data": {"id": "m-async"}})
    )
    result = await async_client.send_message(channel_id="c1", content="async hi")
    assert result["id"] == "m-async"
    await async_client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_context_manager():
    respx.get(f"{BASE}/api/whoami").mock(
        return_value=httpx.Response(200, json={"data": {"id": "789"}})
    )
    async with AsyncDiscordBotClient(BASE, TOKEN) as c:
        result = await c.whoami()
        assert result["id"] == "789"
