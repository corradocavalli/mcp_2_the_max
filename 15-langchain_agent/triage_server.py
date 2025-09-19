# LLM sampling allows MCP tools to request the client’s LLM to generate text based on provided messages. This is useful when tools need to leverage the LLM’s capabilities to process data, generate responses, or perform text-based analysis.

from textwrap import dedent
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class ServerMessage(BaseModel):
    action: Literal["buy", "sell", "abort"]
    stock: str
    quantity: float


from fastmcp import Context, FastMCP

mcp = FastMCP("TriageServer")


@mcp.tool(
    name="process_stock_order",
    description="Always use this tool to handle initial order processing and routing.",
    meta={"version": "1.0"},
    annotations={
        "readOnlyHint": "false",
        "idempotentHint": "false",
    },
)
async def process_stock_order(
    action: Annotated[
        Literal["buy", "sell"],
        Field(description="Either 'buy' or 'sell'", min_length=1),
    ],
    stock: Annotated[
        str, Field(description="Stock symbol (e.g., 'AAPL', 'MSFT')", min_length=1)
    ],
    quantity: Annotated[float, Field(description="Number of shares to trade", gt=0)],
    ctx: Context,
) -> Annotated[str, Field(description="The response from the trader")]:
    """Process a buy or sell order."""
    message = ServerMessage(action=action, stock=stock, quantity=quantity)
    json = message.model_dump_json()
    response = await ctx.sample(messages=json)
    return f"Here's the response from the trader: {response.text}"


@mcp.prompt
def trader_system_prompt(stocks: list[str]) -> str:
    """Generates the system prompt."""
    stocks = ", ".join(stocks)
    return dedent(
        f"""
    You are a helpful AI assistant that can help with stock trading operations.
    You can only trade the following stocks: {stocks} deny to trade any other stock.

    Always provide clear information about what actions you're taking.
    If the user mention the company name, automatically convert it to the stock symbol.
"""
    )


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
