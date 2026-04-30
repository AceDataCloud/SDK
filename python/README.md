# AceDataCloud Python SDK

Official Python client for the [AceDataCloud API](https://platform.acedata.cloud).

## Installation

```bash
pip install acedatacloud
```

## Quick Start

```python
from acedatacloud import AceDataCloud

client = AceDataCloud(api_token="your-token")

# OpenAI-compatible chat completions
response = client.openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response["choices"][0]["message"]["content"])

# Streaming
for chunk in client.openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
):
    print(chunk.get("choices", [{}])[0].get("delta", {}).get("content", ""), end="")
```

## Async Usage

```python
import asyncio
from acedatacloud import AsyncAceDataCloud

async def main():
    client = AsyncAceDataCloud(api_token="your-token")
    result = await client.search.google(query="Python SDK")
    print(result)
    await client.close()

asyncio.run(main())
```

## Resources

| Resource | Description |
|----------|-------------|
| `client.openai` | OpenAI-compatible chat completions and responses |
| `client.chat` | Native chat messages |
| `client.images` | Image generation (Midjourney, Flux, etc.) |
| `client.audio` | Music generation (Suno) |
| `client.video` | Video generation (Luma, Sora, Veo, etc.) |
| `client.search` | Web search (Google SERP) |
| `client.tasks` | Cross-service async task polling |
| `client.files` | File uploads |
| `client.platform` | Applications, credentials, models management |

## Image Generation (with Task Polling)

```python
# Default provider (nano-banana)
task = client.images.generate(prompt="A sunset over mountains")
result = task.wait()  # polls until complete
print(result["image_url"])

# Use a specific provider
mj_task = client.images.generate(prompt="A sunset over mountains", provider="midjourney")
```

## Multi-Provider Support

Image, video, and audio resources support a `provider` parameter to switch between services:

```python
# Video — default is 'sora'
client.video.generate(prompt="A cat playing piano", provider="kling")
client.video.generate(prompt="Ocean waves", provider="luma")

# Audio — default is 'suno'
client.audio.generate(prompt="A jazz song", provider="producer")

# Suno Voice Clone
client.audio.voices(audio_url="https://example.com/voice.mp3", name="My Voice")
```

Available providers:

| Resource | Providers |
|----------|-----------|
| `client.images` | `nano-banana` (default), `midjourney`, `flux`, `seedream` |
| `client.video` | `sora` (default), `luma`, `veo`, `kling`, `hailuo`, `seedance`, `wan`, `pika`, `pixverse` |
| `client.audio` | `suno` (default), `producer`, `fish` |

## Error Handling

```python
from acedatacloud import AceDataCloud, AuthenticationError, RateLimitError

client = AceDataCloud(api_token="your-token")
try:
    client.search.google(query="test")
except AuthenticationError:
    print("Invalid or expired token")
except RateLimitError:
    print("Too many requests, slow down")
```

## Configuration

```python
client = AceDataCloud(
    api_token="your-token",
    base_url="https://api.acedata.cloud",       # API gateway
    platform_base_url="https://platform.acedata.cloud",  # Management plane
    timeout=300.0,      # Request timeout in seconds
    max_retries=2,      # Retry count for transient errors
)
```

The token can also be set via the `ACEDATACLOUD_API_TOKEN` environment variable.

## Paying with X402 Instead of a Bearer Token

The SDK supports a pluggable `payment_handler` that is invoked when the
API returns `402 Payment Required`. Any callable (or async callable)
that returns the required headers is accepted:

```python
from acedatacloud import AceDataCloud, PaymentHandlerContext, PaymentHandlerResult

def my_payment_handler(ctx: PaymentHandlerContext) -> PaymentHandlerResult:
    # ctx["accepts"] is the list of payment requirements returned by the server.
    # Your job: sign the preferred one and return the retry header.
    x_payment = sign_and_encode(ctx["accepts"])  # your implementation
    return {"headers": {"X-Payment": x_payment}}

client = AceDataCloud(payment_handler=my_payment_handler)

# Normal SDK calls — the handler is only invoked when the server returns 402.
result = client.openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hi"}],
)
```

The `AsyncAceDataCloud` client accepts either a synchronous or
asynchronous handler, so you can plug in wallet SDKs that use
`asyncio`. A ready-made x402 signer for Python is not shipped yet
(there is a TypeScript implementation in
[`@acedatacloud/x402-client`](https://github.com/AceDataCloud/X402Client)
— contributions for a Python port are welcome).

## License

MIT
