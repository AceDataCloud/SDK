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

## Spec Overlays

Machine-readable metadata in [spec/overlays](spec/overlays/) drives code generation:

- `domains.yaml` — service domains and grouping
- `operations.yaml` — HTTP method + path for each operation
- `tasks.yaml` — which operations return async tasks
- `streams.yaml` — which operations support SSE streaming
- `uploads.yaml` — which operations accept file uploads
