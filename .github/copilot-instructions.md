# Copilot Sync Instructions for AceDataCloud SDK

## Repository Structure

This is a monorepo with two SDK implementations:

- `typescript/` — TypeScript/Node.js SDK (`@acedatacloud/sdk` on npm)
- `python/` — Python SDK (`acedatacloud` on PyPI)

## Source of Truth

The **AceDataCloud/Docs** repo is the source of truth:

- `openapi/<service>.json` — OpenAPI specs for each service
- `guides/<service>.md` — Usage guides (optional reference)

## What to Sync

When the Docs repo changes, compare the OpenAPI specs against the SDK code and update:

### TypeScript (`typescript/src/`)

1. **Provider types** in `resources/images.ts`, `resources/video.ts`, `resources/audio.ts`:
   - Each resource has a union type (e.g., `ImageProvider`, `VideoProvider`, `AudioProvider`)
   - Ensure all providers from the OpenAPI specs are included
   - Default provider should match the most common/stable option

2. **Task endpoints** in `resources/tasks.ts`:
   - `SERVICE_TASK_ENDPOINTS` map must include all providers
   - Format: `'provider-name': '/provider-name/tasks'`

3. **Request parameters** in resource files:
   - Compare function parameter types against OpenAPI request body schemas
   - Add any new required or optional parameters

4. **API paths** in resource files:
   - Verify endpoint paths match the OpenAPI `paths` section
   - Special cases (e.g., midjourney uses `/midjourney/imagine` not `/midjourney/images`)

### Python (`python/src/acedatacloud/`)

1. **Provider enums/types** — same logic as TypeScript
2. **Request models** — match OpenAPI schemas
3. **Endpoint paths** — match OpenAPI paths

## Rules

- Do NOT change the SDK architecture or patterns — only update data (providers, parameters, paths)
- Do NOT modify `runtime/transport.ts` or `runtime/errors.ts` unless the error codes change
- Do NOT modify CI/CD workflows
- Keep backward compatibility: add new providers/params, don't remove existing ones unless the API removed them
- Run `npx tsc --noEmit` in `typescript/` to verify changes compile
- Run `ruff check .` in `python/` to verify linting passes
