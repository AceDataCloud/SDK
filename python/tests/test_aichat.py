"""AIChat v2 contract tests."""

from unittest.mock import Mock

from acedatacloud import AceDataCloud


def test_aichat_v2_serializes_current_gemini_model_and_fields():
    client = AceDataCloud(api_token="test-token")
    transport = Mock()
    transport.request.return_value = {"id": "conversation-1", "answer": "Hello"}
    client.aichat._transport = transport

    result = client.aichat.create_v2(
        model="gemini-3.7-flash",
        action="chat",
        message={"role": "user", "content": "Hello"},
        allowed_mcp_servers=["server-1"],
        async_=False,
        limit=25,
    )

    assert result["id"] == "conversation-1"
    assert transport.request.call_args.args == ("POST", "/aichat2/conversations")
    assert transport.request.call_args.kwargs["json"] == {
        "model": "gemini-3.7-flash",
        "action": "chat",
        "message": {"role": "user", "content": "Hello"},
        "allowed_mcp_servers": ["server-1"],
        "async": False,
        "limit": 25,
    }
