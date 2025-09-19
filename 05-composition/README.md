# Composition - MCP Server Composition Example

Demonstrates how to combine multiple MCP servers into a single unified server using server composition and prefixed imports.

## Server Configuration

**Server Composition**: Shows how to import and combine multiple MCP servers with namespace prefixes for better organization and decoupling.

```python
# Import weather subserver with prefix
await main_mcp.import_server(weather_mcp, prefix="weather")
```

**Benefits of Server Imports**:
- **Decoupling** - Separate concerns into focused, independent servers
- **Organization** - Logical grouping of related functionality
- **Reusability** - Subservers can be imported into multiple main servers
- **Namespace Management** - Prefixes prevent naming conflicts between servers

## Available Components

### Main Server Tools
- `get_stock(stock_id)` - Stock information retrieval from the main server
  - Returns stock ID and current value

### Imported Weather Server Tools
- `weather_get_forecast(city)` - Weather forecast from imported weather server
  - **Prefixed with "weather"** to avoid naming conflicts
  - Original tool name: `get_forecast` → Imported as: `weather_get_forecast`

### Server Structure
```python
# Main server
main_mcp = FastMCP(name="MainServer")

# Weather subserver (separate file)
weather_mcp = FastMCP(name="WeatherServer")

# Composition
await main_mcp.import_server(weather_mcp, prefix="weather")
```

## Client Behavior

- Lists all available tools from both servers combined
- Calls `get_stock` with stock ID "MSFT" from main server
- Calls `weather_get_forecast` with city "London" from imported weather server
- Demonstrates unified access to composed functionality

## Key Learning Points

- **Server Composition** - Combining multiple MCP servers into one unified interface
- **Namespace Prefixing** - Using prefixes to organize and avoid naming conflicts
- **Modular Architecture** - Separating functionality into focused, reusable components
- **Import Patterns** - How to structure and import subservers
- **Unified Client Access** - Single endpoint serving multiple server capabilities
- **Async Setup** - Proper initialization of server composition before running