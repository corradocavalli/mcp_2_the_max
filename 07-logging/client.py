import asyncio
import logging

from fastmcp import Client
from fastmcp.client.logging import LogMessage
from rich.console import Console

# Get a logger for the module where the client is used
logger = logging.getLogger(__name__)

# This mapping is useful for converting MCP level strings to Python's levels
LOGGING_LEVEL_MAP = logging.getLevelNamesMapping()

console = Console()
console.clear()


async def log_handler(message: LogMessage):
    """
    Handles incoming logs from the MCP server and forwards them
    to the standard Python logging system.
    """
    msg = message.data.get("msg")
    extra = message.data.get("extra")

    # Convert the MCP log level to a Python log level
    level = LOGGING_LEVEL_MAP.get(message.level.upper(), logging.INFO)

    # Log the message using the standard logging library
    logger.log(level, msg, extra=extra)
    console.print(
        f"[bold blue]{message.level.upper()}[/bold blue] [bold red]{msg}[/bold red]"
    )


async def main():
    # Create the client with the custom log handler that will collect logs from the server
    async with Client("http://localhost:8000/mcp", log_handler=log_handler) as client:

        # Call the tool, generated logs will be forwarded to the log_handler
        result = await client.call_tool("analyze_data", {"data": [1, 2, 3, 4, 5]})
        console.print("\nResponse from the tool:", style="bold blue")
        console.print(result, style="bold magenta")


asyncio.run(main())
