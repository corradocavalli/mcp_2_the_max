# Progress - MCP Progress Tracking Example

Demonstrates how to provide real-time feedback about tool execution progress to clients during long-running operations.

## Server Configuration

**Progress Feedback**: MCP now provides the ability to report execution progress, allowing clients to track and display the status of long-running tool operations in real-time.

## Available Tools

### Progress-Enabled Tool
- `process_items(items)` - Processes a list of items with real-time progress updates:

```python
@mcp.tool
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process a list of items with progress updates."""
    total = len(items)
    for i, item in enumerate(items):
        # Report progress as we process each item
        await ctx.report_progress(progress=i, total=total)
        # Processing logic here...
    
    # Report 100% completion
    await ctx.report_progress(progress=total, total=total)
```

**Progress Features**:
- **Real-time Updates** - Progress reported during execution, not just at completion
- **Percentage Calculation** - Client can calculate completion percentage
- **Item-by-Item Tracking** - Progress updates for each processed item
- **Completion Notification** - Final progress report when tool finishes

## Client Behavior

- Implements `progress_handler` to receive and display progress updates
- Calculates completion percentage from progress/total values
- Displays real-time progress as tool executes
- Calls `process_items` with sample data `["hi", "how", "are", "you", "?"]`
- Shows both progress updates and final results

## Key Learning Points

- **Progress Reporting** - Tools can provide feedback about execution status
- **Long-Running Operations** - Essential for tools that take significant time
- **User Experience** - Clients can show progress bars or status indicators
- **Real-time Communication** - Progress updates sent during execution, not just at end
- **Percentage Tracking** - Standard progress/total pattern for completion calculation
- **Async Progress** - Non-blocking progress updates using `ctx.report_progress()`