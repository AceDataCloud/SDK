# AceDataCloud for Zapier

This is a Zapier Platform CLI integration for one text-only **Create Chat Response** action. It is at the source-code stage: no Zapier Developer version has been uploaded, no Zap has run, and it is not listed in the App Directory. The first upload should remain private until a real Zap and billing readback succeed.

## What users can do

Connect with an AceDataCloud API token from [Applications](https://platform.acedata.cloud/console/applications). The connection test calls the non-billable `GET /v1/models` endpoint. A separate connection name labels the account in Zapier; it is never sent to AceDataCloud. The model picker reads the public chat catalog and does not make a billable call.

The action sends one non-streaming `POST /v1/chat/completions` call. Each action test and each Zap run consumes AceDataCloud balance. It accepts:

| Input | Required | Meaning |
| --- | --- | --- |
| Model | Yes | Chat model selected from the current catalog. Availability depends on the connected account. |
| Prompt | Yes | Text to send as the user message; can be mapped from an earlier Zap step. |
| System instructions | No | Additional guidance sent before the user message. |
| Max completion tokens | No | Positive integer output limit. Some models may reject this parameter. |

The action returns the response ID, response text, model, finish reason, input tokens, output tokens, total tokens, and creation time in ISO 8601 format. A refusal appears as response text when the API returns it without ordinary content. Responses without text or a response ID fail visibly instead of producing an empty success. The action does not support images, tool calls, streaming, or multi-turn conversation history.

## Local checks

Use Node.js 22, the [Zapier production runtime](https://docs.zapier.com/integrations/build-cli/overview#requirements). The project pins `zapier-platform-core` and `zapier-platform-cli` to 19.1.0.
The `form-data` override updates a pinned transitive dependency of Zapier core to its patched 4.0.6 release.

```bash
cd examples/zapier
npm ci
npm test
npm run validate
npm run validate:publish
```

`validate` checks the schema locally. `validate:publish` also runs Zapier's online integration checks. Neither command uploads an integration or executes a paid chat request.

## Private installation and real Zap proof

1. Sign in with an AceDataCloud-owned [Zapier Developer account](https://zapier.com/app/developer). Run `zapier-platform login`; SSO users can use a Developer deploy key with `zapier-platform login --sso`. Keep the deploy key outside this repository.
2. Run `zapier-platform integrations` and check for an existing AceDataCloud integration. Link it with `zapier-platform link` if one exists. Otherwise register exactly one app with `zapier-platform register "AceDataCloud"`. Avoid duplicate apps: Zapier permits only one public integration for a brand.
3. Run `zapier-platform push` from this directory to upload version `0.0.1`. New versions start private. Verify the resulting integration ID, version, and private state in the [Developer Platform](https://zapier.com/app/developer). Do not promote it yet.
4. In the Zap editor, build a Zap with a safe test trigger (for example, Schedule by Zapier) and **Create Chat Response**. Connect a dedicated AceDataCloud token, choose a chat model, and map a short, non-sensitive prompt. Testing the action makes a real paid API call.
5. Turn the Zap on and cause one new trigger event. Keep the successful run in [Zap History](https://zapier.com/app/history). Check the action's response ID, text, model, and token usage. Check the corresponding AceDataCloud usage and balance record before repeating a failed or uncertain call. Do not capture the token or prompt in shared evidence.
6. Check invalid-token reconnection, a rejected request, rate-limit behavior, and the model picker in the real Zap editor. Use [Zapier Monitoring](https://zapier.com/app/developer) and HTTP logs for failures. Record the private version and Zap History URL as evidence.

`zapier-platform users:add <email> 0.0.1` can invite a limited tester. Avoid a public invite link during private validation; Zapier says access through such links cannot be revoked once shared.

## Errors, retries, and billing

The connection test and catalog request are read-only. The chat action is billable, including the Zap editor's Test step. Invalid credentials require reconnection; `401 token_mismatched` needs a token with Chat Completions access; `403 used_up` needs more balance. A 429 response raises Zapier's `ThrottledError`, so Zapier retries after a delay. The integration does not retry 5xx responses or timeouts itself. Any replay of a chat POST may generate another completion and charge again because this endpoint has no cross-request idempotency key. Check the usage record and response ID before replaying an uncertain result.

The action shows safe error text and an AceDataCloud trace ID, when one is returned, without displaying upstream details. Send unresolved cases to [support@acedata.cloud](mailto:support@acedata.cloud) with the response ID or trace ID, model, and approximate run time; never send an API token.

## Directory submission preparation

The suggested listing is **AceDataCloud**, description “AceDataCloud is an API platform for AI models and services,” homepage [platform.acedata.cloud](https://platform.acedata.cloud), and category **Artificial Intelligence → AI Models**. A square transparent [512 px brand icon](assets/acedatacloud-icon.png) is ready for upload in the Developer Platform. Verify its rendering there before review. The [privacy policy](https://docs.acedata.cloud/en/resources/privacy), [terms](https://docs.acedata.cloud/en/resources/terms), and [support page](https://docs.acedata.cloud/en/resources/support) are public; prompts and responses handled by this integration should follow those policies and Zapier's data handling rules.

Before submission, add an admin using an `@acedata.cloud` email address and provide a non-expiring, feature-enabled AceDataCloud test account for `integration-testing@zapier.com` through Zapier's secure submission form. Publish a user help article with connection and billing instructions. Test every offered action in an enabled Zap and preserve at least one successful Zap History run. Review the online publishing checks, branding, and privacy details, then submit from the Developer Platform's **Publish** form. Review approval leads to a public beta listing; it is separate from uploading a private version.

Keep `0.0.1` private while testing. After real Zap evidence and product review, prepare `1.0.0` for the public submission. Version changes and promotion must be deliberate because promoted versions are immutable and existing Zaps can remain on older versions.

Official references: [CLI setup and push](https://docs.zapier.com/integrations/build-cli/overview), [dynamic dropdowns](https://docs.zapier.com/integrations/build-cli/dynamic-dropdowns), [publishing requirements](https://docs.zapier.com/integrations/publish/integration-publishing-requirements), [branding](https://docs.zapier.com/integrations/publish/branding-guidelines), and [public review process](https://docs.zapier.com/integrations/publish/public-integration).
