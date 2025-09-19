import asyncio

from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def main():
    async with Client("http://localhost:8000/mcp") as client:
        # List all available tools, both servers combined
        all_tools = await client.list_tools()
        console.print(all_tools, style="bold green")
        console.print("-" * 80, style="white")

        # Call tools from main server
        result = await client.call_tool("get_stock", {"stock_id": "MSFT"})
        console.print(result, style="bold blue")

        # Call tools from imported server, note how the tool name is prefixed with "weather" as indicated in server.py
        result = await client.call_tool(
            "weather_get_forecast", {"city": "London"}
        )  # weather is prefixed
        console.print(result, style="bold blue")


asyncio.run(main())
