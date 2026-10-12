# LangChain chat with Ace Data Cloud

Ace Data Cloud's `/v1/chat/completions` endpoint works with LangChain's existing
[`ChatOpenAI`](https://docs.langchain.com/oss/python/integrations/chat/openai)
adapter. No separate package is needed for standard text, streaming, and tool
calling. `ChatOpenAI` only preserves standard OpenAI response fields; use a
provider-specific API when you need nonstandard fields or operations.

## Run

Use Python 3.10 or newer. Download the example and create a separate environment:

```bash
git clone https://github.com/AceDataCloud/SDK.git
cd SDK
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r examples/langchain/requirements.txt pytest
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in
PowerShell. The example pins `langchain-openai==1.7.0`; CI also checks 1.6.6.

Get an application API key from
[Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_langchain_readme_api_key).
Sign in or register, initialize **General application** if needed, and open
**Keys / Manage Keys → Create** to give this integration a separate key.
Check its service access, expiration, allowed APIs, usage limit, and balance.
Use the raw API key, without `Bearer `; a `platform-...` management token cannot
replace it. See the [illustrated key setup](../../README.md#get-your-ace-data-cloud-api-key).

From the SDK repository root, set the key and run one mode:

```bash
export ACEDATACLOUD_API_TOKEN='your Ace Data Cloud token'
python3 examples/langchain/chat.py 'Reply with one short sentence.'
```

Optional streaming and tool examples each submit additional requests:

```bash
python3 examples/langchain/chat.py --mode stream 'Count from one to three.'
python3 examples/langchain/chat.py --mode tools
```

In PowerShell, set the key with `$env:ACEDATACLOUD_API_TOKEN='your token'`.
The default model is `gpt-4o-mini`; set `ACEDATACLOUD_MODEL` to another model
available to your account in the
[model directory and current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_langchain_readme_pricing).
`ACEDATACLOUD_BASE_URL` defaults to
`https://api.acedata.cloud/v1` and can point to a local mock or staging endpoint.
Do not include `/chat/completions` in the base URL.

The example fixes `use_responses_api=False`, since some model names cause
LangChain to choose the Responses API. It sets `max_retries=0`, so an error is
not automatically submitted again. The `chat` and `stream` modes each make one
billable request; `tools` makes two (tool selection and the final answer). The
local `add_numbers` function has no external side effects. Any automatic retry
or agent loop you add can create more billable requests.

The example prints the API response ID and `usage_metadata` token counts when
available. Keep the response ID for troubleshooting. Token counts are not the
charged Credits; check the
[Usage History](https://platform.acedata.cloud/console/usages?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sdk_langchain_readme_usage) for the actual
charge. Streaming usage is off by default for compatibility. Use
`--mode stream --stream-usage` with a model that supports OpenAI's
`stream_options.include_usage` to request final token counts; if the service
does not return them, check Usage History.

The tool example should print `5` and report usage for its two API calls.
Text appears on stdout; response IDs and available token counts appear on stderr.

| Result | What to check |
| --- | --- |
| `401` | Token value and permissions. Pass the bare token; the adapter adds `Bearer`. |
| `403` | Balance, access, or content policy shown in the response. |
| `429` | Rate limit. Wait before an intentional retry. |
| `404` | Base URL must include `/v1`; confirm the model ID. |
| `5xx` or timeout | Check service status and Usage History before retrying an uncertain request. |

## Verify without a billable call

With `pytest` installed, run:

```bash
cd examples/langchain
python3 -m pytest -q
```

The tests use the installed LangChain and OpenAI SDK with a local HTTP mock.
They check URL, bearer authorization, Chat Completions request mode, response
and token usage parsing, streaming, tool round trip, and errors without making
a network request. They do not establish live account access, provider behavior,
or billing. Complete those checks with a valid token before claiming live
availability or seeking an upstream LangChain listing.
