import asyncio
import logging
import os

from fastmcp import Client
from rich.console import Console

os.system("clear")


async def my_progress_handler(
    progress: float, total: float | None, message: str | None
) -> None:
    if total is not None:
        percentage = (progress / total) * 100
        console.print(f"Progress: {percentage:.1f}% - {message or ''}")
    else:
        console.print(f"Progress: {progress} - {message or ''}")


client = Client("http://localhost:8000/mcp", progress_handler=my_progress_handler)

console = Console()


async def main():
    async with client:

        all_tools = await client.list_tools()
        console.print(all_tools, style="bold green")

        # simple action
        result = await client.call_tool(
            "process_items", {"items": ["hi", "how", "are", "you", "?"]}
        )
        console.print(result, style="bold magenta")


os.system("clear")

asyncio.run(main())
