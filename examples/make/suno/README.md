# Suno by Ace Data Cloud for Make

Create Suno music tasks in Make with your own **Ace Data Cloud** API token, then retrieve the **same task ID** until the audio is ready. This independent app project contains **Generate Suno music**, **Get a Suno task**, and **Make an API call**. It is provided by Ace Data Cloud; it is not an official Suno app or an affiliation claim.

[简体中文](README.zh-CN.md) · [Current API access and pricing](https://platform.acedata.cloud/models?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_readme_pricing) · [API documentation](https://platform.acedata.cloud/documents/suno-audios?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_readme_docs)

**Community directory name:** `Suno` under the current form's service-only naming rule; **provided by Ace Data Cloud** is the integration identity in the description/publisher page. This README title is not an approved directory label. [Submission rules checked 2026-10-19](../COMMUNITY_SUBMISSION.md).

## 1. Install the correct app

**Official Make installation link: pending.** This source project has not been deployed to a Make account, reviewed, or published. Do not install an unrelated search result because its name contains Suno. Once the approved link exists, check that the listing identifies **Ace Data Cloud** as the integration provider, install it into your intended organization, and add its module to a scenario.

Developers can prepare a private test installation with [the pairing instructions](../README.md#set-up-a-private-testing-app). Use this directory's `makecomapp.json`, inspect existing apps before creating another one, and set a separate Suno test origin. Never point the Suno manifest at the existing chat app: these are independently deployable app projects. No real app ID, zone, organization, or invite URL is currently assigned here.

![Official Make example of selecting a private module](./_assets/tutorial/make-official-module-picker.png)

Official Make reference screenshot, downloaded 2026-10-17; its capture date/version is not specified. It shows **Geocodify**, not an installed Ace or Suno app. It illustrates the real Make module picker; the app and module names will differ after installation. [Official source and image provenance](ASSET_SOURCES.md).

## 2. Register and get your Ace Data Cloud API token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_readme_api_key). Register/sign in. If **General application** is missing, choose **Initialize General Application**.
2. Open General application or your Suno-enabled application. Copy its API key, or select **Manage Keys → Create** for a separate `Make Suno` key. Review expiration, allowed APIs, usage limits, service access, and current balance/prices. Allow `/suno/audios` for generation and `/suno/tasks` for lookup; this Connection also validates through `GET /v1/models`, so restricted keys must allow that read. Do not expand a restricted key blindly.

![Copy an application API key or open Manage Keys](./_assets/tutorial/get-api-key-en.png)

![Create a separate API key with optional restrictions](./_assets/tutorial/create-api-key-en.png)

These credential-redacted platform screenshots come from the pinned [SunoDify guide](https://github.com/AceDataCloud/SunoDify/tree/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial), recovered 2026-10-18. They show Ace account setup, not Make installation.

3. In the installed Make Suno module, click **Create a connection** and paste the **raw token** into **Ace Data Cloud API token**. Do not add `Bearer ` or use a `platform-...` account-management token. The separate Make developer key is for deployment, not this Connection.
4. Save. Connection validation calls only `GET https://api.acedata.cloud/v1/models`. A valid token does not prove Suno generation access or sufficient balance. Never put the token in prompts, shared blueprints, screenshots, or request headers in the universal module.

## 3. Create once, query the same task

After the app has been installed and a generation budget approved:

1. Add **Generate Suno music**. Choose a supported Suno model explicitly after checking its current price (for example `chirp-v6` if your account supports it); enter a music description and choose **Instrumental only**. The request uses `/suno/audios`, `action=generate`, `custom=false`, and `async=true`. It submits one billed request and returns `task_id`, `status=pending`, `success=false`. This first version covers description-based generation; custom lyrics and advanced editing are not exposed.
2. Add **Get a Suno task**. In **Task ID**, use Make's variable picker to map **Generate Suno music → Task ID**. This sends `/suno/tasks` with `action=retrieve` and the same ID. It never submits generation. Save a second lookup-only scenario with that ID if further checks are needed; do not replay the creation route to poll.
3. Inspect **Status**, **Terminal success**, and **Completed audio URLs**. Only `status=succeeded` and `success=true` expose the final audio links. Pending previews, unfinished tasks, partial tracks, and failed tasks do not expose media through this output. Only then map the URL to a downstream file/download module. Check one matching generation usage record; Make operation credits and Ace API Credits are different units.

There is no automatic polling loop or automatic paid retry. You control the lookup schedule and its Make operation cost. This project uses Make's built-in expressions; it does not require the separately enabled custom IML-function feature. Static tests do not replace a run in Make.

## 4. Start with free verification

Before any paid action, run **Make an API call** with `GET /v1/models`. For an existing task that belongs to your account, run **Get a Suno task** once and inspect its output. Do not copy another user's task ID or run the generation module without a current budget. A historical successful task readback validates the API response shape, not this app's installation or new-generation billing.

## Troubleshooting

| What you see | What to check |
| --- | --- |
| No public install link | Publication is pending; use the developer pairing checklist only in an authorized private testing account. |
| Connection rejected / 401 / restricted key | Raw application token, expiration, `/v1/models` read permission, Suno API permissions, service access, usage limit, and balance. |
| Pending or no audio URLs | Query the same task ID later. A preview URL or accepted task is not a completed generation. |
| A string instead of the expected task response object | Stop and inspect the task contract. The module rejects unsupported envelopes rather than guessing success. |
| 429, timeout, 5xx, or ambiguous submission | No automatic application-error replay is configured. Inspect [request history](https://platform.acedata.cloud/console/usages?utm_source=make&utm_medium=integration&utm_campaign=evergreen&utm_content=suno_make_readme_usages) before submitting again; transport/scenario replay can still duplicate a paid request. |
| Failed task | Preserve task/trace ID for support; never include your token or private request data. |
| Media unavailable | Confirm all tracks reached `succeeded`, then check the returned URL from your Make/browser environment. |

## Development and publication

The app directory is independently deployable; the Community directory-name draft is **Suno**, with Ace Data Cloud identified separately as the integration provider. Its cloud app label and service/brand classification remain subject to Make's review. It is a single service app, not a renamed copy of the chat app. The repository owns one canonical copy of this project; no duplicate service repository is required to get a separate Make app identity.

From the SDK repository root:

```bash
python3 scripts/validate_make_app.py --schema-root /path/to/vscode-apps-sdk --app-root examples/make/suno
python3 -m unittest discover -s scripts/tests -v
```

CI uses the pinned official Make schema and standard test discovery. Connection/universal source is intentionally packaged locally because a standalone app needs its complete files; parity tests protect the shared credential/URL contract. The Suno base uses `RuntimeError` for 429 and 5xx to avoid configuring a paid generation replay. Read the [submission packet](PUBLICATION.md) before any public action. Publishing is irreversible, requires owner confirmations and fresh scenario evidence, and has not occurred.
