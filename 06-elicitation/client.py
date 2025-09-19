import asyncio

from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult
from rich.console import Console
from server import UserInfo  # Import the dataclass from the server file

console = Console()
console.clear()


async def elicitation_handler(message: str, response_type: type, params, context):
    # Present the message to the user and collect input
    console.print("elicitation_handler Invoked")
    console.print(response_type, style="bold green")
    if response_type is None:
        console.print(message, style="bold green")
        user_input = input("Your response: ")
        if user_input == "yes":
            return ElicitResult(action="accept")
        return ElicitResult(action="cancel")
    if response_type.__name__ == "UserInfo":
        console.print(message, style="bold green")
        name = input("Name: ")
        age = input("Age: ")

        if len(name) == 0 or len(age) == 0:
            return ElicitResult(action="cancel")

        return ElicitResult(
            action="accept", content=response_type(name=name, age=int(age))
        )
    else:
        console.print("Unsupported response type", style="bold red")
        return ElicitResult(action="cancel")


async def main():

    # Create the client with the elicitation handler that will be called on elicitation requests
    async with Client(
        "http://localhost:8000/mcp", elicitation_handler=elicitation_handler
    ) as client:

        # user info tool
        result = await client.call_tool("collect_user_info")
        console.print(result, style="bold blue")

        # simple action
        result = await client.call_tool("accept_tool")
        console.print(result, style="bold magenta")


asyncio.run(main())
