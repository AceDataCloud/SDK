# AceDataCloud SDK RFC

## Status

- Phase: 1
- Status: Proposed and frozen for implementation planning
- Applies to: Python, Node/TypeScript, Go

## Purpose

This RFC defines the cross-language SDK conventions that all first-tier AceDataCloud SDKs must follow.

It exists to prevent divergence before code generation and runtime implementation begin.

This RFC standardizes:

- package naming
- top-level client structure
- subclient boundaries
- method naming
- request and client options
- authentication behavior
- error hierarchy
- retry and timeout behavior
- streaming behavior
- long-running task behavior
- upload behavior
- versioning and compatibility rules
- generated versus handwritten ownership boundaries

## Goals

- Keep Python, TypeScript, and Go SDKs conceptually identical.
- Make the top-level entrypoint simple for common usage.
- Preserve room for strongly typed, generated resource layers.
- Treat task polling and streaming as first-class features.
- Support both calling-plane APIs and management-plane APIs.

## Non-Goals

- This RFC does not define the final canonical OpenAPI aggregation format.
- This RFC does not define the generator vendor or toolchain.
- This RFC does not finalize second-tier language package layouts.
- This RFC does not include endpoint-by-endpoint modeling details.

## Package Naming

### Python

- package name: `acedatacloud`
- primary client: `AceDataCloudClient`
- async client: `AsyncAceDataCloudClient`

### TypeScript

- package name: `@acedatacloud/sdk`
- primary client class: `AceDataCloud`

### Go

- module path: `github.com/AceDataCloud/acedatacloud-go`
- primary client type: `sdk.Client`

## Top-Level Client

Every first-tier SDK must expose one top-level client as the primary entrypoint.

Responsibilities of the top-level client:

- hold immutable configuration
- construct subclients
- own transport defaults
- own retry, timeout, and auth defaults
- expose request hooks and telemetry hooks

### Required top-level subclients

- `chat`
- `images`
- `audio`
- `video`
- `search`
- `tasks`
- `files`
- `platform`
- `openai`

### Task Design Rule

- top-level clients must be immutable after construction
- subclients must share the parent runtime and transport
- subclients must not require separate auth configuration by default

## Subclient Boundaries

### `chat`

Native chat-like APIs that are not strictly OpenAI facade methods.

Examples:

- Claude Messages
- Claude Count Tokens
- native provider-specific chat APIs

### `openai`

OpenAI-compatible facades.

Examples:

- chat completions
- responses
- images generation/edit endpoints exposed through OpenAI-compatible forms

### `images`

Image-generation and image-editing APIs.

Examples:

- Nano Banana
- Seedream
- Flux
- Midjourney image flows in later phases

### `audio`

Audio and music generation APIs.

Examples:

- Suno
- Fish audio later

### `video`

Video generation APIs.

Examples:

- Sora
- Seedance
- Veo and Luma in later phases

### `search`

Synchronous search-style APIs.

Examples:

- SERP

### `tasks`

Cross-service task retrieval and polling helpers.

This client exists even when domain clients also expose task-aware helpers.

### `files`

Platform file upload and related helper operations.

### `platform`

Management-plane APIs.

Examples:

- services
- applications
- credentials
- config
- models

## Method Naming Rules

### General rules

- Use verb-noun naming.
- Prefer short, concrete names over provider-internal terminology.
- Avoid embedding transport details in method names.
- Avoid overloaded names that change return shape across languages.

### Domain examples

- `client.openai.chat.completions.create(...)`
- `client.openai.responses.create(...)`
- `client.images.generate(...)`
- `client.images.edit(...)`
- `client.audio.generate(...)`
- `client.video.generate(...)`
- `client.search.google(...)`
- `client.tasks.get(...)`
- `client.tasks.wait(...)`
- `client.files.upload(...)`
- `client.platform.applications.create(...)`
- `client.platform.credentials.rotate(...)`

### Canonical naming rule

When the same logical operation exists behind both native and compatibility paths:

- compatibility facades live under `openai`
- provider-native operations live under the domain client or provider-specific subgroup only if required

Example:

- `/v1/chat/completions` belongs to `openai.chat.completions.create`
- `/claude/messages` belongs to `chat.messages.create` or `chat.claude.messages.create` if a provider subgroup becomes necessary

## Models and Typing

### Generated models

Generated resource methods may produce generated request and response models.

### Stability rule

- output models must tolerate service evolution better than server-side validation models
- generated clients must avoid assuming too many response fields are permanently required

### Language-specific guidance

- Python: use typed models suitable for IDE support; allow dict-like escape hatches where necessary
- TypeScript: prefer exact exported types and discriminated unions where applicable
- Go: prefer explicit structs and typed option structs over `map[string]any` in public APIs

## Client Options

All first-tier SDKs must support a shared conceptual `ClientOptions` shape.

Required fields:

- `apiToken`
- `baseURL`
- `platformBaseURL`
- `timeout`
- `maxRetries`
- `headers`
- `userAgent`
- `transport`
- `retryPolicy`
- `telemetry`

### Defaults

- `baseURL` defaults to the public API base URL
- `platformBaseURL` defaults to the platform management API base URL
- retry must be enabled by default for retry-safe failures
- timeout must be set by default, not infinite

### Immutability rule

Client options are fixed at construction time. Per-request changes must go through request options.

## Request Options

Every SDK must provide per-request override options.

Required fields:

- `timeout`
- `maxRetries`
- `headers`
- `apiToken`
- `idempotencyKey`
- `signal` or cancellation equivalent

### Language mapping

- Python: keyword-only options object or explicit request options parameter
- TypeScript: trailing request options object
- Go: `context.Context` plus functional options or explicit per-call option struct

## Authentication

### Primary mode

Bearer token authentication is the default auth mode across calling-plane APIs.

### File Upload Required Behavior

- automatically inject `Authorization: Bearer <token>`
- allow per-request token override
- do not mutate client state when request overrides are used

### Management-plane support

Management-plane APIs use the same bearer token model from the platform side.

### Explicit non-goal for v1 SDKs

Do not automatically create applications or credentials behind the user’s back.

The SDK may provide helper methods for platform workflows, but must not implicitly provision resources during normal API calls.

## Error Hierarchy

All SDKs must provide a shared conceptual error model.

### Base classes

- `AceDataCloudError`
- `APIError`
- `TransportError`

### API error subclasses

- `AuthenticationError`
- `PermissionError`
- `RateLimitError`
- `ValidationError`
- `InsufficientBalanceError`
- `TokenMismatchError`
- `ResourceDisabledError`
- `ModerationError`
- `TimeoutError`
- `InternalServerError`

### Error mapping rules

Map gateway error codes into stable SDK errors where possible.

Examples:

- `invalid_token` -> `AuthenticationError`
- `token_mismatched` -> `TokenMismatchError`
- `used_up` -> `InsufficientBalanceError`
- `disabled` -> `ResourceDisabledError`
- `too_many_requests` -> `RateLimitError`
- `bad_request` -> `ValidationError`
- moderation-style `forbidden` responses -> `ModerationError`

### Error payload requirements

All API-facing errors should preserve:

- HTTP status code
- raw response body
- parsed error code if present
- parsed error message if present
- trace ID if present

## Retry Policy

Retries must be enabled by default for retry-safe failures.

### Default retry candidates

- network errors
- connection resets
- request timeout at transport layer
- HTTP 408
- HTTP 409 when explicitly marked retry-safe
- HTTP 429
- HTTP 500+

### Retry rules

- use exponential backoff with jitter
- make retry count configurable globally and per request
- disable retries for non-idempotent operations unless the request is protected by idempotency semantics or explicitly allowed

### Non-retry defaults

Do not automatically retry validation failures, auth failures, or moderation failures.

## Timeout Policy

Timeouts must be enabled by default.

### Rules

- each SDK defines a reasonable default request timeout
- long-running operations should separate submission timeout from wait timeout
- waiting for tasks must support independent polling timeout and total wait timeout

## Streaming

AceDataCloud must treat streaming as a first-class SDK feature.

### Supported streaming forms

- NDJSON streams
- SSE-like event streams

### Public behavior

SDK users must not need to manually parse raw wire formats for standard cases.

### Required abstractions

- Python: iterator and async iterator
- TypeScript: async iterable
- Go: event iterator or callback-driven reader abstraction

### Event shape rule

Where possible, streaming helpers should emit typed event objects rather than raw strings.

### Escape hatch

Each SDK may provide access to the raw stream for advanced users.

## Task Handling

Long-running task workflows are a first-class platform pattern.

### Required abstraction

All first-tier SDKs must expose a task handle or poller abstraction.

Minimum capabilities:

- `id`
- `get()`
- `wait()`
- `waitUntilCompleted()` or equivalent
- `isCompleted()` or equivalent
- `result()` or equivalent final-value accessor

### Design rule

Task submission methods may return either:

- a typed response containing a task handle field, or
- a typed task handle wrapper directly

But this must be consistent within a language.

### Polling defaults

- default polling interval must exist
- caller must be able to override polling interval
- caller must be able to set a maximum wait time

## Files and Uploads

The SDK must expose a standard upload helper for the platform upload endpoint.

### Required behavior

- upload from file path where language conventions allow
- upload from bytes or stream
- return a typed upload result containing the resulting file URL

### Integration behavior

Domain clients may accept uploaded file URLs directly, but the upload operation itself remains owned by `files`.

## Calling Plane vs Management Plane

The SDK supports both planes.

### Calling plane

- chat
- images
- audio
- video
- search
- tasks

### Management plane

- services
- applications
- credentials
- models
- config

### Rule

Calling-plane SDK usage must remain simple even if management-plane support is not used.

## Generation Boundary

### Generated

- operation methods
- request types
- response types
- path binding
- service grouping metadata where possible

### Handwritten

- transport runtime
- retry engine integration
- auth injection
- stream parsing
- task abstractions
- error mapping
- uploads
- request hooks
- OpenAI facade behavior when overlays are needed

### Ownership rule

Generated files must be treated as replaceable artifacts and must not contain handwritten business logic.

## Versioning Strategy

### SDK versioning

- Use semantic versioning for each language SDK.
- Breaking public API changes require a major version bump.
- Additive endpoint support is minor.
- Fixes and non-breaking internal behavior adjustments are patch releases.

### API compatibility

- SDKs should prefer backward-compatible client behavior when response schemas evolve.
- Avoid over-constraining generated output models where service evolution is likely.

## Documentation Requirements

Every first-tier SDK must ship with:

- installation instructions
- one quickstart
- one streaming example
- one task polling example
- one file upload example
- one management-plane example

## Testing Requirements

Minimum expectations for each first-tier SDK:

- unit tests for error mapping
- unit tests for auth injection
- unit tests for retry policy integration
- unit tests for streaming parser behavior
- unit tests for task waiting behavior
- smoke tests against at least one real endpoint class

## Phase 2 Entry Criteria

Phase 2 may begin when all of the following are true:

- this RFC is merged
- the canonical scope from Phase 0 remains accepted
- the generator/runtime boundary is accepted
- there is a chosen location for generated artifacts and handwritten runtime code

## Open Questions Deferred to Phase 2

- exact generator toolchain
- exact canonical spec build pipeline
- exact overlay implementation format
- whether provider-specific nested groups are needed beyond the initial domain clients
- how much of the OpenAI compatibility layer is generated versus wrapped manually
