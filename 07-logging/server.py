from fastmcp import Context, FastMCP

mcp = FastMCP("Logging Server")


from fastmcp import Context, FastMCP

mcp = FastMCP("LoggingDemo")


# Tool with various logging levels (where are these logs visible?)
@mcp.tool
async def analyze_data(data: list[float], ctx: Context) -> dict:
    """Analyze numerical data with comprehensive logging."""
    await ctx.debug("Starting analysis of numerical data")
    await ctx.info(f"Analyzing {len(data)} data points")

    try:
        if not data:
            await ctx.warning("Empty data list provided")
            return {"error": "Empty data list"}

        result = sum(data) / len(data)
        await ctx.info(f"Analysis complete, average: {result}")
        return {"average": result, "count": len(data)}

    except Exception as e:
        await ctx.error(f"Analysis failed: {str(e)}")
        raise


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
