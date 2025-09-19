import asyncio
import os

from fastmcp import Client
from rich.console import Console

os.system("clear")


client = Client("http://localhost:8000/mcp")

console = Console()


async def call_tool(name: str):
    async with client:

        all_tools = await client.list_tools()
        console.print(all_tools, style="bold green")

        result = await client.call_tool("get_stock", {"stock_id": "MSFT"})
        console.print(result, style="bold blue")

        result = await client.call_tool(
            "weather_get_forecast", {"city": "London"}
        )  # weather is prefixed
        console.print(result, style="bold blue")


os.system("clear")

asyncio.run(call_tool("Ford"))
