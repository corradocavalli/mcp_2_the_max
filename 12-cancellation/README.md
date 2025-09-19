# Cancellation - Interrupting Long-Running Tool Executions

Demonstrates MCP's cancellation support for gracefully interrupting long-running tool operations that need to be stopped before completion.

## Overview

Sometimes long-running tasks inside tool executions need to be interrupted. Cancellation support helps manage this scenario, but **the tool must be written with cancellation support** to handle interruption gracefully.

## Server Configuration

**Cancellation-Aware Tools**: Tools must be designed to handle cancellation exceptions and clean up properly:
```python
@mcp.tool
async def long_execution(count: int, ctx: Context) -> str:
    """Long-running operation with cancellation support."""
    try:
        for i in range(count):
            await ctx.report_progress(progress=i, total=count)
            await asyncio.sleep(1)  # Cancellable operation
        return f"Completed long-running operation with {count} steps."
    except Exception as e:
        # Handle cancellation gracefully
        print(f"long_execution was cancelled after {i} steps out of {count}")
        return f"Long execution was cancelled after {i} steps out of {count}"
```

**Progress Reporting**: Integration with progress reporting for better user experience:
```python
await ctx.report_progress(progress=i, total=count)
```

## Available Tools

### Cancellation-Enabled Tools
- `long_execution(count)` - Simulates long-running operation with cancellation support
  - Reports progress at each step using `ctx.report_progress()`
  - Handles cancellation gracefully with proper cleanup
  - Returns partial completion status when cancelled
  - Demonstrates best practices for interruptible operations

- `short_execution(topic)` - Quick operation for comparison
  - Returns immediately with request context information
  - Shows normal execution flow without cancellation concerns

## Client Behavior

**Request ID Management**: Client tracks request IDs for targeted cancellation:
```python
# Get the request ID for the next operation
executing_request_id = client.session._request_id

# Start background cancellation task
cancel_task = asyncio.create_task(
    cancel_after_delay(client, executing_request_id, delay=3)
)
```

**Background Cancellation**: Implements time-based automatic cancellation:
```python
async def cancel_after_delay(client, request_id, delay=3):
    """Cancel execution after a specified delay."""
    await asyncio.sleep(delay)
    await client.cancel(request_id)
```

**Progress Monitoring**: Handles progress updates during execution:
```python
async def progress_handler(progress: float, total: float | None, message: str | None):
    if total is not None:
        percentage = (progress / total) * 100
        console.print(f"Progress: {percentage:.1f}% - {message or ''}")
```

**Exception Handling**: Properly handles cancellation and cleanup:
```python
try:
    result = await client.call_tool("long_execution", {"count": 10})
    cancel_task.cancel()  # Cancel background task on success
except Exception as e:
    console.print(f"Tool error: {e}")  # Handle cancellation exception
```

## Key Learning Points

- **Cancellation Design** - Tools must explicitly support cancellation through proper exception handling
- **Request Tracking** - Client must manage request IDs to target specific operations for cancellation
- **Progress Integration** - Cancellation works seamlessly with progress reporting systems
- **Graceful Degradation** - Cancelled operations should return meaningful partial results
- **Resource Cleanup** - Proper cleanup of background tasks and resources on cancellation
- **Async Best Practices** - Use `asyncio.sleep()` and other cancellable operations in tool loops
- **User Experience** - Combine cancellation with progress reporting for responsive interfaces
- **Error Handling** - Distinguish between cancellation and other exceptions for appropriate responses

## Implementation Requirements

**For Tool Authors**:
1. Use `async` functions for long-running operations
2. Include cancellable operations (like `asyncio.sleep()`) in loops
3. Handle cancellation exceptions gracefully
4. Report progress regularly using `ctx.report_progress()`
5. Return meaningful status on cancellation

**For Client Authors**:
1. Track request IDs for operations that may need cancellation
2. Implement background cancellation logic
3. Handle cancellation exceptions appropriately
4. Clean up background tasks after operations complete