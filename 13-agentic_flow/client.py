import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult
from fastmcp.client.sampling import RequestContext, SamplingMessage, SamplingParams
from rich.console import Console
from triage_server import ServerMessage

load_dotenv()
os.system("clear")


async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext,
) -> str:

    server_Message = ServerMessage.model_validate_json(messages[0].content.text)
    console.print(
        f"Calling trader server to {server_Message.action.upper()}...\n", style="white"
    )
    if server_Message.action == "buy":
        async with trader:
            response = await trader.call_tool(
                "buy",
                {"stock": server_Message.stock, "quantity": server_Message.quantity},
            )
            console.print(
                "\nResponse from trader server:\n", response, style="bold blue"
            )
            return response.content[0].text

    elif server_Message.action == "sell":
        console.print("Proceeding with SELL order...\n", style="white")
        async with trader:
            response = await trader.call_tool(
                "sell",
                {"stock": server_Message.stock, "quantity": server_Message.quantity},
            )
            console.print(
                "\nResponse from trader server:\n", response, style="bold blue"
            )
            return response.content[0].text
    else:
        raise ValueError(f"Unknown action: {server_Message.action}")


async def elicitation_handler(message: str, response_type: type, params, context):
    if response_type is None:
        console.print(message, style="bold bright_cyan")
        user_input = input("Your response (yes/no): ")
        if user_input == "yes":
            return ElicitResult(action="accept")
        return ElicitResult(action="cancel")

    else:
        console.print("Unsupported response type", style="bold red")
        return ElicitResult(action="cancel")


client = Client(os.getenv("TRIAGE_SERVER_URL"), sampling_handler=sampling_handler)
trader = Client(os.getenv("TRADER_SERVER_URL"), elicitation_handler=elicitation_handler)

console = Console()


async def main():
    async with client:

        console.print("--" * 40, style="white")
        console.print("Listing all available tools...", style="bold white")
        console.print("--" * 40, style="white")

        # List all available tools on TriageServer
        all_tools = await client.list_tools()

        console.print(all_tools, style="bold green")
        console.print("--" * 40, style="white")

        # "Buy/sell" action
        result = await client.call_tool(
            "process_stock_order", {"action": "buy", "stock": "MSFT", "quantity": 10}
        )

        # Display the full response object
        console.print("--" * 40, style="white")
        console.print(result.content[0].text, style="bold cyan")
        console.print("--" * 40, style="white")


os.system("clear")

asyncio.run(main())
