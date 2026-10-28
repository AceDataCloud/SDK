# AceDataCloud TypeScript SDK

Official TypeScript/Node.js client for the [AceDataCloud API](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_typescript_readme_platform).

Requires Node.js 18+ (uses native `fetch`).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_typescript_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_typescript_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

Use this application key for API requests. SDK account-management methods require the separate credential described in their management documentation; do not interchange it with the API key. The optional x402 payment flow below is a separate way to pay for supported requests.

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
| `client.images` | Image generation (Flux, Seedream, Nano Banana, etc.) |
| `client.audio` | Music generation (Suno) |
| `client.video` | Video generation (Luma, Sora, Veo, etc.) |
| `client.search` | Web search (Google SERP) |
| `client.face` | Face analysis & transformation (swap, beautify, age, cartoon) |
| `client.shorturl` | Short URL creation |
| `client.tasks` | Cross-service async task polling |
| `client.files` | File uploads |
| `client.platform` | Applications, credentials, models management |

## Chat usage and billing

Accepted model requests through Chat Completions, Responses, and Messages are
billed by the selected model's input, output, and cache usage, not a fixed fee
per request. Switching protocol formats does not change this to per-call billing
or guarantee that a model accepts that format. Consult current model prices and
`usage.cost` for the charge; the SDK preserves reported usage without recalculating it.

- Chat Completions `prompt_tokens` includes reported cached tokens.
- Responses `input_tokens` includes reported cached tokens.
- Messages `input_tokens` excludes separately reported `cache_read_input_tokens`
  and `cache_creation_input_tokens`; those dimensions are charged separately.

Do not add cached tokens to the input total again for Chat Completions or
Responses, or treat Messages input alone as the full input/cache usage.

## Public Chat Completions models

Pass these public IDs to `client.openai.chat.completions.create({ model, messages })`;
use `stream: true` for streaming. The SDK passes model-specific fields through
without rewriting model IDs or enforcing a catalog.

- `claude-opus-5-5`: supports text and streaming Chat Completions with `n: 1`.
  Omit `temperature` and `top_p` to use model defaults; do not set temperature below
  1 or a non-default top-p. Use `tool_choice: 'auto'`, not forced tools. For native
  thinking blocks, signatures, and native tool semantics, use `client.chat.messages`.
- `gemini-4-argon`: supports text and streaming Chat Completions. Thinking can
  consume output budget; Google recommends at least `max_tokens: 32768` for ordinary
  tasks. This does not expose Interactions background long-output functionality.
- `kimi-k3.1-pro`: always reasons; pass `reasoning_effort: 'low'`, `'high'`, or `'max'`.
  Do not disable reasoning. Keep the full assistant message, including
  `reasoning_content` and `tool_calls`, in multi-turn and tool-call history.
  The existing `kimi-k3` alias remains available; use `reasoning_effort: 'max'` for it.

Check current account access and prices before calling. A model's advertised
context size does not guarantee the platform's per-request limit.

## Native Claude Messages

Thinking and output configuration are passed through without SDK model-specific
enum or combination checks. The selected model determines which values it accepts.
For the beta `display: 'updates'` mode, set the required header on a dedicated
client (client headers apply to every request):

```typescript
const claude = new AceDataCloud({
  apiToken: 'your-token',
  headers: { 'anthropic-beta': 'thinking-display-updates-2026-08-18' },
});

const response = await claude.chat.messages.create({
  model: 'claude-sonnet-5-5',
  messages: [{ role: 'user', content: 'Explain this code.' }],
  thinking: { type: 'adaptive', display: 'updates' },
  output_config: { effort: 'high' },
});
```

Streaming and `claude.chat.messages.countTokens(...)` also preserve thinking
configuration. Parameter pass-through does not guarantee model support; API errors
are returned through the SDK's normal error handling.

## OpenAI Embeddings

```typescript
const embeddings = await client.openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: 'The food was delicious and the waiter...',
});
```

Supported models are `text-embedding-3-small` and `text-embedding-3-large`.
`text-embedding-ada-002` is no longer available. When migrating an existing index,
regenerate its vectors and rebuild the index; do not mix old and new model vectors.

## Image Generation (with Task Polling)

```typescript
// Default provider (nano-banana)
const task = await client.images.generate({ prompt: 'A sunset over mountains' });
const result = await task.wait();
console.log(result.image_url);

// Use a specific provider
const fluxTask = await client.images.generate({
  prompt: 'A sunset over mountains',
  provider: 'flux',
});
```

### Nano Banana 2.1

Select `model: 'nano-banana-2.1'` explicitly for generation or editing at
1K, 2K, or 4K. Omitting `model` still uses `nano-banana`; there is no
`nano-banana-2.1:official` variant.

```typescript
const task = await client.nanobanana.generate({
  action: 'generate',
  model: 'nano-banana-2.1',
  prompt: 'A blue ceramic vase on a cream background',
  resolution: '2K',
  aspectRatio: '1:1',
});
await task.wait();
const imageUrls = task.urls();

const editTask = await client.nanobanana.generate({
  action: 'edit',
  model: 'nano-banana-2.1',
  prompt: 'Change the vase to green; preserve the background',
  imageUrls,
  resolution: '4K',
});
await editTask.wait();
```

The public model ID also works with `client.openai.images.generate(...)` and
`client.openai.images.edit(...)`; those use the OpenAI-compatible fields
(`image` for editing) and return response objects, not task handles.

## Maestro Video Production

Use the provider client to request one finished video in one language:

```typescript
const task = await client.maestro.generate({
  prompt: 'Explain vector databases to beginners in 20 seconds',
  langs: ['en'],
  aspect: '9:16',
  duration: 20,
  scenario: 'narrated',
});
const result = await task.wait();
```

`langs` defaults to `['zh-cn']` and must contain exactly one language; create
separate tasks for other languages. The completed result contains one video in
`response.data.variants`. To revise a video, use `action: 'remix'`, `'edit'`, or
`'extend'` with `refTaskId: task.id`.

There is no quality tier: all videos use 1080p/30fps and target durations of
5–300 seconds. Successful tasks cost **0.7 Credits per actual delivered second**,
with integer billed seconds capped at the requested duration (falling back to
that duration if it cannot be read). All scenarios, actions, and languages have
the same rate; failed tasks and `/maestro/tasks` polling are free.

## Kling reference-video billing

Pass `videoList: [{ videoUrl: referenceUrl, referType: 'feature' }]`
to `client.kling.generate` with `model: 'kling-o1'` or `'kling-v3-omni'`.
Reference videos use a separate billing tier: **1.202 Credits/second** in `std`
mode and **1.602 Credits/second** in `pro` mode. For a 5-second O1 result,
`std` / `pro` cost **4.005 / 5.340 Credits** without a reference video, or
**6.010 / 8.010 Credits** with one.

`referType: 'base'` (the default) edits may follow the reference video's length;
billing uses the actual output duration rounded to the nearest integer second.
`referType: 'feature'` uses the requested `duration`. Read
`response.usage.reference_video_seconds` for the final billed seconds;
the request-time estimate can differ from the final charge. This is response
usage, not a request parameter. Image references and first/last frames alone do
not trigger reference-video billing. Do not combine `videoList` with
`generateAudio: true`.

## Suno music processing

Before a cover or extension, optionally call
`await client.suno.availability({ audioId })`. Use the song's `audio_id` from a
completed task, not its `task_id`. This is a synchronous API-token-authenticated
check, currently without a Credits charge; it returns the response object
directly, not a task handle to poll. `result.data.available` is only `true` on
success: it is positive evidence on the current channel, not a guarantee that
a subsequent operation will work. An inconclusive check returns an error,
including `503 availability_unknown`; never convert an error into `false`.
Preserve the error code and trace ID.

Use `client.suno.generate({ custom: true, lyric, style, negativeTags })` for
custom-mode music. `negativeTags` describes styles or genres to exclude; there
is currently no fixed character limit, but overly long input may still fail,
so keep it concise. The SDK sends it as `negative_tags` without truncation.

A downloadable audio file does not guarantee that its `audio_id` remains usable
for covers, extensions or stem separation. If processing returns
`suno_processing_unavailable`, keep the original `task_id` (the task handle's
`id`, when available) and the error's `traceId` for support. The related codes
`suno_model_unavailable` and `suno_processing_failed` mean the selected model is
unavailable for that operation or processing returned no audio, respectively.
Suno can also return `api_error` with the message
`the account may have been offline`; this is a server error, not an SDK
authentication error.
These HTTP 500 errors retain their `code`, `traceId` and `body` on `APIError`.
Retrieve an existing task rather than submitting a replacement generation just
to check its result.

## Fish voice models

`client.fish.model({ title, voices: audioUrl })` creates a reusable voice from a
single publicly downloadable audio URL string, not an array or a multipart
upload. Prefer a direct URL ending in `.mp3` or `.wav`. Successful creation
returns the model object directly (HTTP 201); its `_id` can be used as
`referenceId` in `client.fish.generate`.

Created voices are stored publicly long-term and may be searched and used by
other users. Omit `visibility`: passing `private` or `unlist` does not make the
voice private. For temporary reference audio without creating a saved model,
use `client.fish.generate({ text, references: [{ audio: audioUrl, text: transcript }] })`.

`client.audio.listFishModels({ selfOnly: true, pageSize: 20, pageNumber: 1 })`
lists voices created and saved through this platform by the calling account,
including voices created with its other API tokens. This only filters the list;
it does not restrict public use. Results are paginated in reverse creation order;
`sortBy` supports `created_at` and `task_count`, and `authorId` can further filter
them. Do not combine `selfOnly: true` with `titleLanguage`; that filter is for
the public library. Responses contain `total`, `items`, and `has_more`;
`has_more` is boolean for self queries and may be `null` for public-library queries.

## File uploads

`client.files.upload(fileBytes, { filename: 'photo.jpg' })` uses the
management-plane account token, not a generation API key. Use a separate client
configured with that token. Uploads return `file_url` and `mime`; use the returned
URL rather than constructing one. The platform assigns an `uploads/<uuid>` path
and preserves a safe filename extension. Supply a filename matching the actual
content: MIME inference from the filename does not convert the file. The default
single-file limit is 100 MB.

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
| `client.images` | `nano-banana` (default), `flux`, `seedream` |
| `client.video` | `sora` (default), `luma`, `veo`, `kling`, `hailuo`, `seedance`, `wan`, `pika`, `pixverse` |
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
  baseURL: 'https://x402.acedata.cloud',
  platformBaseURL: 'https://platform.acedata.cloud',
  timeout: 300000,    // ms
  maxRetries: 2,
});
```

The token can also be set via the `ACEDATACLOUD_API_TOKEN` environment variable.

`await client.platform.config.get()` returns `features` and `region`. `region`
is the lowercase country/region code detected from the request IP, or `null`
when unknown. The endpoint accepts no country/region override. Keep any
user-selected display region in your own application; it does not change
server-side availability or security policies. Feature keys may change; use
safe defaults for missing keys and do not share cached config across users.

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

The companion TypeScript/Python signers also support Arbitrum One
(`network: 'arbitrum'` or `'eip155:42161'`) for `exact` payments with native USDC
(6 decimals), not bridged USDC. Availability is rolled out per network: only
select Arbitrum when the server's current `accepts` offers it. A configured
signer does not enable the network on the server. Use the returned payment
requirements and price rather than hard-coding an amount; the SDK forwards
`accepts` unchanged to the handler. The wallet must support and hold funds on
the target chain.

## License

MIT
