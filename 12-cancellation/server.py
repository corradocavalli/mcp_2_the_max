import asyncio

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError

mcp = FastMCP(name="CancellationServer")


# Basic prompt returning a string (converted to user message automatically)
@mcp.tool
def short_execution(topic: str, ctx: Context) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"'{topic}' requested with request_id: {ctx.request_id}"


# Long-running operation simulation with progress reporting and cancellation support
@mcp.tool
async def long_execution(count: int, ctx: Context) -> str:
    """Generates a user message asking for a long-running operation."""
    try:
        for i in range(count):
            await ctx.report_progress(progress=i, total=count)
            await asyncio.sleep(1)

        return f"Completed long-running operation with {count} steps."
    except Exception as e:
        print(f"long_execution was cancelled after {i} steps out of {count}")
        return f"Long execution was cancelled after {i} steps out of {count}"


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
