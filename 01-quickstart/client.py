import asyncio
import os

import httpx
from fastmcp import Client
from rich.console import Console

client = Client("http://localhost:8000/mcp")

console = Console()


async def call_tool(name: str):
    async with client:

        all_tools = await client.list_tools()
        console.print(all_tools, style="bold green")

        # result = await client.call_tool("greet", {"name": name}) # excluded with tags
        result = await client.call_tool("greet_v2", {"name": name})
        console.print(result, style="bold blue")

    async with httpx.AsyncClient() as http_client:
        status = await http_client.get("http://localhost:8000/health")
        console.print(status.text, style="bold magenta")


os.system("clear")

asyncio.run(call_tool("Ford"))
