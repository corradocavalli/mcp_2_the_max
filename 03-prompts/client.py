import asyncio
import os

import httpx
from fastmcp import Client
from rich.console import Console

os.system("clear")


client = Client("http://localhost:8000/mcp")

console = Console()


async def call_prompt(name: str):
    async with client:

        all_prompts = await client.list_prompts()
        console.print(all_prompts, style="bold green")

        prompt = await client.get_prompt("ask_about_topic", {"topic": "pizza"})
        console.print(prompt, style="bold blue")

        prompt = await client.get_prompt(
            "generate_code_request",
            {"language": "python", "task_description": "generate a random number"},
        )
        console.print(prompt, style="bold blue")


asyncio.run(call_prompt("Ford"))
