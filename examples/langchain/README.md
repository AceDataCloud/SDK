# LangChain chat with Ace Data Cloud

Ace Data Cloud's `/v1/chat/completions` endpoint works with LangChain's existing
[`ChatOpenAI`](https://docs.langchain.com/oss/python/integrations/chat/openai)
adapter. No separate package is needed for standard text, streaming, and tool
calling. `ChatOpenAI` only preserves standard OpenAI response fields; use a
provider-specific API when you need nonstandard fields or operations.

## Run

```bash
python3 -m pip install 'langchain-openai>=1.6,<2'
export ACEDATACLOUD_API_TOKEN='your Ace Data Cloud token'
python3 examples/langchain/chat.py 'Reply with one short sentence.'
python3 examples/langchain/chat.py --mode stream 'Count from one to three.'
python3 examples/langchain/chat.py --mode tools
```

Run these commands from the SDK repository root. Get a token from the
[Ace Data Cloud console](https://platform.acedata.cloud/console/applications).
The default model is `gpt-4o-mini`; set `ACEDATACLOUD_MODEL` to another model
available to your account. `ACEDATACLOUD_BASE_URL` defaults to
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
[Usage History](https://platform.acedata.cloud/console/usages) for the actual
charge. Streaming usage is off by default for compatibility. Use
`--mode stream --stream-usage` with a model that supports OpenAI's
`stream_options.include_usage` to request final token counts; if the service
does not return them, check Usage History.

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
python3 -m pytest examples/langchain/test_chat.py -q
```

The tests use the installed LangChain and OpenAI SDK with a local HTTP mock.
They check URL, bearer authorization, Chat Completions request mode, response
and token usage parsing, streaming, tool round trip, and errors without making
a network request. They do not establish live account access, provider behavior,
or billing. Complete those checks with a valid token before claiming live
availability or seeking an upstream LangChain listing.
