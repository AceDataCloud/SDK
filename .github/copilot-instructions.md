# Copilot Sync Instructions for AceDataCloud SDK

## Repository Structure

Three SDK implementations, all hand-written (there is no code generator):

- `python/` — `acedatacloud` on PyPI
- `typescript/` — `@acedatacloud/sdk` on npm
- `go/` — `github.com/AceDataCloud/SDK/go`

**All three must stay in step.** Go has historically lagged; do not add to that gap.

## Source of Truth

The **AceDataCloud/Docs** repo:

- `openapi/<service>.json` — OpenAPI specs, pre-localized to English
- `guides/<service>.md` — usage guides (optional reference)

## The SDK has two axes

This is the most important thing to understand before changing anything.

### Provider axis — the primary surface

`client.kling`, `client.veo`, `client.flux`, … One class per service, with a
**closed signature naming every parameter that service accepts**, its own types,
and its own validation.

This exists because providers in the same modality do not share a parameter set.
Kling takes `duration` / `cfg_scale` / `camera_control`; Flux takes `size` /
`count`; Seedream takes `seed` / `watermark`. There is no useful union of those.
An earlier attempt to force Midjourney into a shared `images.generate()` failed
and the provider was **deleted from the SDK rather than modeled** — that is the
failure mode this axis prevents.

**`python/src/acedatacloud/resources/kling.py` is the reference implementation.**
Copy its shape: closed keyword-only signature, a `_build_*_body` helper, explicit
cross-field validation raising `ValueError` with an actionable message.

### Modality axis — a convenience wrapper

`client.images`, `client.video`, `client.audio` take a `provider=` argument and
**delegate to the provider class**. They exist for callers who want "generate an
image" without picking a service first.

They must not reimplement provider logic. Adding a parameter to a provider class
must not require touching the modality class.

## What to Sync

When Docs changes, update **the provider class** for that service:

1. **Parameters** — compare the closed signature against the OpenAPI request
   schema. Add new parameters; do not remove existing ones unless the API did.
2. **Enums** — model names and other `enum` values become `Literal` types
   (Python), string unions (TypeScript), typed constants (Go).
3. **Required-ness** — mirror the spec's `required` list, with two known traps:
   - A spec's `required` list can **understate** what the upstream enforces.
     `/flux/images` declares only `action` and `prompt` required yet rejects a
     request without `size`. When a property carries an `example` but is not
     listed required, prefer sending the example over omitting it.
   - An `example` that **contradicts the property's own `enum` is wrong**. Flux
     documents `model` with the example `"generate"` — an *action* value, not a
     model. Trust the enum over the example.
4. **Paths** — verify against the OpenAPI `paths` section.
5. **Task endpoints** — every async service polls `POST /<service>/tasks`.

If a service has **no provider class yet, create one**. Do not add it to a
modality union as a shortcut — that is the pattern being retired.

## Async and tasks

Every generation method that can run asynchronously must:

- accept `async_` (Python) / `async` (TypeScript) / `Async` (Go);
- return a **`TaskHandle`, consistently** — never sometimes a dict and sometimes
  a handle. The caller decides whether to `.wait()`;
- support `wait=` / `poll_interval=` / `max_wait=`.

`TaskHandle.wait()` must work even when the server answered synchronously.

Terminal-state detection lives in one place per language (`_runtime/tasks.py`,
`runtime/tasks.ts`, `tasks.go`) and is deliberately heuristic — services report
completion inconsistently. **Do not simplify it.** If a new service reports
completion differently, extend the normalizer and add a case to the tests.

## Rules

- **Keep the three languages at parity.** A change in one is incomplete until the
  other two match.
- Do NOT modify `runtime/transport.*` or `runtime/errors.*` unless error codes
  changed.
- Do NOT modify CI/CD workflows.
- Keep backward compatibility: add, don't remove.
- Base URLs must be identical across languages (`x402.acedata.cloud` for the
  calling plane, `platform.acedata.cloud` for the management plane). Go drifted
  here once; check it.
- Every new provider class needs tests in all three languages.

## Verification

```bash
cd python     && ruff check . && pytest -v
cd typescript && npx tsc --noEmit && npm test
cd go         && go vet ./... && go test ./...
```

All three must pass. The sync workflow can merge with `--admin`, so a failing
check will not necessarily block a merge — **do not rely on that; fix it.**
