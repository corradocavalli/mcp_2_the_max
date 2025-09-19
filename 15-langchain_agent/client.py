import asyncio
import os
from typing import Dict, List

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult
from fastmcp.client.sampling import RequestContext, SamplingMessage, SamplingParams
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field, create_model
from rich.console import Console
from triage_server import ServerMessage

load_dotenv()

os.system("clear")
console = Console()


class DynamicMCPTool(BaseTool):
    """Dynamically generated LangChain tool from MCP server tool."""

    client: Client = Field(exclude=True)
    tool_name: str

    def __init__(
        self,
        client: Client,
        lc_tool: BaseModel,
    ):
        # Extract tool information from MCP server
        tool_name = lc_tool.name
        description = lc_tool.description

        super().__init__(
            name=tool_name,
            description=description,
            client=client,
            tool_name=tool_name,
            args_schema=(
                lc_tool.args_schema if hasattr(lc_tool, "args_schema") else None
            ),
        )

    async def _arun(self, **kwargs) -> str:
        """Async implementation of the tool."""
        try:
            console.print(
                f"\n🔧 LLM invoked tool: '{self.tool_name}' with args: {kwargs}\n",
                style="dim yellow",
            )
            async with self.client:
                result = await self.client.call_tool(self.tool_name, kwargs)
                console.print(
                    f"\n✅ Tool '{self.tool_name}' completed successfully\n",
                    style="dim yellow",
                )
                return result.content[0].text if result.content else str(result.data)
        except Exception as e:
            console.print(
                f"❌ Tool '{self.tool_name}' failed: {str(e)}\n",
                style="red",
            )
            return f"Error calling tool {self.tool_name}: {str(e)}"

    def _run(self, **kwargs) -> str:
        """Sync wrapper for async implementation."""
        return asyncio.run(self._arun(**kwargs))


class MCPLangChainAdapter:
    """Adapter that dynamically converts MCP servers to LangChain tools."""

    def __init__(self):
        self.clients: Dict[str, Client] = {}

    async def get_all_tools(self) -> List[DynamicMCPTool]:
        """Dynamically generate LangChain tools from all connected MCP servers."""
        tools = []

        for server_name, client in self.clients.items():
            try:
                async with client:
                    lc_tools = await load_mcp_tools(client.session)

                    for lc_tool in lc_tools:
                        # Create a dynamic LangChain tool that wraps the associated client
                        dynamic_tool = DynamicMCPTool(
                            client=client,
                            lc_tool=lc_tool,
                        )
                        tools.append(dynamic_tool)

                        console.print(
                            f"✅ Loaded tool '{lc_tool.name}' from server '{server_name}'",
                            style="green",
                        )

            except Exception as e:
                console.print(
                    f"❌ Failed to load tools from server '{server_name}': {e}",
                    style="red",
                )

        return tools


class MCPSamplingHandler:
    """Handles sampling requests from the triage server."""

    def __init__(self, trader_client: Client):
        self.trader_client = trader_client

    async def __call__(
        self,
        messages: List[SamplingMessage],
        params: SamplingParams,
        context: RequestContext,
    ) -> str:
        """Handle sampling requests from triage server."""
        try:
            # Parse the server message
            server_message = ServerMessage.model_validate_json(messages[0].content.text)

            console.print(
                f"\n*Request transferred from Triage server to Trader server*\n",
                style="yellow",
            )

            # Route to appropriate trader tool
            async with self.trader_client:
                if server_message.action == "buy":
                    response = await self.trader_client.call_tool(
                        "buy",
                        {
                            "stock": server_message.stock,
                            "quantity": server_message.quantity,
                        },
                    )
                elif server_message.action == "sell":
                    response = await self.trader_client.call_tool(
                        "sell",
                        {
                            "stock": server_message.stock,
                            "quantity": server_message.quantity,
                        },
                    )
                else:
                    return f"Unknown action: {server_message.action}"

                return (
                    response.content[0].text if response.content else str(response.data)
                )

        except Exception as e:
            return f"Error processing sampling request: {str(e)}"


class ProgressHandler:
    """Handles progress updates from the LangChain agent."""

    async def __call__(self, progress: float, total: float | None, message: str | None):
        """Handle progress updates."""
        percentage = (progress / total) * 100
        console.print(f"{percentage:.1f}% - {message}", style="dim yellow")


class MCPElicitationHandler:
    """Handles elicitation requests from the trader server."""

    async def __call__(self, message: str, response_type: type, params, context):
        """Handle elicitation requests from trader server."""
        console.print(f"{message}", style="bold cyan")
        user_input = input("Confirm? (yes/no): ")

        if user_input.lower() in ["yes", "y"]:
            return ElicitResult(action="accept")
        else:
            return ElicitResult(action="cancel")


async def main():
    """Main function demonstrating dynamic MCP to LangChain integration."""

    console.print("=" * 60, style="white")
    console.print("🚀 Dynamic MCP + LangChain Stock Trading Agent", style="bold blue")
    console.print("=" * 60, style="white")

    try:
        # Create single client instances with proper handlers
        trader_client = Client(
            "http://localhost:9000/mcp",
            elicitation_handler=MCPElicitationHandler(),
            progress_handler=ProgressHandler(),
        )

        triage_client = Client(
            "http://localhost:8000/mcp",
            sampling_handler=MCPSamplingHandler(trader_client),
        )

        # Create the adapter and add the pre-configured clients
        adapter = MCPLangChainAdapter()
        adapter.clients["triage"] = triage_client
        adapter.clients["trader"] = trader_client

        # Dynamically generate all tools
        console.print("\n🔍 Discovering tools from MCP servers...", style="blue")
        tools = await adapter.get_all_tools()

        # Initialize Azure OpenAI LLM
        llm = AzureChatOpenAI(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_BASE_URL"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.1,
        )

        # Get system prompt from triage MCP server
        async with triage_client:
            system_prompt = await triage_client.get_prompt(
                "trader_system_prompt", {"stocks": ["MSFT", "AAPL"]}
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt.messages[0].content.text,
                ),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Create LangChain agent with dynamically discovered tools
        agent = create_openai_tools_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=False,
            handle_parsing_errors=True,
            max_execution_time=60,
        )

        console.print(
            "\nYou can now enter stock trading commands or 'q' to exit",
            style="bold blue",
        )

        while True:
            try:
                user_input = input("\n👤 You: ('q' to exit) ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    break

                if user_input.strip():
                    result = await agent_executor.ainvoke({"input": user_input})
                    console.print(f"🤖 Agent: {result['output']}", style="bold green")

            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"❌ Error: {str(e)}", style="bold red")

        console.print("\n👋 Goodbye!", style="bold blue")

    except Exception as e:
        console.print(f"❌ Failed to initialize: {str(e)}", style="bold red")


if __name__ == "__main__":
    asyncio.run(main())
