# Make release readiness

Prepared 2026-10-12. This is a submission worksheet, not evidence of installation or publication.

## Distribution decision

| Route | Required evidence | Current state |
| --- | --- | --- |
| Private testing | Paired origin, deployed components, target organization/team, connection and executed scenarios | Pending Make account/origin |
| Public app review | All private tests, fresh scenario links/logs, API docs, publisher contacts, categories/logo, trademark and service-policy confirmations | Not submitted |
| Community App | Current signed-partner eligibility, published invite-only app, working invite link, developer landing page and business review | Eligibility and submission unverified |

The [public review flow](https://developers.make.com/custom-apps-documentation/app-review/request-app-review) requires publishing before requesting review. Publishing cannot be undone and public components cannot simply be deleted. An authorized publisher must approve the route and complete all legal confirmations before publication. The [Community FAQ](https://developers.make.com/custom-apps-documentation/community-apps/how-does-it-work) is based on July 2023 policy; its historical review-time estimate is not a current commitment.

## Private scenario acceptance

Use synthetic prompts and non-sensitive outputs. Do not share credentials, full request headers, or customer data. Keep the chat route separate from error tests to avoid accidental reruns.

| Check | Expected result | Evidence to fill |
| --- | --- | --- |
| Origin/deploy | Correct Make zone, app ID/version and both modules visible in the intended organization | App URL, deployed source SHA, organization/team reference |
| Valid Connection | Free `GET /v1/models`, HTTP 200 and `object=list` | Connection validation time; no token value |
| Universal GET | `/v1/models` returns `statusCode=200`, `body.data` and response headers | Scenario URL, execution ID, sanitized output |
| Invalid Connection | Fake token rejected; no generation request | Separate error scenario/log URL |
| Universal error | Invalid GET path displays the upstream error | Separate error scenario/log URL |
| Chat Action | One short request with an authorized current text-chat model; reply, completion ID, model and token usage mapped | Scenario URL, execution ID, sanitized output |
| Billing | Exactly one matching usage record for the accepted chat execution; token count separated from Credits and USD | Usage record reference, Credits, current account package rate |
| Secrets | Authorization redacted in valid and error logs; no credentials in parameters, screenshots or blueprints | Redacted inspection record |
| New organization | Invite/listing installation succeeds for a separate eligible organization | Install URL and scenario result |

The [official prerequisites](https://developers.make.com/custom-apps-documentation/app-review/prerequisites) require each module in at least one scenario and an error scenario. Run them immediately before review and after each review fix because Make execution logs expire. Static schemas do not verify IML evaluation or retry behavior.

## Reviewer form draft

- **App:** AceDataCloud.
- **Proposed category:** AI, subject to the categories offered by the current form.
- **Description:** Connect Make scenarios to AceDataCloud using your own API token. Create a text chat completion with reply and token-usage outputs, or make an authorized API call.
- **Service website:** <https://acedata.cloud/>.
- **API documentation:** <https://docs.acedata.cloud/>; verify the exact chat reference page in the active docs navigation before submission.
- **Source and instructions:** <https://github.com/AceDataCloud/SDK/tree/codex/make-chat-poc-20261006/examples/make>. Use the deployed commit permalink in the actual submission.
- **Pricing explanation:** Make operation/credit charges and AceDataCloud API charges are separate. Chat uses current model pricing and the customer's current account package rate. A connection test or model-list request does not prove paid model access.
- **Owner to supply:** Relationship to AceDataCloud, partnership and support contacts, approved logo/trademark rights, app ID/zone, install/landing-page URL and fresh scenario links. No identity or contact is invented here.
- **Owner-only confirmations:** Trademark permissions, compliance with relevant external-service terms, indemnification, and any partner agreement. Drafting this worksheet does not accept them.

## Acquisition and attribution

The README API-key link uses `utm_source=make`, `utm_medium=integration`, `utm_campaign=evergreen`, and `utm_content=make_readme_api_key`. For a future Make landing page, use `make_listing_api_key` as the content value and keep the same source/medium/campaign.

Before claiming conversion, verify landing-page arrival, persisted registration source, application/key creation, Make connection, successful scenario execution, and the matching usage record. A GitHub commit, link click, package download or listing view is insufficient evidence of the whole funnel. The current project has no Make-hosted attribution or conversion evidence.
