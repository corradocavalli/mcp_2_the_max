# LLM sampling allows MCP tools to request the client’s LLM to generate text based on provided messages. This is useful when tools need to leverage the LLM’s capabilities to process data, generate responses, or perform text-based analysis.

from typing import Literal

from pydantic import BaseModel


class ServerMessage(BaseModel):
    action: Literal["buy", "sell", "abort"]
    stock: str
    quantity: float


from fastmcp import Context, FastMCP

mcp = FastMCP("TriageServer")


@mcp.tool(
    name="process_stock_order",
    title="The stock order",
    meta={"version": "1.0"},
    annotations={
        "readOnlyHint": "false",
        "idempotentHint": "false",
    },
)
async def process_stock_order(
    action: Literal["buy", "sell"], stock: str, quantity: float, ctx: Context
) -> str:
    """Process a buy or sell order."""
    message = ServerMessage(action=action, stock=stock, quantity=quantity)
    json = message.model_dump_json()
    response = await ctx.sample(messages=json)
    return f"Here's the response from the trader: {response.text}"


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
