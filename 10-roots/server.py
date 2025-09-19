# MCP roots define the base locations that a client authorizes a server to access.

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError

mcp = FastMCP("RootsServer")


# This tool uses the provided roots to identify the allowed file locations.
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

    # For simplicity, we just use the first root, we read the file relative to it.
    file_uri = f"{all_roots[0].uri}/{filename}".replace("file://", "")

    text = ""
    with open(file_uri, "r") as f:
        text = f.read()
    return text


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
