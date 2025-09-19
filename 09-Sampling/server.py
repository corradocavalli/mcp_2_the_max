# LLM sampling allows MCP tools to request the client’s LLM to generate some text based on provided messages.
# This is useful when tools need to leverage the LLM’s capabilities to process data, generate responses, or perform text-based analysis.
# Since its just a request to the client, it can be also used for orchestration.

from fastmcp import Context, FastMCP

mcp = FastMCP("SamplingDemo")


# A simple tool that uses sampling to generate a creative story about a given topic.
@mcp.tool
async def creative_writing(topic: str, ctx: Context) -> str:
    """Generate creative content using a specific model."""
    response = await ctx.sample(
        system_prompt="You are a creative writing assistant.",
        messages=f"Write a creative short story about {topic}",
        model_preferences="claude-3-sonnet",  # Prefer a specific model
        include_context="thisServer",  # Use the server's context
        temperature=0.9,  # High creativity
        max_tokens=1000,
    )
    return response.text


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
