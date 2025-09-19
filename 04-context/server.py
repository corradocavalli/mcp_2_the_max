# This server demonstrates the use of Context objects in FastMCP

import json

from fastmcp import Context, FastMCP
from fastmcp.server.dependencies import get_context  # Other way to access the context

mcp = FastMCP(name="Context-Server")


# Exposes a resource can accesses the context and returns the request ID
@mcp.resource("resource://system-status")
async def get_system_status(ctx: Context) -> dict:
    """Provides system status information."""
    return {"status": "operational", "request_id": ctx.request_id}


# A tool that uses the context to read an existing resource
@mcp.tool()
async def system_health_check(ctx: Context) -> dict:
    """Checks the health of the system."""
    status_resource = await ctx.read_resource("resource://system-status")
    content = status_resource[0].content
    return json.loads(content)


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
