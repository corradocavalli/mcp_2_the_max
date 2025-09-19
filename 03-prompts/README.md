# Prompts - MCP Prompts Example

Demonstrates how to create parameterized message templates for LLMs using MCP prompts.

## Server Configuration

**Basic Setup**: Simple FastMCP server named "PromptServer" without complex configuration options.

## Available Prompts

### Basic Prompts
- `ask_about_topic(topic)` - Generates a user message asking for explanation of a topic
- `generate_code_request(language, task_description)` - Creates code generation request with specific language and task
- `conversation_prompt(character, situation)` - Sets up roleplay scenario with multi-message exchange

### Advanced Metadata Prompt
- `analyze_data_request(data_uri, analysis_type)` - Demonstrates comprehensive prompt configuration:

```python
@mcp.prompt(
    name="analyze_data_request",  # Custom prompt name
    description="Creates a request to analyze data with specific parameters",
    tags={"analysis", "data"},  # Categorization tags
    meta={"version": "1.1", "author": "data-team"},  # Custom metadata
)
def data_analysis_prompt(
    data_uri: str = Field(description="The URI of the resource containing the data."),
    analysis_type: str = Field(default="summary", description="Type of analysis."),
) -> str:
```

## Client Behavior

- Lists all available prompts from the server
- Gets `ask_about_topic` prompt with topic "pizza"
- Gets `conversation_prompt` with character "Ford" and time traveler situation

## Key Learning Points

- **Prompt Templates** - Parameterized message generation for LLMs
- **Message Types** - String vs PromptMessage vs PromptResult returns
- **Multi-message Prompts** - Creating conversation flows with multiple messages
- **Parameter Validation** - Using Pydantic Field for parameter descriptions and defaults
- **Prompt Metadata** - Names, descriptions, tags, and custom metadata
- **Role Management** - Specifying user/assistant roles in message exchanges