# A Resource is data (read-only) exposed by the server for the LLM or client application.


from fastmcp import Context, FastMCP

mcp = FastMCP(name="DataServer")


# Basic dynamic resource returning a string
@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """Provides a simple greeting message."""
    return "Hello from MCP Resource!"


# Resource returning JSON data (dict is auto-serialized)
@mcp.resource(
    "data://config", annotations={"readOnlyHint": True, "idempotentHint": True}
)
def get_config() -> dict:
    """Provides application configuration as JSON."""
    return {
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "inspect"],
    }


# Example specifying metadata
@mcp.resource(
    uri="data://app-status",  # Explicit URI (required)
    name="ApplicationStatus",  # Custom name
    description="Provides the current status of the application.",  # Custom description
    mime_type="application/json",  # Explicit MIME type
    tags={"monitoring", "status"},  # Categorization tags
    meta={"version": "2.1", "team": "infrastructure"},  # Custom metadata
)
def get_application_status() -> dict:
    return {
        "status": "ok",
        "uptime": 12345,
        "version": "1.23",
    }


@mcp.resource("resource://system-status")
async def get_system_status(ctx: Context) -> dict:
    """Provides system status information."""
    return {"status": "operational", "request_id": ctx.request_id}


# Dynamic resource with parameter, note that this kind of resource are not listed by client.list_resources()
@mcp.resource(uri="resource://{name}/details", name="NameDetails")
async def get_name_details(name: str, ctx: Context) -> dict:
    """Get details for a specific name."""
    return {"name": name, "accessed_at": ctx.request_id}


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
