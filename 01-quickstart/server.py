from dataclasses import dataclass
from typing import Annotated

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from typing_extensions import Literal

mcp = FastMCP(
    name="My MCP Server",
    include_tags={"dev", "catalog"},  # Only expose these tagged components
    exclude_tags={"internal", "deprecated"},  # Hide these tagged components
    on_duplicate_tools="error",  # Handle duplicate registrations
    on_duplicate_resources="warn",
    on_duplicate_prompts="replace",
    include_fastmcp_meta=False,  # Disable FastMCP metadata for cleaner integration
)


@dataclass
class Person:
    name: str
    age: int
    email: str


# structured output
@mcp.tool(tags={"dev", "admin"})
def get_user_profile(user_id: str) -> Person:
    """Get a user's profile information."""
    return Person(name="Alice", age=30, email="alice@example.com")


# Raise error
@mcp.tool(tags={"dev", "admin"})
def divide(a: float, b: float) -> float:
    """Divide a by b."""

    if b == 0:
        # Error messages from ToolError are always sent to clients,
        # regardless of mask_error_details setting
        raise ToolError("Division by zero is not allowed.")

    # If mask_error_details=True, this message would be masked
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers.")

    return a / b


# disabled tool
@mcp.tool(enabled=False)
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool(tags={"dev", "admin"})
def greet_v2(name: str) -> str:
    return f"Hello, DEV {name}!"


@mcp.tool(
    tags={"dev", "admin"},
    annotations={
        "title": "Get cpu usage",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
)
def cpu_usage() -> str:
    return "47%"


# Tool with type hints for the LLM
@mcp.tool(
    name="find_products",  # Custom tool name for the LLM
    description="Search the product catalog with optional category filtering.",  # Custom description
    tags={"catalog", "search"},  # Optional tags for organization/filtering
    meta={"version": "1.2", "author": "product-team"},  # Custom metadata
)
def search_products_implementation(
    query: Annotated[str, Field(description="The user query")],
    category: Annotated[
        Literal["ai", "microsoft"] | None, Field(description="The desired category")
    ] = None,
) -> Annotated[
    list[dict], Field(description="A list of products matching the search criteria.")
]:
    print(f"Searching for '{query}' in category '{category}'")
    return [{"id": 2, "name": "Another Product"}]


# Custom route
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Server is OK")


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
