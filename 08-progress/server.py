# LLM sampling allows MCP tools to request the client’s LLM to generate text based on provided messages.
# This is useful when tools need to leverage the LLM’s capabilities to process data, generate responses, or perform text-based analysis.


import asyncio

from fastmcp import Context, FastMCP

mcp = FastMCP("ProgressDemo")


@mcp.tool
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process a list of items with progress updates."""
    total = len(items)
    results = []

    for i, item in enumerate(items):
        # Report progress as we process each item
        await ctx.report_progress(progress=i, total=total)

        # Simulate processing time
        await asyncio.sleep(0.5)
        results.append(item.upper())

    # Report 100% completion
    await ctx.report_progress(progress=total, total=total)

    return {"processed": len(results), "results": results}


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
