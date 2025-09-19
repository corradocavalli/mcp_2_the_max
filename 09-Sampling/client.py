import asyncio
import os

from fastmcp import Client
from fastmcp.client.sampling import RequestContext, SamplingMessage, SamplingParams
from rich.console import Console

os.system("clear")


async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext,
) -> str:

    console.print("Received list of SamplingMessage objects:", style="bold yellow")
    console.print(messages, style="bold green")
    console.print(params, style="bold blue")

    # Discriminate by message content, role, etc.
    for msg in messages:
        console.print(f"Message type: {type(msg)}", style="bold cyan")
        if hasattr(msg, "role"):
            console.print(f"Role: {msg.role}", style="bold cyan")
        if hasattr(msg, "content"):
            console.print(f"Content: {msg.content}", style="bold cyan")

    return "This is a sample response from the client's LLM."


client = Client("http://localhost:8000/mcp", sampling_handler=sampling_handler)

console = Console()


async def main():
    async with client:

        # simple action
        result = await client.call_tool("creative_writing", {"topic": "Switzerland"})
        console.print(result, style="bold magenta")


os.system("clear")

asyncio.run(main())
