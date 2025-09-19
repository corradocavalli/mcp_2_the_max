# Context - MCP Context Management Example

Demonstrates how to use Context objects for request management and resource access within MCP tools and resources.

## Server Configuration

**Basic Setup**: Simple FastMCP server named "Context-Server" that uses context to access the ID of calling requests.

## Available Components

### Context-Aware Resource
- `resource://system-status` - System status resource that uses context to access and include the calling request ID
  - Returns operational status with the current request identifier
  - Demonstrates how the server uses `ctx.request_id` to track individual requests

### Context-Using Tool
- `system_health_check()` - Tool that uses context to read internal resources:

```python
@mcp.tool()
async def system_health_check(ctx: Context) -> dict:
    """Checks the health of the system."""
    status_resource = await ctx.read_resource("resource://system-status")
    content = status_resource[0].content
    return json.loads(content)
```

## Client Behavior

- Calls `system_health_check` tool which internally uses context
- Displays the result showing system status with request ID
- Demonstrates tool-to-resource communication via context

## Key Learning Points

- **Context Injection** - How to receive Context objects in tools and resources
- **Request Tracking** - Using `ctx.request_id` for request identification
- **Internal Resource Access** - Tools reading resources using `ctx.read_resource()`
- **Context Lifecycle** - Context objects maintain request state throughout the call
- **Resource Communication** - Tools can access other server resources internally
- **JSON Handling** - Parsing resource content within tool implementations