# Suno Make app: publication packet

Prepared 2026-10-18. Source and reviewer materials only; no Make app, invite link, or public version has been created.

## Identity and discoverability proposal

- **Internal name:** `suno-acedatacloud` (proposal; check actual availability and existing app first).
- **Community directory service name:** `Suno`. The live submission form requires the exact service name and excludes the developer company; identify Ace Data Cloud in the description and publisher/landing page instead. The eventual cloud app label must follow Make's decision for the selected publication route.
- **Description:** Generate Suno music through Ace Data Cloud, save the asynchronous task ID, and retrieve the finished audio using your own Ace Data Cloud API token. Independent integration provided by Ace Data Cloud; not an official Suno app.
- **Proposed categories:** AI, music/audio, automation; use only categories offered by the current review form.
- **Relevant search terms:** Suno, Suno music, AI music, Ace Data Cloud. Put terms in accurate label/description/module text and landing-page content; no unrelated keyword stuffing or ranking claims.
- **Modules:** Generate Suno music; Get a Suno task; Make an API call.
- **Community logo:** use only a service-identifying asset with the necessary rights confirmed by its owner. The form says to omit a new logo when an existing service listing already supplies it. Do not submit the Ace company logo as the service logo or assume Suno logo rights.
- **Install URL:** pending actual Make app, publisher eligibility, and review. Never substitute a source URL for an official installation link.

Make's [app naming rules](https://developers.make.com/custom-apps-documentation/best-practices/naming-conventions/apps) prohibit advertising descriptions in the app name. The [live Community submission form](https://f.make.com/submit-your-app), checked 2026-10-19, is more specific: use the exact service name, do not include the developer company unless it is part of the official product name, and stay within 60 characters. Therefore **Suno** is the directory-name draft; **provided by Ace Data Cloud** belongs in the description, provider identity and landing page. A README title describing ownership is not the value to paste into the form's app-name field. See the [current form worksheet](../COMMUNITY_SUBMISSION.md) for all required fields and legal gates. [Module labels](https://developers.make.com/custom-apps-documentation/best-practices/naming-conventions/modules/module-labels) use action/entity sentence case.

## Choose the permitted public path

The [standard technical-review prerequisites](https://developers.make.com/custom-apps-documentation/app-review/prerequisites) require a service not already integrated, warn against redirect/dependent APIs, and require a universal module, safe secrets, accurate interfaces and real test scenarios. Ace provides its own API domain and customer token, but those facts do not establish eligibility. Ask the authorized publisher to resolve the service/brand classification before public submission.

The separate [Community App policy](https://developers.make.com/custom-apps-documentation/community-apps/how-does-it-work) explicitly allows multiple partner apps connecting the same service, but requires a signed Make partner, no default/roadmap conflict, a published invite-only app, an invite URL, and a developer landing page. Its FAQ states its thinking is from July 2023; verify current partner eligibility instead of assuming it. The documented submission form is <https://f.make.com/submit-your-app>; no submission or legal acceptance was made.

The public review flow requires **Publish** before requesting review and says publishing cannot be undone. Trademark rights, external-service compliance, indemnification, support contacts, and any partner agreement require the authorized owner. Do not click Publish to bypass a missing decision.

## Scenario and evidence checklist

1. Inspect the intended account's existing apps. Assign a separate existing/private Suno origin, actual zone `/api`, app ID/version, organization/team and scoped development credential. Never replace the chat origin or another developer's record.
2. Deploy this project only to the authorized private test app. Verify all three module labels, connection field, interface and Authorization redaction.
3. Free checks: Connection and universal `GET /v1/models`; an error-only connection/GET; Get a Suno task for an existing owned task ID. Record scenario URLs, execution IDs, sanitized outputs, and log inspection. The lookup must be run without a generation module before it.
4. With a separate current generation budget only: generate once, preserve task ID, query that ID until terminal, verify all audio links and one corresponding usage charge at the current account package rate. Do not replay generation to poll.
5. Re-run each module's test immediately before review, because Make execution logs expire. Get separate-organization installation proof from the real invite/listing after publication.

Partial tracks remain pending and all failed/pending tasks hide audio URLs. Only an allowlist of task ID, status, success, trace ID, titles and completed audio URLs is exposed; internal request/user/credential/routing fields are not returned by the query module. The current implementation expects the API's JSON-object `response` envelope; unsupported string envelopes are rejected. Static expression simulations are not Make IML-engine certification.

## Landing page copy and acquisition

**Headline:** Suno music workflows in Make, provided by Ace Data Cloud.

**Value:** Describe music, submit once, and connect the completed audio to your workflow. Bring your own Ace Data Cloud API token. Make operation charges and Ace API generation charges are separate; consult current prices and account restrictions.

**Install:** pending Make's real installation link. **Get API token:** <https://platform.acedata.cloud/console/applications?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_listing_api_key>. **Pricing:** <https://platform.acedata.cloud/models?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_listing_pricing>.

Use the linked English/Chinese README as the developer landing material until a reviewed site URL is selected. Actual public listing form, install link, logo rights and support contact remain owner-supplied. UTM source/medium/campaign/content values identify this Make entry; no conversion, paid-user or revenue claim is made.

## Native AI Provider track

This music app is a tool/app, not the LLM that reasons for a Make AI Agent. Make documents a fixed [LLM-provider enum and GET inspection routes](https://developers.make.com/api-documentation/api-reference/ai-agents/llm-providers), including `openai-api-spec-compatible`, but no public create-brand-provider route. The [AI Agent setup guide](https://help.make.com/create-your-first-ai-agent) requires a paid Make plan for custom provider connections. A manually configured compatible connection does not make **Ace Data Cloud** a default named provider.

Prepared provider-review facts: provider name Ace Data Cloud; API origin `https://api.acedata.cloud`; application Bearer token; `GET /v1/models`; non-streaming `POST /v1/chat/completions`; current chat-only catalog `https://platform.acedata.cloud/api/v1/models/?type=chat&with_pricing=true`; no automatic model fallback. Connection/model-list behavior must be inspected in an authorized account, and a full tool-call conversation still needs a separately approved budget. Do not claim all Make AI Agent features from protocol compatibility. The authorized publisher needs Make's supported provider onboarding route for a branded default entry; no unsolicited third-party message is sent by this project.
