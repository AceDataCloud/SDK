# AceDataCloud SDK

Official SDK clients for the [AceDataCloud API](https://platform.acedata.cloud).

## Languages

| Language | Directory | Package |
|----------|-----------|---------|
| Python | [python](python/) | `acedatacloud` |
| TypeScript | [typescript](typescript/) | `@acedatacloud/sdk` |

## Architecture

Both SDKs share the same design:

```
client
├── openai          # OpenAI-compatible completions & responses
├── chat            # Native chat messages
├── images          # Image generation (returns TaskHandle for polling)
├── audio           # Music generation (returns TaskHandle)
├── video           # Video generation (returns TaskHandle)
├── search          # Web search
├── tasks           # Cross-service task retrieval
├── files           # File uploads
└── platform        # Applications, credentials, models, config
```

### Key Patterns

- **Task-based generation**: Image/audio/video endpoints return a `TaskHandle` that polls until completion
- **SSE streaming**: Chat and OpenAI-compat endpoints support streaming via Server-Sent Events
- **Automatic retries**: Transient errors (5xx, network) are retried with exponential backoff + jitter
- **Error hierarchy**: Typed errors for auth, rate-limit, balance, validation, moderation, etc.
- **Dual base URLs**: API gateway (`api.acedata.cloud`) for calling-plane, platform (`platform.acedata.cloud`) for management
- **Pluggable payment handler**: on `402 Payment Required`, the SDK invokes an optional handler to produce the retry headers — the integration point for on-chain (x402) payments

## Paying Per Request with X402

Both SDKs expose a `paymentHandler` / `payment_handler` hook that is
called when the server returns `402 Payment Required`. Plug in
[`@acedatacloud/x402-client`](https://github.com/AceDataCloud/X402Client)
and the SDK can call any x402-enabled endpoint using on-chain USDC
instead of a Bearer token — no other code changes needed.

```typescript
import { AceDataCloud } from '@acedatacloud/sdk';
import { createX402PaymentHandler } from '@acedatacloud/x402-client';

const client = new AceDataCloud({
  paymentHandler: createX402PaymentHandler({
    network: 'base',
    evmProvider: window.ethereum,
    evmAddress: '0xYourAddress...',
  }),
});

await client.openai.chat.completions.create({
  model: 'gpt-4o-mini',
  messages: [{ role: 'user', content: 'hi' }],
});
```

In Python the hook is the same shape — any callable that returns
`{"headers": {"X-Payment": "<base64-envelope>"}}`. See
[python/README.md](python/README.md#paying-with-x402-instead-of-a-bearer-token).

## Spec Overlays

Machine-readable metadata in [spec/overlays](spec/overlays/) drives code generation:

- `domains.yaml` — service domains and grouping
- `operations.yaml` — HTTP method + path for each operation
- `tasks.yaml` — which operations return async tasks
- `streams.yaml` — which operations support SSE streaming
- `uploads.yaml` — which operations accept file uploads
