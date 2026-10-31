from unittest.mock import Mock

import pytest

from acedatacloud.resources.openai_compat import OpenAI


@pytest.mark.parametrize("model", ["mimo-v2.6-pro", "mimo-v2.6-flash"])
@pytest.mark.parametrize("stream", [False, True])
def test_mimo_uses_existing_chat_transport_and_preserves_its_parameters(model, stream):
    transport = Mock()
    transport.request.return_value = {}
    transport.request_stream.return_value = iter(['{"choices":[]}'])
    messages = [{"role": "assistant", "content": "Ready", "reasoning_content": "Captured reasoning"}]
    result = OpenAI(transport).chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
        max_completion_tokens=64,
        thinking={"type": "enabled"},
        tool_choice="auto",
    )
    body = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": 64,
        "thinking": {"type": "enabled"},
        "tool_choice": "auto",
    }
    if stream:
        assert list(result) == [{"choices": []}]
        body["stream"] = True
        transport.request_stream.assert_called_once_with("POST", "/openai/chat/completions", json=body)
        transport.request.assert_not_called()
    else:
        assert result == {}
        transport.request.assert_called_once_with("POST", "/openai/chat/completions", json=body)
