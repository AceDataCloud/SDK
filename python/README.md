# AceDataCloud Python SDK

Official Python client for the [AceDataCloud API](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_python_readme_platform).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_python_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_python_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

Use this application key for API requests. SDK account-management methods require the separate credential described in their management documentation; do not interchange it with the API key. The optional x402 payment flow below is a separate way to pay for supported requests.

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
| `client.images` | Image generation (Flux, Seedream, Nano Banana, etc.) |
| `client.audio` | Music generation (Suno) |
| `client.video` | Video generation (Luma, Sora, Veo, etc.) |
| `client.search` | Web search (Google SERP) |
| `client.face` | Face analysis & transformation (swap, beautify, age, cartoon) |
| `client.shorturl` | Short URL creation |
| `client.tasks` | Cross-service async task polling |
| `client.files` | File uploads |
| `client.platform` | Applications, credentials, models management |

## Native Claude Messages

Thinking and output configuration are passed through without SDK model-specific
enum or combination checks. The selected model determines which values it accepts.
For the beta `display: "updates"` mode, set the required header on a dedicated
client (client headers apply to every request):

```python
with AceDataCloud(
    api_token="your-token",
    headers={"anthropic-beta": "thinking-display-updates-2026-08-18"},
) as client:
    response = client.chat.messages.create(
        model="claude-sonnet-5-5",
        messages=[{"role": "user", "content": "Explain this code."}],
        thinking={"type": "adaptive", "display": "updates"},
        output_config={"effort": "high"},
    )
```

`AsyncAceDataCloud` accepts the same header and fields. Streaming and
`client.chat.messages.count_tokens(...)` also preserve thinking configuration.
Parameter pass-through does not guarantee model support; API errors are returned
through the SDK's normal error handling.

## OpenAI Embeddings

```python
result = client.openai.embeddings.create(
    model="text-embedding-3-small",
    input="The food was delicious and the waiter...",
)
```

Supported models are `text-embedding-3-small` and `text-embedding-3-large`.
`text-embedding-ada-002` is no longer available. When migrating an existing index,
regenerate its vectors and rebuild the index; do not mix old and new model vectors.

## Image Generation (with Task Polling)

```python
# Default provider (nano-banana)
task = client.images.generate(prompt="A sunset over mountains")
result = task.wait()  # polls until complete
print(result["image_url"])

# Use a specific provider
flux_task = client.images.generate(prompt="A sunset over mountains", provider="flux")
```

### Nano Banana 2.1

Select `model="nano-banana-2.1"` explicitly for generation or editing at
1K, 2K, or 4K. Omitting `model` still uses `nano-banana`; there is no
`nano-banana-2.1:official` variant.

```python
task = client.nano_banana.generate(
    action="generate",
    model="nano-banana-2.1",
    prompt="A blue ceramic vase on a cream background",
    resolution="2K",
    aspect_ratio="1:1",
)
task.wait()
image_urls = task.urls()

edit_task = client.nano_banana.generate(
    action="edit",
    model="nano-banana-2.1",
    prompt="Change the vase to green; preserve the background",
    image_urls=image_urls,
    resolution="4K",
)
edit_task.wait()
```

`AsyncAceDataCloud` exposes the same parameters (await `generate` and `wait`).
The public model ID also works with `client.openai.images.generate(...)` and
`client.openai.images.edit(...)`; those use the OpenAI-compatible fields
(`image` for editing) and return response dictionaries, not task handles.

## Maestro Video Production

Use the provider client to request one finished video in one language:

```python
task = client.maestro.generate(
    prompt="Explain vector databases to beginners in 20 seconds",
    langs=["en"],
    aspect="9:16",
    duration=20,
    scenario="narrated",
)
result = task.wait()
```

`langs` defaults to `["zh-cn"]` and must contain exactly one language; create
separate tasks for other languages. The completed result contains one video in
`response.data.variants`. `AsyncAceDataCloud` supports the same parameters;
await both `generate` and `wait`. To revise a video, use `action="remix"`,
`"edit"`, or `"extend"` with `ref_task_id=task.id`.

There is no quality tier: all videos use 1080p/30fps and target durations of
5–300 seconds. Successful tasks cost **0.7 Credits per actual delivered second**,
with integer billed seconds capped at the requested duration (falling back to
that duration if it cannot be read). All scenarios, actions, and languages have
the same rate; failed tasks and `/maestro/tasks` polling are free.

## Multi-Provider Support

Image, video, and audio resources support a `provider` parameter to switch between services:

```python
# Video — default is 'sora'
client.video.generate(prompt="A cat playing piano", provider="kling")
client.video.generate(prompt="Ocean waves", provider="luma")

# Audio — default is 'suno'
client.audio.generate(prompt="A jazz song", provider="producer")
```

Available providers:

| Resource | Providers |
|----------|-----------|
| `client.images` | `nano-banana` (default), `flux`, `seedream` |
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
    base_url="https://x402.acedata.cloud",  # API gateway (default)
    platform_base_url="https://platform.acedata.cloud",  # Management plane
    timeout=300.0,  # Request timeout in seconds
    max_retries=2,  # Retry count for transient errors
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

The `AsyncAceDataCloud` client accepts either a synchronous or asynchronous
handler. For a ready-made signer, install `acedatacloud-x402` and pass its
handler directly:

```python
from acedatacloud import AceDataCloud
from acedatacloud_x402 import EVMAccountSigner, create_x402_payment_handler

client = AceDataCloud(
    payment_handler=create_x402_payment_handler(
        network="base",
        evm_signer=EVMAccountSigner.from_private_key("0x..."),
        prefer_scheme="upto",
    )
)
```

See [`AceDataCloud/X402Client`](https://github.com/AceDataCloud/X402Client) for
Base, Solana, and SKALE setup details.

## License

MIT
