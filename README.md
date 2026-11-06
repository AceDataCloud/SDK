# AceDataCloud SDK

Official SDK clients for the [AceDataCloud API](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_catalog_readme_platform).

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_catalog_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_catalog_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

Use this application key for API requests. SDK account-management methods require the separate credential described in their management documentation; do not interchange it with the API key. The optional x402 payment flow below is a separate way to pay for supported requests.

## For single-service integration maintainers

The public SDK is shared infrastructure for independently named service integrations. Keep the service identity visible (for example **Suno by Ace Data Cloud**) and point users to that platform's verified install entry, not only to a generic API URL. The SDK itself is not a default provider listing in another application.

Use the [English/Chinese first-use templates and real API-key screenshot sources](docs/integration-onboarding/README.md) to build the service's installation → application key → host credential → first request → same-task retrieval guide. The templates preserve the current four UTM fields and require platform-specific instructions; they do not generate fake screenshots or claim a marketplace release.

## Languages

**LlamaIndex example:** [web search → extraction → cited retrieval](python/examples/llamaindex/README.md)
([中文](python/examples/llamaindex/README.zh-CN.md)), with a no-token offline demo and hosted MCP discovery.

| Language | Directory | Package |
|----------|-----------|---------|
| Python | [python](python/) | `acedatacloud` |
| TypeScript | [typescript](typescript/) | `@acedatacloud/sdk` |
| Go | [go](go/) | `github.com/AceDataCloud/SDK/go` |

## Framework examples

- [LangChain chat](examples/langchain/): use `langchain-openai` with the
  OpenAI-compatible Chat Completions endpoint for text, streaming, and tools.

## Architecture

All three SDKs share the same design, organised along **two axes**:

```
client
│
├── ── provider axis — one namespace per service, fully typed ──
│   ├── kling       # every Kling parameter, validated
│   ├── veo         # generate / upsample / extend / reshoot / objects
│   ├── glm
│   └── openai      # OpenAI-compatible completions & responses
│
├── ── modality axis — pick a provider at call time ──
│   ├── images      # images.generate(prompt=..., provider="flux")
│   ├── audio
│   ├── video
│   └── chat
│
└── ── cross-cutting ──
    ├── search      # Web search
    ├── tasks       # Cross-service task retrieval
    ├── files       # File uploads
    └── platform    # Applications, credentials, models, config
```

The **provider axis** is the primary surface: services in the same modality do
not share a parameter set (Kling has `cfg_scale` and `camera_control`, Flux has
`size` and `count`), so each gets a closed, precisely typed signature.

The **modality axis** is a convenience wrapper over it, for callers who just
want "generate an image" and are happy with common parameters plus a
`provider=` switch. It delegates rather than reimplementing.

### Key Patterns

- **Task-based generation**: Image/audio/video endpoints return a `TaskHandle` that polls until completion
- **SSE streaming**: Chat and OpenAI-compat endpoints support streaming via Server-Sent Events
- **Automatic retries**: Transient errors (5xx, network) are retried with exponential backoff + jitter
- **Error hierarchy**: Typed errors for auth, rate-limit, balance, validation, moderation, etc.
- **Dual base URLs**: calling plane (`x402.acedata.cloud`) and management plane (`platform.acedata.cloud`)
- **Pluggable payment handler**: on `402 Payment Required`, the SDK invokes an optional handler to produce the retry headers — the integration point for on-chain (x402) payments

## Platform balances and usage retention

Python and TypeScript expose application details through `client.platform.applications.get`.
Use an Account Token, not a generation API key. For Proxy-type services, a paused
balance sync or sync timeout returns the last saved `remaining_amount`; a positive
balance does not establish current service availability. Check service status,
`disabled`, and `expired_at`, and interpret the amount using `service.unit`, not
as dollars. The balance endpoint, authentication, and field names are unchanged.
See the [application details guide](https://platform.acedata.cloud/documents/platform-application-detail).

Application list, detail, and create responses expose `allow_overdraft`, a
read-only boolean that defaults to `false` and can only be enabled by an
administrator, not through application creation parameters. An authorized
`Usage` application may continue calling with an insufficient or negative
`remaining_amount`; a negative balance is unsettled usage. Recharges offset
that balance without resetting `used_amount`. Disabled/expired applications and
credential limits still apply. An overdraft-enabled application continues to
charge its own balance instead of switching to the global application for
insufficient funds. Otherwise `allow_consume_global` applies; after switching,
the charged global application's overdraft setting determines eligibility.
The SDK returns these fields unchanged and does not authorize overdraft locally.

Platform account usage records and billing summaries are queryable for the latest
60 days; request and response bodies are retained separately for 30 days. Records
30–60 days old still retain trace, status, timing, model, usage, and actual-charge
summaries, but their details no longer return `metadata.request`
or `metadata.response`. Body expiry does not change actual charges, usage, or
aggregate statistics. Save bodies at call time if you need longer retention.
The SDK has no usage-list, aggregate, or CSV-export helper; consult the existing
[usage list](https://platform.acedata.cloud/documents/platform-usage-list),
[aggregate](https://platform.acedata.cloud/documents/platform-usage-aggregate), and
[export](https://platform.acedata.cloud/documents/platform-usage-export) guides for
those account-management operations.

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

## Provider generation

Most provider-axis clients are generated for Python, TypeScript, and Go from the
pinned OpenAPI snapshots in [`scripts/specs`](scripts/specs/) and the curated
[`scripts/services.json`](scripts/services.json) manifest:

```bash
python3 scripts/generate_providers.py \
  --manifest scripts/services.json \
  --specs scripts/specs \
  --languages python,typescript,go
```

Kling, OpenAI, Serp, ShortURL, WebExtrator, and Veo remain hand-written because
they contain validation or helper behavior that the selected OpenAPI operations
do not fully express. CI reruns the generator and requires a clean working tree.

The older files in [spec/overlays](spec/overlays/) are inactive design artifacts;
they are not generator inputs and cover only the original nine domains.

## Contract synchronization

PlatformBackend's daily ecosystem CronJob prepares incremental capability PRs
using a pinned Backend source. Existing CI and human review gate each update.
The previous dispatch/Copilot sync workflows are retired.

For an offline preview, use a clean SDK checkout and a PlatformBackend checkout at
the source SHA:

```bash
python3 scripts/sync_from_platformbackend.py --backend-dir ../PlatformBackend --services flux
python3 scripts/generate_providers.py --manifest scripts/services.json --specs scripts/specs --languages python,typescript,go
```

The curated manifest is not expanded automatically. New endpoints and the six
hand-written client families above need review; missing or moved operations fail
before any snapshot is written. A schema removal or stricter parameter may be a
breaking API change, so generated PRs remain drafts until compatibility is checked.

## Daily capability updates

PlatformBackend `ecosystem.py` is the only scheduled coordinator.
One daily Kubernetes Job reviews Backend docs and API changes with Claude Code,
updates existing files, and creates or updates one reviewable PR per repository.
It never merges PRs or duplicates the Backend guide tree. Normal CI and review
remain required; publication and sub-repository mirroring run after merge.

## Native Zapier application

The [Ace Data Cloud Zapier application](https://github.com/AceDataCloud/AceDataCloudZapier)
has its own source, package and release workflow. It provides named Suno music
generation and original-task recovery actions alongside chat. Follow its
[English guide](https://github.com/AceDataCloud/AceDataCloudZapier/blob/main/README.md)
or [Chinese guide](https://github.com/AceDataCloud/AceDataCloudZapier/blob/main/readme/README_zh_Hans.md)
for actual publication status, account connection and billing boundaries.

The application is source-only until its private upload and public review are
verified; this link is not a Zapier installation or listing. SDK clients do not
embed or maintain a second copy of the Zapier application.

## MiMo

`mimo-v2.6-pro` and `mimo-v2.6-flash` are model identifiers for the existing OpenAI-compatible `client.openai.chat.completions.create` interface in Python/TypeScript (and the corresponding Go client), including streaming. Check the live console catalog, service status and account access before using it. Use `max_completion_tokens`, preserve captured assistant `reasoning_content` during tool continuations, and use only function tools with `tool_choice=auto`. This does not enable MiMo on Responses or Messages.

### GPT Image 2.6 native GIF

GIF generation and editing are available for `gpt-image-2.6-flare`, its `:reverse`/`:official` variants, and all `gpt-image-2.6-sunburst` variants.  Use `output_format="gif"` in Python, `outputFormat: "gif"` in TypeScript, or `OutputFormat: "gif"` in Go. Frame controls are `frame_count`/`frame_duration_ms` (Python), `frameCount`/`frameDurationMs` (TypeScript), and `FrameCount`/`FrameDurationMS` (Go).

GIF defaults to a 512x512 preview, 9 frames and 200 ms per frame; actual dimensions may be adjusted by the model. The static 4K presets (`3840x2160`, `2160x3840`) remain supported for PNG/JPEG/WebP generation and editing on all 2.6 variants. GIF has separate size/frame constraints.

GPT Image 2.6 supports `complexity="low"|"medium"|"high"` (omitted: model default high). Static edits accept `markup`: a PNG with transparent pixels, matching the first reference after orientation, up to 16,777,216 pixels per image and 40MB for the annotation. JSON accepts an HTTPS URL, PNG data URL or an object containing only `image_url`; multipart accepts an annotation file. Do not combine markup with mask, GIF or prompt_rewriter. GIF frame count is 2–16; frame duration is 20–655350ms, rounded to 10ms. GIF rejects masks, custom compression and partial streaming. Pricing is unchanged.
