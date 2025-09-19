# Resources - MCP Resources Example

Demonstrates how to expose read-only data through MCP resources with various configurations and access patterns.

## Server Configuration

**Basic Setup**: Simple FastMCP server named "DataServer" without complex duplication handling.

## Available Resources

### Basic Resources
- `resource://greeting` - Simple text greeting message
- `data://config` - Application configuration with `readOnlyHint=True` and `idempotentHint=True` annotations
- `resource://system-status` - System status using request context (async handler)

### Advanced Metadata Resource
- `data://app-status` - Demonstrates comprehensive resource configuration:

```python
@mcp.resource(
    uri="data://app-status",  # Explicit URI
    name="ApplicationStatus",  # Custom name
    description="Provides the current status of the application.",
    mime_type="application/json",  # Explicit MIME type
    tags={"monitoring", "status"},  # Categorization tags
    meta={"version": "2.1", "team": "infrastructure"},  # Custom metadata
)
```

### Dynamic Resource (Not Listed)
- `resource://{name}/details` - Parameterized resource (not visible in `list_resources()` because it uses URI templates)
  - Accessed directly: `resource://corrado/details`
  - Uses both parameter (`name`) and context (`ctx`)

## Client Behavior

- Lists all available static resources
- Reads `data://app-status` and displays JSON content
- Directly accesses parameterized resource `resource://corrado/details`
- Reads context-aware `resource://system-status`

## Key Learning Points

- **Resource Types** - String vs JSON data exposure
- **Static vs Dynamic** - Enumerable resources vs parameterized templates  
- **Resource Metadata** - Names, descriptions, MIME types, tags, and custom metadata
- **Context Usage** - Accessing request context in resource handlers
- **Behavioral Annotations** - `readOnlyHint` and `idempotentHint` for resource guidance
- **URI Patterns** - Different schemes (`resource://`, `data://`) and parameterization