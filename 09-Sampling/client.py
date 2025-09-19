import asyncio

from fastmcp import Client
from fastmcp.client.sampling import RequestContext, SamplingMessage, SamplingParams
from rich.console import Console

console = Console()
console.clear()


async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext,
) -> str:
    console.print("-" * 80, style="white")
    console.print("\nReceived list of SamplingMessage objects:", style="bold cyan")
    console.print(messages, style="bold green")
    console.print(params, style="bold blue")
    console.print("-" * 80, style="white")

    # Discriminate by message content, role, etc.
    for msg in messages:
        console.print(f"Message type: {type(msg)}", style="bold cyan")
        if hasattr(msg, "role"):
            console.print(f"Role: {msg.role}", style="bold cyan")
        if hasattr(msg, "content"):
            console.print(f"Content: {msg.content}", style="bold cyan")

    return "This is a sample response from the client's LLM."


async def main():
    # Create the client with the custom sampling handler
    async with Client(
        "http://localhost:8000/mcp", sampling_handler=sampling_handler
    ) as client:

        # simple action
        console.print("Calling creative_writing tool...", style="bold cyan")
        result = await client.call_tool("creative_writing", {"topic": "Switzerland"})
        console.print(result, style="bold magenta")


asyncio.run(main())
