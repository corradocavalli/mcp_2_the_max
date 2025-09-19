# Agentic Flow - Server Orchestration with Elicitation and Sampling

Demonstrates advanced MCP server orchestration using Elicitation and Sampling to show how MCP can route requests between multiple specialized servers in an agentic workflow.

## Prerequisites

**Multiple Server Setup**: This example requires running both servers simultaneously:
```bash
# Terminal 1 - Start the triage server
uv run triage_server.py

# Terminal 2 - Start the trader server  
uv run trader_server.py

# Terminal 3 - Run the client
uv run client.py
```

## Server Configuration

**Triage Server (Port 8000)**: Acts as a routing coordinator that processes stock orders and delegates execution:
```python
@mcp.tool
async def process_stock_order(
    action: Literal["buy", "sell"], stock: str, quantity: float, ctx: Context
) -> str:
    """Process a buy or sell order."""
    message = ServerMessage(action=action, stock=stock, quantity=quantity)
    json = message.model_dump_json()
    # Use sampling to delegate to trader server via client
    response = await ctx.sample(messages=json)
    return f"Here's the response from the trader: {response.text}"
```

**Trader Server (Port 9000)**: Executes actual trading operations with user confirmation:
```python
@mcp.tool
async def buy(stock: str, quantity: float, ctx: Context) -> str:
    """Process a buy order with user confirmation."""
    # Use elicitation to request user approval
    result = await ctx.elicit(
        message=f"Confirm the **BUY** order of {quantity} shares of {stock}?"
    )
    if result.action == "accept":
        return f"Bought {quantity} shares of {stock}"
    else:
        return "Buy order NOT confirmed"
```

## Available Tools

### Triage Server Tools
- `process_stock_order(action, stock, quantity)` - Routes stock orders to appropriate execution server
  - Accepts "buy" or "sell" actions with stock symbol and quantity
  - Uses `ctx.sample()` to delegate execution to trader server
  - Demonstrates server-to-server communication patterns

### Trader Server Tools
- `buy(stock, quantity)` - Executes buy orders with user confirmation
  - Uses `ctx.elicit()` to request user approval before execution
  - Returns confirmation message on successful purchase
  - Demonstrates interactive approval workflows

- `sell(stock, quantity)` - Executes sell orders with user confirmation
  - Similar elicitation pattern for sell transactions
  - Requires explicit user confirmation before execution
  - Provides clear feedback on transaction status

## Client Behavior

**Multi-Server Orchestration**: Client manages connections to both servers with specialized handlers:
```python
# Sampling handler for triage server delegation
async def sampling_handler(messages, params, context):
    server_message = ServerMessage.model_validate_json(messages[0].content.text)
    # Route to appropriate trader server method
    if server_message.action == "buy":
        response = await trader.call_tool("buy", {...})
    elif server_message.action == "sell":
        response = await trader.call_tool("sell", {...})

# Elicitation handler for trader server confirmations
async def elicitation_handler(message, response_type, params, context):
    console.print(message)
    user_input = input("Your response (yes/no): ")
    return ElicitResult(action="accept" if user_input == "yes" else "cancel")
```

**Environment-Based Configuration**: Uses `.env` variables for server endpoints:
```python
client = Client(os.getenv("TRIAGE_SERVER_URL"), sampling_handler=sampling_handler)
trader = Client(os.getenv("TRADER_SERVER_URL"), elicitation_handler=elicitation_handler)
```

## Key Learning Points

- **Server Orchestration** - How multiple MCP servers can work together in distributed workflows
- **Sampling Delegation** - Using `ctx.sample()` to route requests from one server to client-side handlers
- **Elicitation Integration** - Combining user confirmation flows with server-to-server communication
- **Agentic Patterns** - Building intelligent routing systems that can make decisions about task delegation
- **Handler Specialization** - Different clients can have specialized handlers for different interaction types
- **Environment Configuration** - Managing multiple server endpoints through environment variables
- **Message Serialization** - Using Pydantic models for structured communication between servers
- **Interactive Workflows** - Combining automated routing with human-in-the-loop confirmation patterns
- **Distributed Architecture** - Designing systems where specialized servers handle specific domain responsibilities

## Architecture Pattern

**Workflow Flow**:
1. **Client Request** → Triage Server (`process_stock_order`)
2. **Triage Server** → Uses `ctx.sample()` to delegate back to client
3. **Client Sampling Handler** → Routes to appropriate Trader Server tool
4. **Trader Server** → Uses `ctx.elicit()` for user confirmation
5. **Client Elicitation Handler** → Prompts user and returns decision
6. **Response Chain** → Results flow back through the delegation chain

**Benefits**:
- **Separation of Concerns** - Triage handles routing, Trader handles execution
- **User Control** - Explicit confirmation required for financial transactions
- **Flexibility** - Easy to add new server types or modify routing logic
- **Scalability** - Servers can be deployed independently and scaled separately
- **Auditability** - Clear chain of responsibility for all trading decisions

This pattern demonstrates how MCP enables sophisticated multi-server architectures where different services can collaborate while maintaining clear boundaries and user control points.