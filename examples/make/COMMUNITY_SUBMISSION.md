# Current Make Community submission worksheet

Checked **2026-10-19** against the live [Community App Submission form](https://f.make.com/submit-your-app), which was open. This worksheet records required fields; it is not a submission, agreement acceptance, partner-status claim or public installation link.

## Current rules that affect these apps

The live form says **only official Make Partners with a signed Partnership Agreement** may submit. Do not infer partner eligibility from owning a Make account or from a private Custom App.

For **Name of your App**, the form requires the exact service name, excludes the developer company unless it is part of the official product name, and limits the name to 60 characters. The directory-name drafts below therefore use **Suno**, **Seedance**, **HappyHorse**, **GPT Image**, and **Nano Banana**. Put **provided by Ace Data Cloud** in accurate descriptions, the provider identity and the landing page. Do not paste a README ownership title such as “Suno by Ace Data Cloud” into this field.

The form limits the short description to **200 characters**. Its logo must illustrate the service; the owner is responsible for rights and permissions. The form says a new logo is unnecessary if the app already contains the suitable logo or the service already has a directory logo. Do not substitute the Ace company logo or assume third-party trademark rights.

These rules refine the more general [app naming guidance](https://developers.make.com/custom-apps-documentation/best-practices/naming-conventions/apps). The [Community FAQ](https://developers.make.com/custom-apps-documentation/community-apps/how-does-it-work) allows multiple partner apps for a service, but also has eligibility/default/roadmap conditions and identifies its policy as July 2023. Current account and application status must still be checked.

## Field-by-field packet

| Current form field | Prepared draft or exact remaining input |
| --- | --- |
| Company name | Unknown: use the legal name in the **existing signed** Make Partnership Agreement. Do not invent or sign an agreement. |
| Business contact name/email | Unknown: owner-approved contact for the actual application. Do not substitute a GitHub bot identity. |
| Support email | Unknown: owner-approved support address. |
| Name of your App | Exact service-only draft from the table below; final service/brand classification remains with Make. |
| Service website | Unknown pending classification: the form asks for the actual service product website. Distinguish the underlying service from the Ace integration/API site; do not misrepresent either. |
| Short description | One of the service-specific drafts below, each at most 200 characters. |
| App characteristics: Free / Paid | The form distinguishes a fee for the **integration itself** from underlying API costs. Confirm the actual licensing decision; do not treat a paid Ace API as proof that the integration is sold separately. |
| App landing page | Pending approved public page with capabilities, provider identity, API charges, support, installation method and licensing terms. The existing EN/ZH README is a reviewable starting point, not proof of a published Make install. |
| Invite link | Pending a real published invite-only Make app; do not substitute a GitHub source link. The form says this is for Make/Celonis review rather than direct display to users. |
| App ID | Pending the actual existing app identity from `https://<actual-zone>.make.com/apps/<actual-app-id>`. Never copy README examples as real values. |
| Documentation URL | The service's EN/ZH README at the exact reviewed source revision, followed by the released/main URL after merge. |
| API URL | The relevant API landing/documentation page from the service publication packet. The request origin is `https://api.acedata.cloud`; a route URL alone is not a product landing page. |
| App logo | Rights-confirmed service asset or existing service-directory logo; owner/Make decision required. |
| Categories/subcategories | Select only the choices offered by the actual form for music/audio, video or images and automation. No fabricated keywords or ranking claims. |
| How your app processes data | Draft below; authorized owner must validate it against the actual deployment and privacy notice. |
| Consent to Terms and conditions | **Not accepted.** The final form explicitly agrees to submission/listing terms. The authorized legal owner must complete any new acceptance; technical publishing authorization does not make a legal declaration true. |

### Service-name and short-description drafts

| Directory name draft | Short description draft |
| --- | --- |
| Suno | Generate Suno music with the integration provided by Ace Data Cloud. Bring your own API token and retrieve completed audio using the same task ID. |
| Seedance | Generate Seedance videos with the integration provided by Ace Data Cloud. Bring your own API token and retrieve completed video using the same task ID. |
| HappyHorse | Generate HappyHorse videos with the integration provided by Ace Data Cloud. Bring your own API token and retrieve completed video using the same task ID. |
| GPT Image | Generate GPT Image pictures with the integration provided by Ace Data Cloud. Bring your own API token and retrieve one completed image using the same task ID. |
| Nano Banana | Generate Nano Banana pictures with the integration provided by Ace Data Cloud. Bring your own API token and retrieve one completed image using the same task ID. |

### Data-processing draft for owner verification

The Make modules send the user's Ace Data Cloud application token and chosen request parameters over HTTPS to `api.acedata.cloud`. The connection reads the model list, the generation action submits one asynchronous task, and the lookup action reads that task ID. Generation prompts and the selected service/model parameters are processed by the Ace API. Make stores the connection and scenario execution data according to its own settings. Application code sanitizes Authorization and internal task-envelope fields in logs and maps only the documented task/status/media outputs for lookup. No separate developer licensing check or additional data-collection endpoint is implemented in this source.

This is a technical source description, **not** a legal claim that the API provider cannot access request data. The authorized owner must supply the applicable privacy/retention terms, support contact and service-rights confirmation; do not copy the form's example “no data accessible to the developer” wording when it is untrue.

## Existing account and partner inspection

1. Open the intended **existing** Make account through [login](https://www.make.com/en/login). Confirm account, actual zone, organization/team, Custom Apps access and existing five service apps before considering registration or another app.
2. Inspect existing Make Apps Editor configuration/credentials. The documented development scopes are `sdk-apps:read` and `sdk-apps:write`; reuse already authorized access. If the account lacks the required role or permissions, report the exact missing role instead of expanding access.
3. Check existing partner records, the partner manager and earlier submission/review threads. [Partner program](https://www.make.com/en/partners), [Community program](https://developers.make.com/custom-apps-documentation/community-apps/how-does-it-work), and the [live submission form](https://f.make.com/submit-your-app) are entry points, not proof of an active Ace agreement. No new account or agreement is created by this worksheet.
4. If Community eligibility is absent, inspect the [technical-review route](https://developers.make.com/custom-apps-documentation/app-review/request-app-review) and ask the relevant Make technical/partner contact which route fits the implemented Ace API integrations. Use existing discussions first; deduplicate before sending. Do not repeatedly resubmit or imply an agreement exists.

## Technical contact brief (prepared; not sent)

We maintain five separately deployable Make App projects for Suno, Seedance, HappyHorse, GPT Image and Nano Banana via the Ace Data Cloud API, with native parameter forms, application-token connections and same-ID asynchronous task retrieval. Source and validation are in [SDK PR #800](https://github.com/AceDataCloud/SDK/pull/800); no public Make listing or production installation is claimed.

Please confirm the supported submission path and service/provider classification for this implementation: technical app review or Community distribution under an existing eligible partner. We will use exact service-only directory names and identify Ace Data Cloud separately as the integration provider, consistent with the current form. We also seek the supported onboarding path for an **Ace Data Cloud** named LLM provider in Make AI Agents; a generic compatible connection is not being presented as a named/default provider.

Before sending, resolve the actual sender/partner identity, inspect earlier relevant correspondence, add the merged source permalink and real private-test evidence, and remove any claim not supported by that evidence. Do not accept a contract, assert trademark rights, buy a plan or send bulk marketing to progress this inquiry.
