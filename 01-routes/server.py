from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP(
    name="Routes Server",
    include_tags={"dev", "catalog"},  # Only expose these tagged components
    on_duplicate_tools="error",  # Handle duplicate registrations
    on_duplicate_resources="warn",
    on_duplicate_prompts="replace",
)


@mcp.tool(
    tags={"dev", "admin"},  # Note how tags can be used to filter tools
    annotations={
        "title": "Get cpu usage",
        "readOnlyHint": True,
        "openWorldHint": False,
        "idempotentHint": True,
    },
)
def cpu_usage() -> str:
    return "47%"


# This is a custom route, not a tool, can be used as an API endpoint
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Server is OK")


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
