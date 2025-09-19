import asyncio

from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def main():
    async with Client("http://localhost:8000/mcp") as client:

        # Call a tool that internally uses Context to read a resource returning the request ID
        result = await client.call_tool("system_health_check")
        console.print(result, style="bold blue")


asyncio.run(main())
