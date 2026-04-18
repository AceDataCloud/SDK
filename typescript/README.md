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
| `client.video` | `sora` (default), `luma`, `veo`, `kling`, `hailuo`, `seedance`, `wan`, `pika`, `pixverse` |
| `client.audio` | `suno` (default), `producer` |

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

## License

MIT
