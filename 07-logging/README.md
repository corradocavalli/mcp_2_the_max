# Logging - MCP Log Forwarding Example

Demonstrates how MCP servers can forward logs to clients, making remote debugging and monitoring simple and accessible.

## Server Configuration

**Remote Logging Challenge**: When MCP servers run remotely, inspecting logs can be complicated since traditional logging outputs aren't accessible to the client.

**MCP Solution**: MCP forwards server logs directly to the invoking client, making inspection much simpler regardless of server location.

## Available Tools

### Comprehensive Logging Tool
- `analyze_data(data)` - Data analysis tool with multi-level logging:

```python
@mcp.tool
async def analyze_data(data: list[float], ctx: Context) -> dict:
    """Analyze numerical data with comprehensive logging."""
    await ctx.debug("Starting analysis of numerical data")
    await ctx.info(f"Analyzing {len(data)} data points")
    await ctx.warning("Empty data list provided")  # On empty data
    await ctx.error(f"Analysis failed: {str(e)}")  # On exceptions
```

**Logging Levels Used**:
- **Debug** - Detailed execution flow information
- **Info** - General operational messages
- **Warning** - Potential issues or edge cases
- **Error** - Exception handling and failures

## Client Behavior

- Implements `log_handler` to receive and process server logs
- Converts MCP log levels to Python logging levels
- Displays logs in real-time with Rich console formatting
- Calls `analyze_data` with sample data `[1, 2, 3, 4, 5]`
- Shows both logs and final tool response

## Key Learning Points

- **Remote Log Access** - Server logs forwarded to client regardless of server location
- **Real-time Monitoring** - Live log streaming during tool execution
- **Level Mapping** - Converting MCP log levels to standard Python logging
- **Debugging Simplification** - No need for server-side log file access
- **Unified Logging** - Client receives complete execution trace from remote servers
- **Development Experience** - Seamless debugging of distributed MCP applications