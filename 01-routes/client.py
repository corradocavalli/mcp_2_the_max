import asyncio
import os

import httpx
from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def call_tool(name: str):
    async with Client("http://localhost:8000/mcp") as client:
        # List all available tools, health_check is a custom route, not a tool so excluded
        all_tools = await client.list_tools()
        console.print(all_tools)

        # result = await client.call_tool("greet", {"name": name}) # excluded with tags
        result = await client.call_tool("cpu_usage", {})
        console.print(result, style="bold blue")

    # Call the custom /health route
    async with httpx.AsyncClient() as http_client:
        status = await http_client.get("http://localhost:8000/health")
        console.print(status.text, style="bold magenta")


os.system("clear")

asyncio.run(call_tool("Ford"))
