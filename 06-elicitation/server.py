# Elicitation allows you to interactively gather information from users.

from dataclasses import dataclass

from fastmcp import Context, FastMCP

mcp = FastMCP("Elicitation Server")


@dataclass
class UserInfo:
    name: str
    age: int


@mcp.tool
async def collect_user_info(ctx: Context) -> str:
    """Collect user information through interactive prompts."""
    result = await ctx.elicit(
        message="Please provide your information", response_type=UserInfo
    )

    if result.action == "accept":
        user = result.data
        return f"Hello {user.name}, you are {user.age} years old"
    elif result.action == "decline":
        return "Information not provided"
    else:  # cancel
        return "Operation cancelled"


@mcp.tool
async def accept_tool(ctx: Context) -> str:
    result = await ctx.elicit("This is gonna cost 2000 CHF, do you want to continue?")

    if result.action == "accept":
        return "Accepted!"
    elif result.action == "decline":
        return "Declined!"
    else:
        return "Cancelled!"


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
