from unittest.mock import Mock

from acedatacloud import AceDataCloud


def test_discord_channel_search_uses_documented_path_and_query():
    client = AceDataCloud(api_token="test-token")
    client.discord._transport = transport = Mock()

    client.discord.search_messages(channel_id="channel", q="hello", limit=25)

    transport.request.assert_called_once_with(
        "GET", "/api/channels/channel/messages/search", params={"q": "hello", "limit": 25}
    )


def test_telegram_message_and_chat_requests_use_documented_parameters():
    client = AceDataCloud(api_token="test-token")
    client.telegram._transport = transport = Mock()

    client.telegram.chats(limit=20, unread_only="false")
    client.telegram.send_message(target="@alice", text="hello", reply_to="42")

    assert transport.request.call_args_list[0].kwargs["params"] == {"limit": 20, "unread_only": "false"}
    assert transport.request.call_args_list[1].kwargs["json"] == {
        "target": "@alice",
        "text": "hello",
        "reply_to": "42",
    }
