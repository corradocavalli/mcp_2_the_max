import asyncio

from fastmcp import Client
from rich.console import Console

console = Console()
console.clear()


async def progress_handler(
    progress: float, total: float | None, message: str | None
) -> None:
    if total is not None:
        percentage = (progress / total) * 100
        console.print(f"Progress: {percentage:.1f}% - {message or ''}")
    else:
        console.print(f"Progress: {progress} - {message or ''}")


async def cancel_after_delay(client, request_id, delay=3):
    """Background task to cancel execution after a delay."""
    await asyncio.sleep(delay)
    console.print(f"Cancelling execution after {delay} seconds...", style="bold red")
    # Cancel the specific request using its ID
    await client.cancel(request_id)


async def main():
    async with Client(
        "http://localhost:8000/mcp", progress_handler=progress_handler
    ) as client:

        console.print("Client connected", style="bold green")

        # Get the request ID that will be used for the next call
        # This is necessary for cancellation
        executing_request_id = client.session._request_id
        console.print(
            f"Next execution request ID: {executing_request_id}", style="bold green"
        )

        # Start the cancellation task in the background
        cancel_task = asyncio.create_task(
            cancel_after_delay(client, executing_request_id, delay=3)
        )

        console.print("Starting long_execution tool...", style="bold green")

        try:
            # Call the tool in the main thread - this will block until completion or cancellation
            result = await client.call_tool("long_execution", {"count": 10})
            console.print(f"Tool completed: {result}", style="bold magenta")

            # Cancel the background cancellation task since we completed successfully
            cancel_task.cancel()

        except Exception as e:
            console.print(f"Tool error ({type(e).__name__}): {e}", style="bold red")

        # Clean up the cancel task if it's still running
        if not cancel_task.done():
            cancel_task.cancel()
            try:
                await cancel_task
            except asyncio.CancelledError:
                pass


asyncio.run(main())
