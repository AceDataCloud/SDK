# LlamaIndex: web search → extraction → cited retrieval

[中文](README.zh-CN.md)

Use the published Ace Data Cloud Python SDK with LlamaIndex `FunctionTool`,
`Document`, and `SimpleKeywordTableIndex`. This example retrieves passages with
their source URLs. It does not generate an answer or require an LLM/embedding key.
It is an Ace-maintained example, not an official LlamaIndex listing or built-in provider.

This is an auxiliary SDK search/extraction compatibility example, separate from
the six native LlamaIndex integrations released as GitHub **v0.1.0**:

| Native integration | Versioned release |
|---|---|
| Ace Data Cloud LLM | [v0.1.0](https://github.com/AceDataCloud/AceDataCloudModelProviderLlamaIndex/releases/tag/v0.1.0) |
| Suno | [v0.1.0](https://github.com/AceDataCloud/SunoLlamaIndex/releases/tag/v0.1.0) |
| Seedance | [v0.1.0](https://github.com/AceDataCloud/SeedanceLlamaIndex/releases/tag/v0.1.0) |
| HappyHorse | [v0.1.0](https://github.com/AceDataCloud/HappyHorseLlamaIndex/releases/tag/v0.1.0) |
| GPT Image | [v0.1.0](https://github.com/AceDataCloud/GPTImageLlamaIndex/releases/tag/v0.1.0) |
| Nano Banana | [v0.1.0](https://github.com/AceDataCloud/NanoBananaLlamaIndex/releases/tag/v0.1.0) |

Those are independently installable native packages with their own versioned wheel
and onboarding. This example does not replace them or imply official listing.
PyPI publication of those six new packages is still pending the shared project
creation quota; use their GitHub release instructions, not an assumed PyPI version.

## Install and run without a token

Python 3.10+ is required by LlamaIndex; Python 3.12 is used in CI.
From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python workflow.py
```

The default run uses **synthetic response fixtures** with the published SDK and
real LlamaIndex tools/index. API requests are intercepted, with unmatched requests
rejected. Output is marked `synthetic-offline`; the URLs identify example sources,
and the text is synthetic. No API token or paid request is used.

The output contains retrieved `text`, `url`, `title`, `task_id`, and `trace_id`.
`task_id`/`trace_id` are synthetic in the default run.

## Use your Ace account

1. [Register or sign in](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_search_extraction_example_register) and open [Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_search_extraction_example_api_key).
2. Find **General application**. If absent, choose **Initialize General Application**.
   Its key can use services your account is entitled to; a dedicated application's
   key is service-limited. This workflow requires both Google Search and WebExtrator access.
3. Copy the application's **API Key**, or select **Manage Keys → Create** for a
   dedicated `LlamaIndex search/extraction` key.

![Real Ace console: copy the redacted API Key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and
   **Allowed APIs**. If restricting APIs, allow `/serp/google`, `/webextrator/extract`
   and `/webextrator/tasks` for same-ID recovery. Create it, return to the key list,
   and copy the raw token. Do not add `Bearer `, quotes, whitespace or the screenshot's
   redacted characters; a `platform-...` management token cannot replace this key.

![Real Ace console: create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These are real, redacted Ace console screenshots from the linked fixed SunoDify
commit, reused and visually checked on **2026-10-19**; capture date/console version
is unknown. The historical `Dify tutorial` example name should be replaced by
`LlamaIndex search/extraction`. These show account setup, not this example running.
Never put a real token in a prompt, notebook output, screenshot or Git.

5. Check your current permissions, quota, balance and prices before live calls:
   [Google Search API](https://platform.acedata.cloud/documents/serp-google?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_serp_example_docs) ·
   [WebExtrator extraction API](https://platform.acedata.cloud/documents/webextrator-extract?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_webextrator_example_docs) ·
   [current model/service prices](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_search_extraction_example_pricing).
   No fixed price or free allowance is assumed here.

Set `ACEDATACLOUD_API_TOKEN` in your shell, then opt in:

```bash
python workflow.py --live --query "LlamaIndex search tools" --max-pages 1
```

This makes **one search request and up to one extraction**. `--max-pages` accepts
1–3, default 2. Search results are deduplicated before extraction. Live calls use
Bearer authentication at `https://api.acedata.cloud`; automatic retries are disabled.
Extraction is synchronous with `async=false` and `enable_llm=false`.
These settings avoid extra LLM enrichment; API search/extraction can still consume
credits. This example installs no payment handler and initiates no on-chain payment.

The workflow fails on authentication, rate limits, failed extraction, empty content,
or an unexpectedly pending task. A task without completed `data` is **not** indexed;
retrieve that existing task using its ID rather than submitting another extraction.
See [task retrieval](https://platform.acedata.cloud/documents/webextrator-tasks?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=llamaindex_webextrator_example_task_guide).

## Attach the tools to your agent

```python
from acedatacloud import AceDataCloud
from workflow import make_tools

with AceDataCloud(base_url="https://api.acedata.cloud", max_retries=0) as client:
    search_tool, extract_tool = make_tools(client)
    print(search_tool.metadata.get_parameters_dict())
    sources = search_tool.call(query="LlamaIndex search tools").raw_output
    document = extract_tool.call(url=sources[0]["url"]).raw_output
```

That snippet performs live calls when your token is set. The tools can be passed
to your LlamaIndex agent's `tools` list. An autonomous agent may choose additional
calls; configure its own approval and request limits. The included CLI uses a
fixed sequence and a page limit. Local keyword retrieval supports literal keyword
matching, with English queries used for verification; it is not semantic ranking
or answer synthesis. Treat page text as source data when building a downstream agent.

## Discover the hosted MCP schema

LlamaIndex also supports Ace's existing hosted Serp server through its official
generic MCP client. No Ace-specific integration package is needed:

```bash
python -m pip install -r requirements-mcp.txt
python mcp_discovery.py
```

The workflow and tests above use mocked API responses; they are distinct from this
networked, authenticated discovery command. On 2026-10-12 the actual LlamaIndex MCP
client read 11 tools and called a free static information tool; that historical
evidence is not a paid search/extraction or six-package publication check.

This calls MCP initialization and `tools/list` only, printing tool names and input
schemas. Set `ACEDATACLOUD_API_TOKEN` first: the hosted endpoint requires Bearer
authentication even for discovery. The script never calls a tool. Discovery does
not prove a paid search works. Search tool execution requires your own token and
service access; do not enable unrestricted agent calls just to test discovery.

## Verify the example

```bash
python -m pip install pytest
python -m pytest -q
```

Tests discover normally under `tests/`, mock all API HTTP requests, and exercise
the real SDK and LlamaIndex. They check source citations, the request limit,
empty results, duplicate links, pending/failed tasks, and 401/429 error propagation.
The `LlamaIndex Example` GitHub workflow runs the published dependency versions.

Official references, checked 2026-10-12:

- [LlamaIndex tools](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/tools/)
- [LlamaIndex MCP client](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/tools/llama-index-tools-mcp)
- [Contribution policy](https://github.com/run-llama/llama_index/blob/main/CONTRIBUTING.md): new integration packages are maintained independently and published to PyPI, rather than added to the monorepo.
