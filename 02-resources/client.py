import asyncio
import os

import httpx
from fastmcp import Client
from rich.console import Console

os.system("clear")


client = Client("http://localhost:8000/mcp")

console = Console()


async def call_resource(name: str):
    async with client:

        all_resources = await client.list_resources()
        console.print(all_resources, style="bold green")

        resource = await client.read_resource("data://app-status")
        console.print(resource[0].text, style="bold blue")

        name = "corrado"
        resource = await client.read_resource(f"resource://{name}/details")
        console.print(resource, style="bold red")

        resource = await client.read_resource("resource://system-status")
        console.print(resource, style="bold cyan")


asyncio.run(call_resource("Ford"))
