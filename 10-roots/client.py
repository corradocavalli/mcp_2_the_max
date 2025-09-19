import asyncio
import os

from fastmcp import Client
from fastmcp.client.roots import RequestContext
from rich.console import Console

os.system("clear")


# pass this to make roots dynamic
async def roots_callback(context: RequestContext) -> list[str]:
    console.print(f"Server requested roots (Request ID: {context.request_id})")
    return ["file:////Users/corradocavalli/Dev/Hackathon/fastmcp20/10-roots"]


# Define roots to be used by the client
roots = ["file:///Users/corradocavalli/Dev/Hackathon/fastmcp20/10-roots"]
client = Client("http://localhost:8000/mcp", roots=roots)

console = Console()


async def main():
    async with client:
        result = await client.call_tool("read_file", {"filename": "poem.txt"})
        console.print(result, style="bold blue")


os.system("clear")

asyncio.run(main())
