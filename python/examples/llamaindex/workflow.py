"""Search, extract and retrieve cited passages with LlamaIndex; offline by default."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any
from urllib.parse import urldefrag, urlparse

import httpx
import respx
from llama_index.core import Document, SimpleKeywordTableIndex
from llama_index.core.llms import MockLLM
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool

from acedatacloud import AceDataCloud

API_BASE = "https://api.acedata.cloud"
DEMO_BASE = "https://offline.example.invalid"
DEMO_PAGES = {
    "https://developers.llamaindex.ai/python/framework/community/integrations/": {
        "title": "LlamaIndex integrations (synthetic demo)",
        "text": "LlamaIndex tools connect search and extraction APIs to a retrieval workflow. "
        "Documents preserve source URLs for citations.",
    },
    "https://developers.llamaindex.ai/python/framework/module_guides/mcp/": {
        "title": "LlamaIndex MCP (synthetic demo)",
        "text": "MCP discovery lists tool schemas without executing a search. "
        "A search tool call can use an authenticated API and consume account credits.",
    },
}


def source_url(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Expected an HTTP(S) source URL")
    url = urldefrag(value)[0]
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Expected an HTTP(S) source URL without credentials")
    return url


def make_tools(client: AceDataCloud) -> tuple[FunctionTool, FunctionTool]:
    def search(query: str) -> list[dict[str, str]]:
        """Search the web once; returns source URLs and titles. Consumes API credits in live mode."""
        if not query.strip():
            raise ValueError("Search query must not be empty")
        response = client.search.google(query=query, type="search", number=10, page=1)
        if response.get("success") is False:
            raise ValueError("Search returned an unsuccessful response")
        data = response.get("data", response)
        if not isinstance(data, dict) or not isinstance(data.get("organic"), list):
            raise ValueError("Search response must contain an organic result list")
        sources: list[dict[str, str]] = []
        seen: set[str] = set()
        for item in data["organic"]:
            if not isinstance(item, dict):
                continue
            try:
                url = source_url(item.get("link"))
            except ValueError:
                continue
            if url not in seen:
                sources.append({"url": url, "title": str(item.get("title", url))})
                seen.add(url)
        return sources

    def extract(url: str) -> Document:
        """Extract one page synchronously without LLM enrichment. Consumes API credits in live mode."""
        url = source_url(url)
        response = client.webextrator.extract(url=url, async_=False, enable_llm=False, timeout=30)
        if response.get("success") is False:
            raise ValueError("Extraction returned an unsuccessful response")
        data = response.get("data")
        if not isinstance(data, dict):
            task_id = response.get("task_id", "unknown")
            raise ValueError(f"No completed extraction body; retrieve existing task {task_id}. Do not resubmit.")
        text = data.get("markdown") or data.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Extraction returned no page text")
        metadata = {
            "url": source_url(data.get("finalUrl") or data.get("url") or url),
            "title": str(data.get("title") or url),
            "task_id": str(response.get("task_id", "")),
            "trace_id": str(response.get("trace_id", "")),
        }
        return Document(
            text=text,
            metadata=metadata,
            excluded_llm_metadata_keys=list(metadata),
            excluded_embed_metadata_keys=list(metadata),
        )

    return (
        FunctionTool.from_defaults(fn=search, name="ace_web_search"),
        FunctionTool.from_defaults(fn=extract, name="ace_web_extract"),
    )


def run(client: AceDataCloud, query: str, max_pages: int = 2) -> list[dict[str, str]]:
    if not 1 <= max_pages <= 3:
        raise ValueError("max_pages must be between 1 and 3")
    search, extract = make_tools(client)
    sources = search.call(query=query).raw_output[:max_pages]
    if not sources:
        return []
    documents = [extract.call(url=source["url"]).raw_output for source in sources]
    # Regex keyword retrieval needs neither a remote LLM nor embeddings.
    index = SimpleKeywordTableIndex.from_documents(
        documents,
        llm=MockLLM(),
        transformations=[SentenceSplitter(chunk_size=256, chunk_overlap=32, tokenizer=str.split)],
    )
    nodes = index.as_retriever(retriever_mode="simple", llm=MockLLM(), num_chunks_per_query=3).retrieve(query)
    return [{**node.node.metadata, "text": node.node.text} for node in nodes]


def install_demo_routes(router: respx.MockRouter) -> None:
    router.post(f"{DEMO_BASE}/serp/google").respond(
        200, json={"organic": [{"link": url, "title": page["title"]} for url, page in DEMO_PAGES.items()]}
    )

    def extract_response(request: httpx.Request) -> httpx.Response:
        url = json.loads(request.content)["url"]
        return httpx.Response(
            200,
            json={
                "success": True,
                "task_id": "synthetic-demo-task",
                "trace_id": "synthetic-demo-trace",
                "data": {"url": url, **DEMO_PAGES[url]},
            },
        )

    router.post(f"{DEMO_BASE}/webextrator/extract").mock(side_effect=extract_response)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="LlamaIndex search tools")
    parser.add_argument("--max-pages", type=int, choices=(1, 2, 3), default=2)
    parser.add_argument(
        "--live", action="store_true", help="Use your token: 1 search + up to max-pages paid extractions"
    )
    args = parser.parse_args()
    if args.live:
        token = os.environ.get("ACEDATACLOUD_API_TOKEN")
        if not token:
            parser.error("Set ACEDATACLOUD_API_TOKEN before --live")
        with AceDataCloud(api_token=token, base_url=API_BASE, max_retries=0) as client:
            passages = run(client, args.query, args.max_pages)
    else:
        with respx.mock(assert_all_mocked=True, assert_all_called=False) as router:
            install_demo_routes(router)
            with AceDataCloud(api_token="offline-demo", base_url=DEMO_BASE, max_retries=0) as client:
                passages = run(client, args.query, args.max_pages)
    print(json.dumps({"mode": "live" if args.live else "synthetic-offline", "passages": passages}, indent=2))


if __name__ == "__main__":
    main()
