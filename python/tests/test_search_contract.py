"""SERP search request contract tests."""

from unittest.mock import Mock

import pytest

from acedatacloud.resources.search import Search


def test_google_serializes_defaults_and_new_filters() -> None:
    transport = Mock()
    transport.request.return_value = {"organic_results": []}
    search = Search(transport)

    search.google(
        query="SDK examples",
        country="US",
        language="en",
        range="qdr:w",
        image_size="10mp",
    )

    assert transport.request.call_args.args == ("POST", "/serp/google")
    assert transport.request.call_args.kwargs["json"] == {
        "query": "SDK examples",
        "type": "search",
        "page": 1,
        "number": 10,
        "country": "US",
        "language": "en",
        "range": "qdr:w",
        "image_size": "10mp",
    }


def test_google_treats_legacy_none_page_as_the_default() -> None:
    transport = Mock()
    transport.request.return_value = {"organic_results": []}

    Search(transport).google(query="SDK examples", page=None)

    assert transport.request.call_args.kwargs["json"]["page"] == 1


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"query": "   "}, "query"),
        ({"query": "test", "page": 0}, "page"),
        ({"query": "test", "number": 101}, "number"),
        ({"query": "test", "country": ""}, "country"),
        ({"query": "test", "language": "x" * 33}, "language"),
        ({"query": "test", "range": "invalid"}, "range"),
        ({"query": "test", "image_size": "huge"}, "image_size"),
    ],
)
def test_google_rejects_invalid_contract_values(kwargs: dict[str, object], message: str) -> None:
    search = Search(Mock())

    with pytest.raises(ValueError, match=message):
        search.google(**kwargs)
