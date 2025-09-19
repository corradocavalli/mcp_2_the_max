import asyncio

from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def my_progress_handler(
    progress: float, total: float | None, message: str | None
) -> None:
    if total is not None:
        percentage = (progress / total) * 100
        console.print(f"Progress: {percentage:.1f}% - {message or ''}")
    else:
        console.print(f"Progress: {progress} - {message or ''}")


async def main():
    # Create the client with the custom progress handler
    async with Client(
        "http://localhost:8000/mcp", progress_handler=my_progress_handler
    ) as client:

        # simple action
        console.print("Calling process_items tool...\n", style="bold green")
        result = await client.call_tool(
            "process_items", {"items": ["hi", "how", "are", "you", "?"]}
        )
        console.print(result, style="bold magenta")


asyncio.run(main())
