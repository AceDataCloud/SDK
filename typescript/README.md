# AceDataCloud TypeScript SDK

Official TypeScript/Node.js client for the [AceDataCloud API](https://platform.acedata.cloud).

Requires Node.js 18+ (uses native `fetch`).

## Installation

```bash
npm install @acedatacloud/sdk
```

## Quick Start

```typescript
import { AceDataCloud } from '@acedatacloud/sdk';

const client = new AceDataCloud({ apiToken: 'your-token' });

// OpenAI-compatible chat completions
const response = await client.openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

## Streaming

```typescript
const stream = await client.openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Tell me a story' }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices?.[0]?.delta?.content ?? '');
}
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

```typescript
// Default provider (nano-banana)
const task = await client.images.generate({ prompt: 'A sunset over mountains' });
const result = await task.wait();
console.log(result.image_url);

// Use a specific provider
const mjTask = await client.images.generate({
  prompt: 'A sunset over mountains',
  provider: 'midjourney',
});
```

## Multi-Provider Support

Image, video, and audio resources support a `provider` parameter to switch between services:

```typescript
// Video — default is 'sora'
await client.video.generate({ prompt: 'A cat playing piano', provider: 'kling' });
await client.video.generate({ prompt: 'Ocean waves', provider: 'luma' });

// Audio — default is 'suno'
await client.audio.generate({ prompt: 'A jazz song', provider: 'producer' });
```

Available providers:

| Resource | Providers |
|----------|-----------|
| `client.images` | `nano-banana` (default), `midjourney`, `flux`, `seedream` |
| `client.video` | `sora` (default), `luma`, `veo`, `kling`, `hailuo`, `seedance`, `wan`, `pika`, `pixverse`, `midjourney` |
| `client.audio` | `suno` (default), `producer`, `fish` |

## Error Handling

```typescript
import { AceDataCloud, AuthenticationError, RateLimitError } from '@acedatacloud/sdk';

const client = new AceDataCloud({ apiToken: 'your-token' });
try {
  await client.search.google({ query: 'test' });
} catch (err) {
  if (err instanceof AuthenticationError) {
    console.error('Invalid or expired token');
  } else if (err instanceof RateLimitError) {
    console.error('Too many requests');
  }
}
```

## Configuration

```typescript
const client = new AceDataCloud({
  apiToken: 'your-token',
  baseUrl: 'https://api.acedata.cloud',
  platformBaseUrl: 'https://platform.acedata.cloud',
  timeout: 300000,    // ms
  maxRetries: 2,
});
```

The token can also be set via the `ACEDATACLOUD_API_TOKEN` environment variable.

## Paying with X402 Instead of a Bearer Token

The SDK supports a pluggable `paymentHandler` that is invoked when the
API returns `402 Payment Required`. Combine it with
[`@acedatacloud/x402-client`](https://github.com/AceDataCloud/X402Client)
to pay for requests on-chain (Base, Solana, SKALE) instead of using a
Bearer token:

```bash
npm install @acedatacloud/sdk @acedatacloud/x402-client
```

```typescript
import { AceDataCloud } from '@acedatacloud/sdk';
import { createX402PaymentHandler } from '@acedatacloud/x402-client';

const client = new AceDataCloud({
  // No apiToken needed — the x402 handler pays per request.
  paymentHandler: createX402PaymentHandler({
    network: 'base',               // or 'solana' | 'skale'
    evmProvider: window.ethereum,
    evmAddress: '0xYourAddress...',
  }),
});

const result = await client.openai.chat.completions.create({
  model: 'gpt-4o-mini',
  messages: [{ role: 'user', content: 'Say hi in 3 words' }],
  max_tokens: 10,
});
```

On each API call, the SDK first sends the request unauthenticated. If
the server replies with `402`, the SDK passes the `accepts` list to
the handler, which signs and returns an `X-Payment` header. The SDK
retries the request once with that header. Everything else — task
polling, streaming, retries, error mapping — keeps working exactly the
same.

You can still pass a Bearer token alongside the handler if you want a
mixed mode (some endpoints via subscription, others via x402) — the
SDK only invokes the handler when it actually sees a `402`.

## License

MIT
