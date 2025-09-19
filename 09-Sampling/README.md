# Sampling - MCP LLM Sampling Example

Demonstrates how MCP servers can request LLM text generation from clients, enabling server-driven AI workflows and orchestration patterns.

## Server Configuration

**LLM Sampling**: Allows servers to send messages to clients requesting LLM elaboration, but since it's just a request sent to the client, it opens possibilities for server orchestration and distributed AI workflows.

**Orchestration Potential**:
- **Server-Driven AI** - Servers can leverage client-side LLM capabilities
- **Distributed Processing** - AI workloads distributed between server and client
- **Workflow Orchestration** - Servers can coordinate complex multi-step AI processes
- **Resource Optimization** - Utilize client-side AI resources when available

## Available Tools

### AI-Powered Tool
- `creative_writing(topic)` - Generates creative content using client's LLM:

```python
@mcp.tool
async def creative_writing(topic: str, ctx: Context) -> str:
    """Generate creative content using a specific model."""
    response = await ctx.sample(
        system_prompt="You are a creative writing assistant.",
        messages=f"Write a creative short story about {topic}",
        model_preferences="claude-3-sonnet",  # Prefer specific model
        include_context="thisServer",  # Use server context
        temperature=0.9,  # High creativity
        max_tokens=1000,
    )
    return response.text
```

**Sampling Parameters**:
- **System Prompt** - Role definition for the LLM
- **Model Preferences** - Request specific AI models
- **Temperature** - Control creativity/randomness
- **Context Inclusion** - Server context awareness
- **Token Limits** - Response length control

## Client Behavior

- Implements `sampling_handler` to process server sampling requests
- Receives and displays sampling messages and parameters
- Analyzes message structure (role, content, type)
- Calls `creative_writing` with topic "Switzerland"
- Returns mock LLM response to demonstrate the flow

## Key Learning Points

- **Server-to-Client AI Requests** - Servers can request LLM processing from clients
- **LLM Parameter Control** - Fine-tuned control over AI generation parameters
- **Distributed AI Architecture** - AI capabilities distributed across client-server boundary
- **Orchestration Patterns** - Foundation for complex AI workflow coordination
- **Resource Utilization** - Leverage client-side AI resources and models
- **Flexible AI Integration** - Servers don't need their own LLM capabilities