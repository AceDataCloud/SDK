"""Minimal LangChain chat call through AceDataCloud's OpenAI-compatible API."""

import os
import sys

from langchain_openai import ChatOpenAI


def main() -> None:
    token = os.environ["ACEDATACLOUD_API_TOKEN"]
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Reply with one short sentence."
    model = ChatOpenAI(
        model=os.environ.get("ACEDATACLOUD_MODEL", "gpt-5.5"),
        api_key=token,
        base_url=os.environ.get("ACEDATACLOUD_BASE_URL", "https://api.acedata.cloud/v1"),
        use_responses_api=False,
        stream_usage=False,
        max_retries=0,
        timeout=60,
    )
    response = model.invoke([("user", prompt)])
    print(response.content)


if __name__ == "__main__":
    main()
