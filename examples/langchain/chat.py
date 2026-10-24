"""Call Ace Data Cloud Chat Completions with LangChain's ChatOpenAI."""

import argparse
import json
import os
import sys

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

BASE_URL = "https://api.acedata.cloud/v1"
DEFAULT_MODEL = "gpt-4o-mini"
ADD_TOOL = {
    "type": "function",
    "function": {
        "name": "add_numbers",
        "description": "Add two integers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        },
    },
}


def build_model(*, stream_usage: bool = False, **client_options) -> ChatOpenAI:
    token = os.environ.get("ACEDATACLOUD_API_TOKEN")
    if not token:
        raise SystemExit("Set ACEDATACLOUD_API_TOKEN before running this example.")
    return ChatOpenAI(
        model=os.environ.get("ACEDATACLOUD_MODEL", DEFAULT_MODEL),
        api_key=token,
        base_url=os.environ.get("ACEDATACLOUD_BASE_URL", BASE_URL),
        use_responses_api=False,
        stream_usage=stream_usage,
        max_retries=0,
        timeout=60,
        **client_options,
    )


def show_usage(message) -> None:
    response_id = message.response_metadata.get("id")
    if response_id:
        print(f"response id: {response_id}", file=sys.stderr)
    usage = message.usage_metadata
    if usage:
        print(f"tokens: {json.dumps(usage, sort_keys=True)}", file=sys.stderr)
    else:
        print(
            "token usage unavailable; check Usage History for the charge",
            file=sys.stderr,
        )


def run_chat(model: ChatOpenAI, prompt: str) -> None:
    reply = model.invoke([HumanMessage(content=prompt)])
    print(reply.content)
    show_usage(reply)


def run_stream(model: ChatOpenAI, prompt: str) -> None:
    complete = None
    for chunk in model.stream([HumanMessage(content=prompt)]):
        if isinstance(chunk.content, str):
            print(chunk.content, end="", flush=True)
        complete = chunk if complete is None else complete + chunk
    print()
    if complete is not None:
        show_usage(complete)


def run_tools(model: ChatOpenAI) -> None:
    messages = [
        HumanMessage(content="Use add_numbers to add 2 and 3, then report the sum.")
    ]
    tool_reply = model.bind_tools([ADD_TOOL], tool_choice="required").invoke(messages)
    if not tool_reply.tool_calls:
        raise RuntimeError("The model returned no tool call.")
    show_usage(tool_reply)
    messages.append(tool_reply)
    for call in tool_reply.tool_calls:
        if call["name"] != "add_numbers":
            raise RuntimeError(f"Unexpected tool: {call['name']}")
        args = call["args"]
        result = int(args["a"]) + int(args["b"])
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    final = model.invoke(messages)
    print(final.content)
    show_usage(final)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", default="Reply with one short sentence.")
    parser.add_argument("--mode", choices=("chat", "stream", "tools"), default="chat")
    parser.add_argument(
        "--stream-usage",
        action="store_true",
        help="Request a final token usage chunk when streaming (model support varies).",
    )
    args = parser.parse_args()
    model = build_model(stream_usage=args.stream_usage)
    if args.mode == "chat":
        run_chat(model, args.prompt)
    elif args.mode == "stream":
        run_stream(model, args.prompt)
    else:
        run_tools(model)


if __name__ == "__main__":
    main()
