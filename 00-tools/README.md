# Tools - Basic Tools Example

Demonstrates fundamental MCP tool creation, configuration, and client-server communication.

## Server Configuration

**Duplication Handling**: Shows how to configure behavior when duplicate tools/resources/prompts are registered:
```python
mcp = FastMCP(
    on_duplicate_tools="error",      # Raise error on duplicate tools
    on_duplicate_resources="warn",   # Warn on duplicate resources  
    on_duplicate_prompts="replace",  # Replace existing prompts
)
```

**Tag-based Filtering**: Uses `include_tags={"dev", "catalog"}` and `exclude_tags={"internal", "deprecated"}` to control tool visibility.

## Available Tools

### Basic Tools
- `get_user_profile(user_id)` - Returns structured user profile data (dataclass output)
- `divide(a, b)` - Mathematical division with error handling using `ToolError`
- `greet_v2(name)` - Simple greeting function (tagged as "dev")

### Advanced Annotated Tool
- `find_products(query, category)` - Demonstrates comprehensive LLM guidance through annotations:

```python
@mcp.tool(
    name="find_products",  # Custom tool name for LLM
    description="Search the product catalog with optional category filtering.",
    tags={"catalog", "search"},
    meta={"version": "1.2", "author": "product-team"}
)
def search_products(
    query: Annotated[str, Field(description="The user query")],
    category: Annotated[Literal["ai", "microsoft"] | None, 
                       Field(description="The desired category")] = None,
) -> Annotated[list[dict], Field(description="A list of products matching criteria")]:
```

### Hidden Tool
- `cpu_usage()` - Mock CPU usage (tagged as "internal", hidden because "internal" is in exclude_tags)
  - Uses `readOnlyHint=True` and `openWorldHint=False` annotations

## Client Behavior

- Lists all available tools from the server
- Calls `greet_v2` with name "Fred"
- Calls `find_products` with query "laptop" and category "ai"

## Key Learning Points

- **Duplication Configuration** - Handle tool/resource/prompt conflicts with `on_duplicate_*` settings
- **LLM Annotations** - Guide LLM behavior with `Field(description=...)`, custom names, and hints
- **Structured Outputs** - Return dataclasses for better LLM parsing
- **Type Safety** - Use `Annotated` types and `Literal` for parameter validation
- **Tool Metadata** - Add version info and authorship with `meta` parameter
- **Behavioral Hints** - Use `readOnlyHint` and `openWorldHint` for client app guidance