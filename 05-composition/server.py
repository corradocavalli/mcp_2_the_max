# Combine multiple mcp server

import asyncio

from fastmcp import FastMCP
from weather_server import weather_mcp

# Define main server
main_mcp = FastMCP(name="MainServer")


@main_mcp.tool
def get_stock(stock_id: str) -> dict:
    """Get stock information."""
    return {"id": stock_id, "value": 212.45}


# Import subserver
async def setup():
    await main_mcp.import_server(weather_mcp, prefix="weather")


# Result: main_mcp now contains prefixed components:
# - Tool: "weather_get_forecast" + "get_stock"
# - Resource: "data://weather/cities/supported"

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run(transport="http", host="localhost", port=8000)
