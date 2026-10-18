# Seedance Make publication packet

Prepared 2026-10-18. No cloud app/official listing/invite link is provisioned.

- Community directory service name: **Seedance**. The current form requires the exact service name without the developer company. Put **provided by Ace Data Cloud** in the description, publisher identity and landing page; cloud labels remain subject to Make's decision.
- Proposed internal app name: `seedance-acedatacloud`; inspect availability and existing apps before assigning.
- Relevant discovery terms: **Seedance**, **Seedance video**, **Ace Data Cloud**. Accurate service descriptions only; no official-affiliation badge, unrelated keyword stuffing or ranking claim.
- Description: Generate one Seedance video through Ace Data Cloud, preserve its async task ID, and retrieve completed media using your own API token.
- Scope: Text-to-video only. Model IDs are selected explicitly. This module offers 480p/720p across its four Seedance 2.x models and 5/10-second targets; it does not expose reference uploads, editing, web search, or extension. Its API body uses `content=[{type:"text", text:...}]`, not a top-level prompt. The final video may be in `data.content.video_url` or the documented `data.video_url`; status must be succeeded.
- Native modules: Generate a Seedance video; Get a Seedance task; Make an API call.
- Categories: relevant AI/video/automation choices offered by the review form.
- Community logo: service-identifying asset only, with owner-confirmed rights. The form allows omitting a new logo when the service already has one in the directory. Do not use the Ace company logo as a substitute or assume third-party logo rights.
- API paths: `/seedance/videos` and `/seedance/tasks`; Connection GET `/v1/models`.
- Official install link / landing URL / cloud version: **pending**. GitHub source is not a public install URL.

[Common Make policy, duplicate-service rules, and irreversible publication gate](../suno/PUBLICATION.md#choose-the-permitted-public-path): technical review requires correct service classification, no conflicting integration, secret handling, universal module, fresh scenarios; Community allows multiple partner apps but requires current signed-partner eligibility and no default/roadmap conflict. Historical July2023 FAQ is not current approval. Name/brand/terms/indemnification are owner decisions, not accepted here.

The [live Community form](https://f.make.com/submit-your-app), checked 2026-10-19, requires a service-only app name (maximum 60 characters), a description of at most 200 characters, an existing signed partner agreement, real landing/invite/app IDs and consent to listing terms. Use the [current field worksheet](../COMMUNITY_SUBMISSION.md). The README ownership title is not a form app-name value.

## Private acceptance before submission

1. Assign an authorized separate existing/private Seedance app origin and actual zone/app/version/org/team; never reuse another service app's origin.
2. Deploy all three modules. Verify password-only Token input, correct case-sensitive choices, output interfaces and Authorization/internal-envelope log sanitization.
3. Run free Connection + universal GET and an error-only path. Separately run Get task against a task already owned by the account; do not include generation before the lookup.
4. With a current approved budget only, generate once and query that same ID until terminal; verify **Completed video URL**, media accessibility and unique usage record. No generation was requested by preparation of this packet.
5. Refresh each module's scenario logs immediately before review; retain sanitized scenario/execution IDs and exact source SHA. Test actual Make IML evaluation, since offline expression simulations do not prove it.
6. After approved publication, verify service-name directory search and separate-organization installation; do not count source/CI as market availability.

## Landing copy and tagged links

**Seedance video workflows in Make, provided by Ace Data Cloud.** Choose the service/model explicitly, submit once, then connect completed media to your automation. Bring your own token. Make operations and Ace API billing are separate.

- [Get API token](https://platform.acedata.cloud/console/applications?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=seedance_make_listing_api_key)
- [Current prices](https://platform.acedata.cloud/models?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=seedance_make_listing_pricing)
- Install button: pending real reviewed Make invite/listing URL.

Use the EN/ZH README as reviewable onboarding; screenshot provenance is [recorded](../suno/ASSET_SOURCES.md). Real Seedance Make screenshots, support/publisher contact, logo rights, invite/landing links, fresh scenarios and paid acceptance remain to supply. No account, agreement, new payment or permissions were created.
