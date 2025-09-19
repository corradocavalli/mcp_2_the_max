import asyncio
import os

from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def main():
    async with Client("http://localhost:8000/mcp") as client:

        # List all available tools, note that some are excluded by tags
        all_tools = await client.list_tools()
        console.print(all_tools, style="bold green")
        console.print("-" * 80, style="white")

        # Call the greet_v2 tool
        console.print("Calling greet_v2 tool...", style="bold yellow")
        result = await client.call_tool("greet_v2", {"name": "Fred"})
        console.print(result, style="bold blue")

        # Call the search_products tool with parameters, note the structured output
        console.print("Calling search_products tool...", style="bold yellow")
        result = await client.call_tool(
            "find_products", {"query": "laptop", "category": "ai"}
        )
        console.print(result, style="bold blue")


os.system("clear")

asyncio.run(main())
