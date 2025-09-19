import asyncio
import os
from pathlib import Path

from fastmcp import Client
from fastmcp.client.roots import RequestContext
from rich.console import Console

console = Console()
console.clear()

current_dir = Path(__file__).parent.absolute()


# Root can also be provided through a callback to dynamically authorize them per request
async def roots_callback(context: RequestContext) -> list[str]:
    console.print(f"Server requested roots (Request ID: {context.request_id})")
    return [f"file://{current_dir}/roots"]


# Define roots to be used by the client - use current directory
roots = [f"file://{current_dir}"]


async def main():
    # Create the client specifying the roots the server can access
    async with Client("http://localhost:8000/mcp", roots=roots) as client:
        result = await client.call_tool("read_file", {"filename": "poem.txt"})
        console.print(result, style="bold blue")


asyncio.run(main())
