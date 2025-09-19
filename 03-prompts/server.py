# Prompts provide parameterized message templates for LLMs


import json

from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent
from pydantic import Field

mcp = FastMCP(name="PromptServer")


# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt
def ask_about_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"Can you please explain the concept of '{topic}'?"


# Prompt returning a specific message type
@mcp.prompt
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """Generates a user message requesting code generation."""
    content = f"Write a {language} function that performs the following task: {task_description}"
    return PromptMessage(role="user", content=TextContent(type="text", text=content))


@mcp.prompt(
    name="analyze_data_request",  # Custom prompt name
    description="Creates a request to analyze data with specific parameters",  # Custom description
    tags={"analysis", "data"},  # Optional categorization tags
    meta={"version": "1.1", "author": "data-team"},  # Custom metadata
)
@mcp.prompt(
    name="analyze_data_request",  # Custom prompt name
    description="Creates a request to analyze data with specific parameters",  # Custom description
    tags={"analysis", "data"},  # Optional categorization tags
    meta={"version": "1.1", "author": "data-team"},  # Custom metadata
)
def data_analysis_prompt(
    data_uri: str = Field(description="The URI of the resource containing the data."),
    analysis_type: str = Field(default="summary", description="Type of analysis."),
) -> str:
    """This docstring is ignored when description is provided."""
    return (
        f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."
    )


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)
