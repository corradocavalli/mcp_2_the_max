import asyncio
import logging
import os

import httpx
from fastmcp import Client
from fastmcp.client.logging import LogMessage
from rich.console import Console

os.system("clear")

# Get a logger for the module where the client is used
logger = logging.getLogger(__name__)

# This mapping is useful for converting MCP level strings to Python's levels
LOGGING_LEVEL_MAP = logging.getLevelNamesMapping()


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


client = Client("http://localhost:8000/mcp", log_handler=log_handler)

console = Console()


async def main():
    async with client:

        all_tools = await client.list_tools()
        console.print(all_tools, style="bold green")

        # user info tool
        # result = await client.call_tool("collect_user_info")
        # console.print(result, style="bold blue")

        # simple action
        result = await client.call_tool("analyze_data", {"data": [1, 2, 3, 4, 5]})
        console.print(result, style="bold magenta")


os.system("clear")

asyncio.run(main())
