import asyncio
import os

import httpx
from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def main():
    async with Client("http://localhost:8000/mcp") as client:

        all_prompts = await client.list_prompts()
        console.print(all_prompts, style="bold green")
        console.print("-" * 80, style="white")

        # Get specific prompts
        prompt = await client.get_prompt("ask_about_topic", {"topic": "pizza"})
        console.print(prompt, style="bold blue")

        prompt = await client.get_prompt(
            "conversation_prompt",
            {"character": "Ford", "situation": "a time traveler from the future"},
        )
        console.print(prompt, style="bold blue")


asyncio.run(main())
