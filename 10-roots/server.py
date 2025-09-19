# LLM sampling allows MCP tools to request the client’s LLM to generate text based on provided messages. This is useful when tools need to leverage the LLM’s capabilities to process data, generate responses, or perform text-based analysis.


import asyncio

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError

mcp = FastMCP("SamplingDemo")


@mcp.tool
async def read_file(filename: str, ctx: Context) -> str:
    """Read the contents of a file."""
    all_roots = []
    try:
        all_roots = await ctx.list_roots()
    except Exception as e:
        print(f"Error listing roots: {e}")
        raise ToolError(
            "No roots available to read the file. Please specify them in client configuration."
        )

    for root in all_roots:
        print(f"Available root: {root}")

    file_uri = f"{all_roots[0].uri}/{filename}".replace("file://", "")
    print(f"Attempting to read file at: {file_uri}")

    text = ""
    with open(file_uri, "r") as f:
        text = f.read()
    return text


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
