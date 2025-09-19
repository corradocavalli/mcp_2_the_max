# Elicitation - MCP Two-Way Communication Example

Demonstrates interactive data collection and confirmation workflows using MCP elicitation for bidirectional server-client communication.

## Server Configuration

**Two-Way Communication**: Server can request information from clients during tool execution, enabling interactive workflows and user confirmations.

**Elicitation Benefits**:
- **Interactive Confirmation** - "Are you sure?" type prompts during operations
- **User Input Collection** - Gather structured data from users mid-execution
- **Smooth UX** - Seamless integration of user interaction in tool workflows
- **Server Routing** - Opens possibilities for conditional logic based on user responses

## Available Tools

### Data Collection Tool
- `collect_user_info()` - Demonstrates structured data elicitation:

```python
@mcp.tool
async def collect_user_info(ctx: Context) -> str:
    """Collect user information through interactive prompts."""
    result = await ctx.elicit(
        message="Please provide your information", 
        response_type=UserInfo
    )
    # Handle accept/decline/cancel actions
```

### Confirmation Tool
- `accept_tool()` - Simple yes/no confirmation workflow
  - Asks user to confirm expensive operation (2000 CHF cost)
  - Handles accept/decline/cancel responses
  - Demonstrates confirmation patterns

## Client Behavior

- Implements `elicitation_handler` to respond to server requests
- Handles structured data input (UserInfo with name/age)
- Manages simple confirmation prompts (yes/no responses)
- Calls both tools and processes interactive responses

## Key Learning Points

- **Bidirectional Communication** - Server can request data from client during execution
- **Interactive Workflows** - Tools can pause execution to gather user input
- **Confirmation Patterns** - Simple "Are you sure?" prompts for critical operations
- **Structured Elicitation** - Type-safe data collection using dataclasses
- **Response Handling** - Managing accept/decline/cancel action flows
- **Server Routing Potential** - Foundation for conditional tool behavior based on user input