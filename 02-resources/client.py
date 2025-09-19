import asyncio
import os

from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def main():

    async with Client("http://localhost:8000/mcp") as client:

        # List all available resources
        all_resources = await client.list_resources()
        console.print(all_resources, style="bold green")
        console.print("-" * 80, style="white")

        # Read specific resources
        resource = await client.read_resource("data://app-status")
        console.print(resource[0].text, style="bold blue")

        # dynamic resource with parameter
        name = "corrado"
        resource = await client.read_resource(f"resource://{name}/details")
        console.print(resource, style="bold red")

        # generic resource
        resource = await client.read_resource("resource://system-status")
        console.print(resource, style="bold cyan")


asyncio.run(main())
