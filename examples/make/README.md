# AceDataCloud for Make

This directory is a source-controlled [Make Apps Editor local app](https://developers.make.com/custom-apps-documentation/get-started/make-apps-editor/apps-sdk/local-development-for-apps), with a Basic Connection, **Create a chat completion** action, and **Make an API call** universal module. The app calls only `https://api.acedata.cloud`.

**Current state:** The local components have not been installed in a Make account or run in a Make scenario. `makecomapp.json` has no origin until a Make developer pairs it with a private custom app. This is an Apps Editor project, not a Make scenario blueprint or a public listing.

## Set up a private testing app

1. In the intended Make organization and zone, create a **private Custom App** with an available ID such as `acedatacloud`, label **AceDataCloud**, and version 1. Keep it private during testing.
2. Create a Make API key with `sdk-apps:read` and `sdk-apps:write` scopes. Save it only to `examples/make/.secrets/apikey`; that directory is git-ignored. Install and configure the [Make Apps Editor for VS Code](https://developers.make.com/custom-apps-documentation/get-started/make-apps-editor/apps-sdk/configuration-of-vs-code) for the same zone. This key is for deploying the app, not for connecting to AceDataCloud.
3. Add an origin to `makecomapp.json` using the actual Make zone and app ID. The app must already exist in Make. For example, after replacing the values with your own:

   ```json
   "origins": [{
     "label": "Testing",
     "baseUrl": "https://us1.make.com/api",
     "appId": "acedatacloud",
     "appVersion": 1,
     "apikeyFile": ".secrets/apikey"
   }]
   ```

4. Open this directory in VS Code. Right-click `makecomapp.json` and choose **Deploy to Make (beta)**. Select the testing origin and confirm creation of the Connection and both modules. Review their labels, code, output interfaces, and Base in Make's editor. [Make documents this deployment flow](https://developers.make.com/custom-apps-documentation/get-started/make-apps-editor/apps-sdk/local-development-for-apps/deploy-changes-from-local-app-to-make-app); the local development feature is beta, so use the editor's validation and inspect the installed version.
5. Create an AceDataCloud connection inside Make. Enter only the raw AceDataCloud API token in the password field, without a `Bearer ` prefix. The connection sends a free `GET /v1/models` request to validate the token. This check establishes token validity; it does not prove that a specific chat model is enabled or funded.

If a script or agent will create, run, and inspect the test scenario through the Make API, its Make token also needs `connections:read`, `connections:write`, `scenarios:read`, `scenarios:write`, and `scenarios:run`. The `sdk-apps` scopes alone cover only app development. The user or agent also needs access to the target Make team and its team ID.

The Connection token is stored by Make and omitted from this repository. Both Base and Connection sanitize the Authorization header in Make request logs. Do not put either token in scenario fields, shared blueprints, screenshots, or support tickets.

## Verify in Make

Use a token authorized for chat with a small available balance and a model ID available to that account. In a private scenario:

1. Run **Make an API call** with `GET` and `/v1/models`. Confirm the module returns HTTP 200 and a `body.data` list. This request is not billable.
2. Run **Create a chat completion** once with a short prompt and a current chat model ID. Confirm the output has a completion ID, reply, model, and token usage. The action makes exactly one non-streaming `POST /v1/chat/completions` request per execution. Make's IML arrays start at 1, so the first choice is mapped as `body.choices[1]`.
3. In AceDataCloud's usage history, match that completion's time/model and confirm one charge for the one run. The returned `total_tokens` is a token count, **not** a monetary cost. The cost depends on the current model prices and account package rate.
4. For a non-billable error check, use an invalid token when creating a separate Make connection and confirm it is rejected. Optionally call an invalid GET path with the universal module and confirm the error is visible. Inspect Make's execution log to ensure Authorization is redacted.

Do not submit a public review until the installed app, connection, scenario output, charge, and redacted logs have been inspected. Record the Make app ID/zone, scenario URL and execution ID, sanitized output, and usage-history reference in the PR or an internal run record.

## Error, retry, and billing behavior

- `401` is a connection/token error; update the Make Connection. `429` retains Make's rate-limit delay and retry behavior.
- Other API errors, including `5xx`, use `RuntimeError` so Make does not apply its `ConnectionError` retry/backoff to an ambiguous **billable** chat request. A transport failure or a scenario-level replay can still repeat a call. Check the Make execution and AceDataCloud usage history before manually rerunning or resuming a scenario.
- The universal module accepts a relative path under `https://api.acedata.cloud`. Its `GET /v1/models` example is free; other paths and write methods may incur charges. Do not add credentials in its custom Headers field.
- Model IDs and prices change. Keep the model input mappable and consult the current [AceDataCloud chat model catalog with pricing](https://platform.acedata.cloud/api/v1/models/?type=chat&with_pricing=true) and usage history. `/v1/models` can include models unsuitable for text chat, so it is not used as an unfiltered dropdown.

## Maintain and publish

Update these source files, deploy to a private testing app, and rerun the connection, safe GET, and one chat scenario before deploying to any shared/public version. Keep the local project and Make origin in sync with **Pull All Components from Make** when changes are made in Make's web editor. Never commit `.secrets` or connection data.

Make's [public app review prerequisites](https://developers.make.com/custom-apps-documentation/app-review/prerequisites) require a universal module, correct interfaces, secret sanitization, error handling, and fresh test scenario logs. After those checks, a public app can be [submitted for Make review](https://developers.make.com/custom-apps-documentation/app-review/request-app-review). A [Community App](https://developers.make.com/custom-apps-documentation/community-apps/how-does-it-work) follows a separate submission process. Public publishing creates an install link and cannot simply be reverted to private, so confirm the desired distribution path before publishing. Verify discoverability with the actual install link or listing and a separate organization install.
