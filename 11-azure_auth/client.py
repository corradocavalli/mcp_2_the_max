import asyncio

from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def main():
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:

        all_tools = await client.list_tools()
        console.print(all_tools, style="bold green")

        # Test the protected tool
        result = await client.call_tool("get_user_info")
        console.print(result.content[0].text, style="bold blue")


asyncio.run(main())
