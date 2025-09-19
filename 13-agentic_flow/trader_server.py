# LLM sampling allows MCP tools to request the client’s LLM to generate text based on provided messages. This is useful when tools need to leverage the LLM’s capabilities to process data, generate responses, or perform text-based analysis.

from typing import Literal

from fastmcp import Context, FastMCP
from pydantic import BaseModel

mcp = FastMCP("TraderServer")


@mcp.tool(name="buy", meta={"description": "Process a buy order"})
async def buy(stock: str, quantity: float, ctx: Context) -> str:
    """Process a buy order."""
    result = await ctx.elicit(
        message=f"Confirm the **BUY** order of {quantity} shares of {stock}?"
    )
    print(result)
    if result.action == "accept":
        return f"Bought {quantity} shares of {stock}"
    else:
        return "Buy order NOT confirmed"


@mcp.tool(name="sell", meta={"description": "Process a sell order"})
async def sell(stock: str, quantity: float, ctx: Context) -> str:
    """Process a sell order."""
    result = await ctx.elicit(
        message=f"Confirm the **SELL** order of {quantity} shares of {stock}?"
    )
    if result.action == "accept":
        return f"Sold {quantity} shares of {stock}"
    else:
        return "Sell order NOT confirmed"


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=9000)
