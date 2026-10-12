"""List hosted Serp tools with the official LlamaIndex MCP client; never call a tool."""

import asyncio
import json
import os

from llama_index.tools.mcp import BasicMCPClient


async def main() -> None:
    token = os.environ.get("ACEDATACLOUD_API_TOKEN")
    if not token:
        raise SystemExit("Set ACEDATACLOUD_API_TOKEN: hosted MCP discovery requires authentication.")
    headers = {"Authorization": f"Bearer {token}"}
    client = BasicMCPClient("https://serp.mcp.acedata.cloud/mcp", headers=headers, timeout=30)
    try:
        tools = await client.list_tools()
        print(json.dumps([tool.model_dump(by_alias=True) for tool in tools.tools], indent=2))
    finally:
        await client.http_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
