import json

import httpx
import pytest
import respx
from workflow import DEMO_BASE, install_demo_routes, make_tools, run

from acedatacloud import AceDataCloud, AuthenticationError, RateLimitError


def test_search_extract_retrieve_keeps_citations_and_request_bound():
    with respx.mock(assert_all_mocked=True, assert_all_called=True) as router:
        install_demo_routes(router)
        with AceDataCloud(api_token="offline-demo", base_url=DEMO_BASE, max_retries=0) as client:
            passages = run(client, "LlamaIndex search tools", max_pages=1)
        assert len(router.calls) == 2
        search_body = json.loads(router.calls[0].request.content)
        assert search_body == {"query": "LlamaIndex search tools", "type": "search", "number": 10, "page": 1}
        assert json.loads(router.calls[1].request.content)["async"] is False
        assert json.loads(router.calls[1].request.content)["enable_llm"] is False
        assert passages
        assert passages[0]["url"].startswith("https://developers.llamaindex.ai/")
        assert passages[0]["task_id"] == "synthetic-demo-task"
        assert "source URLs" in passages[0]["text"]


def test_empty_search_makes_no_extraction_request():
    with respx.mock(assert_all_mocked=True) as router:
        router.post(f"{DEMO_BASE}/serp/google").respond(200, json={"organic": []})
        with AceDataCloud(api_token="offline-demo", base_url=DEMO_BASE, max_retries=0) as client:
            assert run(client, "nothing") == []
        assert len(router.calls) == 1


def test_search_deduplicates_links_and_ignores_non_web_sources():
    with respx.mock(assert_all_mocked=True) as router:
        router.post(f"{DEMO_BASE}/serp/google").respond(
            200,
            json={
                "data": {
                    "organic": [
                        {"link": "https://example.com/page#one"},
                        {"link": "https://example.com/page#two"},
                        {"link": "mailto:person@example.com"},
                    ]
                }
            },
        )
        with AceDataCloud(api_token="offline-demo", base_url=DEMO_BASE, max_retries=0) as client:
            search, _ = make_tools(client)
            assert search.call(query="example").raw_output == [
                {"url": "https://example.com/page", "title": "https://example.com/page"}
            ]


@pytest.mark.parametrize(
    "response",
    [
        {"success": True, "task_id": "existing-task"},
        {"success": True, "data": {"text": ""}},
        {"success": False, "data": {"text": "failed"}},
    ],
)
def test_pending_empty_or_failed_extraction_is_not_a_document(response):
    with respx.mock(assert_all_mocked=True) as router:
        router.post(f"{DEMO_BASE}/webextrator/extract").respond(200, json=response)
        with AceDataCloud(api_token="offline-demo", base_url=DEMO_BASE, max_retries=0) as client:
            _, extract = make_tools(client)
            with pytest.raises(ValueError):
                extract.call(url="https://example.com/page")
        assert len(router.calls) == 1


@pytest.mark.parametrize("status,error_type", [(401, AuthenticationError), (429, RateLimitError)])
def test_api_errors_keep_their_meaning_and_do_not_retry(status, error_type):
    with respx.mock(assert_all_mocked=True) as router:
        router.post(f"{DEMO_BASE}/serp/google").mock(
            return_value=httpx.Response(status, json={"error": {"message": "request rejected"}})
        )
        with AceDataCloud(api_token="offline-demo", base_url=DEMO_BASE, max_retries=0) as client:
            with pytest.raises(error_type):
                run(client, "example")
        assert len(router.calls) == 1
