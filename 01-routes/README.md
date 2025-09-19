# Routes - MCP Tools + Custom Routes Example

Demonstrates how an MCP server can expose both MCP tools and custom HTTP endpoints simultaneously.

## Server Configuration

**Duplication Handling**: Shows how to configure behavior when duplicate tools/resources/prompts are registered:
```python
mcp = FastMCP(
    on_duplicate_tools="error",      # Raise error on duplicate tools
    on_duplicate_resources="warn",   # Warn on duplicate resources  
    on_duplicate_prompts="replace",  # Replace existing prompts
)
```

**Tag-based Filtering**: Uses `include_tags={"dev", "catalog"}` to control tool visibility.

## Available Tools

### MCP Tool
- `cpu_usage()` - Returns mock CPU usage data (47%)
  - Uses comprehensive annotations: `readOnlyHint=True`, `openWorldHint=False`, `idempotentHint=True`
  - Tagged as "dev" and "admin"

### Custom HTTP Route
- `GET /health` - Custom endpoint that returns "Server is OK"
  - Defined with `@mcp.custom_route("/health", methods=["GET"])`
  - Returns `PlainTextResponse` 
  - **Not exposed as an MCP tool** - accessible only via direct HTTP calls

## Client Behavior

- Lists all available MCP tools (custom routes are not included)
- Calls `cpu_usage()` MCP tool via MCP protocol
- Makes direct HTTP GET request to `/health` endpoint using httpx

## Key Learning Points

- **Dual Protocol Support** - Same server exposes both MCP tools and HTTP endpoints
- **Protocol Separation** - Custom routes are not visible to MCP clients as tools
- **Route Definition** - Use `@mcp.custom_route()` decorator for HTTP endpoints
- **Client Access Patterns** - MCP tools via Client, HTTP routes via direct HTTP calls
- **Tool Annotations** - Advanced hints like `idempotentHint` for operation characteristics
- **Response Types** - Custom routes can return various Starlette response types