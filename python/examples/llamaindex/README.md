# LlamaIndex: web search → extraction → cited retrieval

[中文](README.zh-CN.md)

Use the published Ace Data Cloud Python SDK with LlamaIndex `FunctionTool`,
`Document`, and `SimpleKeywordTableIndex`. This example retrieves passages with
their source URLs. It does not generate an answer or require an LLM/embedding key.
It is an Ace-maintained example, not an official LlamaIndex listing or built-in provider.

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

1. [Register or sign in](https://platform.acedata.cloud/?utm_source=llamaindex&utm_medium=example&utm_campaign=search-extraction).
2. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=llamaindex&utm_medium=example&utm_campaign=search-extraction), create an application if necessary, then create and copy its API credential.
3. Check your current service access, quota and pricing for
   [Google Search](https://platform.acedata.cloud/service/serp?utm_source=llamaindex&utm_medium=example&utm_campaign=search-extraction)
   and [WebExtrator](https://platform.acedata.cloud/service/webextrator?utm_source=llamaindex&utm_medium=example&utm_campaign=search-extraction).

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
See [task retrieval](https://platform.acedata.cloud/documents/webextrator-tasks?utm_source=llamaindex&utm_medium=example&utm_campaign=search-extraction).

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
