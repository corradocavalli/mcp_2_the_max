# LLM sampling allows MCP tools to request the client’s LLM to generate text based on provided messages. This is useful when tools need to leverage the LLM’s capabilities to process data, generate responses, or perform text-based analysis.

import asyncio

from fastmcp import Context, FastMCP
from pydantic import BaseModel, Field
from typing_extensions import Annotated

STOCK_INFO = False

mcp = FastMCP("TraderServer")


async def progress(ctx: Context):
    await ctx.report_progress(progress=1, total=3, message="Contacting broker...")
    await asyncio.sleep(0.5)
    await ctx.report_progress(progress=2, total=3, message="Sending order...")
    await asyncio.sleep(1)
    await ctx.report_progress(progress=3, total=3, message="Order completed.")
    await asyncio.sleep(0.5)


@mcp.tool(name="buy", meta={"description": "Process a buy order"})
async def buy(stock: str, quantity: float, ctx: Context) -> str:
    """Process a buy order."""
    result = await ctx.elicit(
        message=f"Confirm the **BUY** order of {quantity} shares of {stock}?"
    )
    print(result)
    if result.action == "accept":
        await progress(ctx)
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
        await progress(ctx)
        return f"Sold {quantity} shares of {stock}"
    else:
        return "Sell order NOT confirmed"


@mcp.tool(
    name="get_stock_quote",
    description="Provide the current stock quote for a given stock symbol.",
    annotations={
        "readOnlyHint": "true",
        "idempotentHint": "true",
    },
)
async def get_stock_quote(
    symbol: Annotated[
        str, Field(description="Stock symbol (e.g., 'AAPL', 'MSFT')", min_length=1)
    ],
    ctx: Context,
) -> str:
    """Get the current stock quote."""
    if symbol == "AAPL":
        return "The current price of AAPL is $238.78"
    elif symbol == "MSFT":
        return "The current price of MSFT is $510.00"
    else:
        return f"Sorry, I don't have data for the stock symbol '{symbol}'."


# Add comprehensive stock info tool if enabled
if STOCK_INFO:

    @mcp.tool(
        name="get_stock_info",
        description="Provide financial information for a given stock symbol.",
        annotations={
            "readOnlyHint": "true",
            "idempotentHint": "true",
        },
    )
    async def get_stock_info(
        symbol: Annotated[
            str, Field(description="Stock symbol (e.g., 'AAPL', 'MSFT')", min_length=1)
        ],
        ctx: Context,
    ) -> str:
        """Get comprehensive financial information for a stock."""
        if symbol == "AAPL":
            return "AAPL: Price $238.78, Market Cap $3.67T, P/E 32.4, 52-week range $164.08-$237.23, Dividend Yield 0.44%"
        elif symbol == "MSFT":
            return "MSFT: Price $510.00, Market Cap $3.79T, P/E 34.2, 52-week range $309.45-$468.35, Dividend Yield 0.72%"
        else:
            return (
                f"Sorry, I don't have financial data for the stock symbol '{symbol}'."
            )


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=9000)  # run the MCP server
