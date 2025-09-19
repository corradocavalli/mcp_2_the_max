# Roots - File System Access Control

Demonstrates MCP's root-based security model for controlling server file system access through client-authorized paths.

## Server Configuration

**Root Discovery**: Server uses `ctx.list_roots()` to discover client-authorized file system locations:
```python
@mcp.tool
async def read_file(filename: str, ctx: Context) -> str:
    """Read the contents of a file."""
    all_roots = []
    try:
        all_roots = await ctx.list_roots()
    except Exception as e:
        raise ToolError(
            "No roots available to read the file. Please specify them in client configuration."
        )
```

**Secure File Access**: Constructs file paths relative to authorized roots for safe file operations:
```python
# Uses first available root and appends filename
file_uri = f"{all_roots[0].uri}/{filename}".replace("file://", "")
```

## Available Tools

### File Operations
- `read_file(filename)` - Reads file content from client-authorized directories only
  - Validates against available roots before file access
  - Provides detailed error messages when roots are unavailable
  - Demonstrates secure file system boundaries

## Client Behavior

**Static Root Authorization**: Client defines specific directories the server can access:
```python
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
roots = [f"file://{current_dir}"]

client = Client("http://localhost:8000/mcp", roots=roots)
```

**Dynamic Root Callback**: Alternative approach for runtime root authorization:
```python
async def roots_callback(context: RequestContext) -> list[str]:
    console.print(f"Server requested roots (Request ID: {context.request_id})")
    return [f"file://{current_dir}/roots"]
```

**Portable Path Handling**: Uses cross-platform path resolution instead of hardcoded absolute paths:
- `Path(__file__).parent.absolute()` - Gets script directory dynamically
- Works consistently across different machines and operating systems
- Prevents path-related deployment issues

## Key Learning Points

- **Security Model** - Roots provide granular control over server file system access
- **Client Authorization** - Servers can only access paths explicitly authorized by clients
- **Error Handling** - Graceful degradation when roots are unavailable or misconfigured
- **Cross-Platform Paths** - Use `pathlib.Path` for portable file path handling
- **Dynamic Authorization** - Root callbacks enable runtime permission management
- **File System Boundaries** - MCP enforces strict boundaries between authorized and unauthorized locations
- **Request Context** - Root callbacks receive request context for audit and logging purposes