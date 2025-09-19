import asyncio
import os

import httpx
from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult
from rich.console import Console
from server import UserInfo  # Import the dataclass from the server file

os.system("clear")


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


client = Client("http://localhost:8000/mcp", elicitation_handler=elicitation_handler)

console = Console()


async def main():
    async with client:

        all_tools = await client.list_tools()
        console.print(all_tools, style="bold green")

        # user info tool
        # result = await client.call_tool("collect_user_info")
        # console.print(result, style="bold blue")

        # simple action
        result = await client.call_tool("accept_tool")
        console.print(result, style="bold magenta")


os.system("clear")

asyncio.run(main())
