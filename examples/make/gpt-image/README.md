# GPT Image by Ace Data Cloud for Make

Use GPT Image in Make with your **Ace Data Cloud application API token**. This standalone app project provides **Generate a GPT Image image**, **Get a GPT Image task**, and **Make an API call**. Independent integration provided by Ace Data Cloud; no third-party official status or affiliation is claimed.

[简体中文](README.zh-CN.md) · [Current pricing](https://platform.acedata.cloud/models?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=gpt_image_make_readme_pricing)

## 1. Install the correct integration

**Official Make installation URL: pending.** This is an independently deployable source project, not a published Make app. After publication, use the real approved install link and verify the integration provider is **Ace Data Cloud**. A similarly named app by someone else is not this integration.

For an authorized private test, follow the [pairing guide](../README.md#set-up-a-private-testing-app) with this directory's `makecomapp.json`. Inspect existing apps first; reuse the intended existing GPT Image private app. Use a distinct app ID/origin from Suno, chat and the other service projects. Zone, remote app/version, organization/team and development credential remain unassigned; do not paste example values as real deployment facts.

![Official Make private-module picker reference](../suno/_assets/tutorial/make-official-module-picker.png)

Official Make Geocodify screenshot, downloaded 2026-10-17; original capture date/version unknown. It illustrates the real module picker and does not show GPT Image installed. [Screenshot provenance](../suno/ASSET_SOURCES.md).

## 2. Register, sign in and obtain a service-enabled API token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=gpt_image_make_readme_api_key), register/sign in, and initialize **General application** if it is absent.
2. Open General application or a GPT Image-enabled application. Copy its API key, or choose **Manage Keys → Create** for a separately named `Make GPT Image` key. Review expiration, usage limit, service access, balance and current pricing. Allowed APIs must cover `/openai/images/generations` for generation, `/openai/tasks` for task lookup, and the Connection's free `GET /v1/models`; do not broaden permissions blindly.

![Ace Applications: copy a key or open Manage Keys](../suno/_assets/tutorial/get-api-key-en.png)

![Ace key creation with restrictions](../suno/_assets/tutorial/create-api-key-en.png)

These are existing, credential-redacted Ace platform screenshots recovered 2026-10-18 from the pinned SunoDify guide; they are not Make installation evidence. The historical `Dify tutorial` key name is an example; use your own name.

3. In the installed Make app, click **Create a connection** and paste the raw value into **Ace Data Cloud API token**. Do not add `Bearer `, use a `platform-...` management token, or confuse it with the Make deployment key.
4. Save. Only the model-list GET runs for validation; this does not prove paid service access. Keep tokens out of prompts, blueprints, screenshots and universal-module custom headers.

## 3. Generate once and retrieve the same task

One generated image only: `n=1`, `response_format=url`, GPT Image 2 / 2.5 Flare / 2.5 Sunburst, explicit size and quality. No image editing, base64 output, partial-image preview, unrelated model or fallback. The task returns the image in `response.data[0].url` (Make index 1).

After checking the selected model's current restrictions/prices and obtaining an execution budget:

1. Add **Generate a GPT Image image** and configure the native fields below. Model, size/resolution, duration and quality are explicit choices, not silent substitutions. Example prompt: `A cute baby sea otter`. Verify model-specific constraints before running.

| Make field | Offered values / meaning |
| --- | --- |
| Image description | Describe one image. This first action creates one URL result; edits and base64 output are not exposed. |
| GPT Image model | GPT Image 2, GPT Image 2.5 Flare, GPT Image 2.5 Sunburst |
| Image size | Auto, 1024 × 1024, 1024 × 1536, 1536 × 1024 |
| Quality | Auto, Low, Medium, High |

2. Run creation **once**. It sends `/openai/images/generations` with `async=true`, no callback placeholder, no automatic model fallback or application-error retry, and returns `task_id`, `status=pending`, `success=false`. An accepted task is not finished media.
3. Add **Get a GPT Image task**. Map the creation module's **Task ID** with Make's variable picker; it posts `{"action":"retrieve","id":"<same-task-id>"}` to `/openai/tasks`. Query that ID in a lookup-only scenario if pending; do not replay the generation route.
4. Use **Completed image URL** only when **Status=succeeded** and **Terminal success=true**. The module requires: finished_at exists, response.success=true, exactly one data item has a URL. Pending/failed/unknown/string response envelopes and unsupported cardinality do not produce final media. Only safe task/trace/status fields and the media URL are mapped; internal request/user/credential data is not returned.
5. Check the one generation's usage record and current account package conversion; Make operation credits and Ace API Credits are separate. Scenario/transport replay may duplicate a billed request, so inspect [request history](https://platform.acedata.cloud/console/usages?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=gpt_image_make_readme_usages) before any resubmission.

## 4. Free verification and troubleshooting

Start with **Make an API call → GET /v1/models**. With a task already owned by your account, run **Get a GPT Image task** in a separate lookup-only scenario. No new generation is required for this check. HTTP POST task retrieval is a read operation; the generate module is billable.

| Symptom | Action |
| --- | --- |
| No official install link | Publication is pending; do not treat GitHub source as an installed/public app. |
| 401 / restricted credential | Check raw token, expiration, allowed APIs, service access, balance and usage limit. |
| 400 / unsupported choice | Check this service's exact model, case-sensitive resolution and allowed size/duration; do not copy another service's fields. |
| Pending / empty media | Query the same ID; a preview or green scenario is not terminal media success. |
| Failed / string or unexpected response | Inspect original task/trace; the app does not guess a success result or auto-generate again. |
| 429 / timeout / 5xx | Inspect request history before resubmitting. No automatic paid application-error retry is configured. |

## Development and publication

From the SDK repository root:

```bash
python3 scripts/validate_make_app.py --schema-root /path/to/vscode-apps-sdk --app-root examples/make/gpt-image
python3 -m unittest discover -s scripts/tests -v
```

All service projects use standard test discovery and official Make schemas. Limited offline IML-expression simulations are not Make's actual engine. No custom-IML enablement or extra permissions are required by the source. See [PUBLICATION.md](PUBLICATION.md) for brand, review, scenario, install and legal gates. No real account installation, official listing, generation/billing proof or conversion is claimed.
