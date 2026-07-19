import httpx
import pytest
import respx

from acedatacloud import AceDataCloud, AsyncAceDataCloud, KimiModel
from acedatacloud.resources.kimi import AsyncKimi, Kimi


def test_public_kimi_types_are_importable() -> None:
    model: KimiModel = "kimi-k3"
    assert model == "kimi-k3"


@respx.mock
def test_kimi_chat_completions() -> None:
    route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Hello!"}}]},
        )
    )
    client = AceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0)

    result = client.kimi.chat.completions.create(
        model="kimi-k3",
        messages=[{"role": "user", "content": "Hi"}],
        temperature=0.5,
    )

    assert result == {"choices": [{"message": {"content": "Hello!"}}]}
    assert route.called
    assert client.kimi.__class__ is Kimi
    client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_kimi_chat_completions_streaming() -> None:
    route = respx.post("https://api.acedata.cloud/kimi/chat/completions").mock(
        return_value=httpx.Response(200, text='data: {"delta":"ok"}\n\ndata: [DONE]\n\n')
    )
    client = AsyncAceDataCloud(api_token="test-token", base_url="https://api.acedata.cloud", max_retries=0)

    stream = await client.kimi.chat.completions.create(
        model="kimi-k3",
        messages=[{"role": "user", "content": "Hi"}],
        stream=True,
    )
    chunks = [chunk async for chunk in stream]

    assert chunks == [{"delta": "ok"}]
    assert route.called
    assert client.kimi.__class__ is AsyncKimi
    await client.close()
