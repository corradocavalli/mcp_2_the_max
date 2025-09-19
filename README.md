# MCP 2 the Max 🚀

A comprehensive collection of code snippets and examples used during Model Context Protocol (MCP) investigation and exploration. This repository serves as a practical learning resource for understanding and implementing various MCP features through hands-on examples.

## Prerequisites

**📋 Basic MCP Knowledge Assumed**: This repository assumes you have basic familiarity with the Model Context Protocol concepts, architecture, and terminology. If you're new to MCP, we recommend first reading the [Model Context Protocol Specification](https://modelcontextprotocol.io/docs/getting-started/intro) to understand the foundational concepts.

## Overview

This repository contains a curated set of simple, focused examples that demonstrate different aspects and capabilities of the Model Context Protocol. Each folder represents a specific feature or concept, allowing you to explore MCP functionality incrementally and understand how different components work together.

## Why FastMCP?

To accelerate development and shield away from unnecessary complexity, all examples use the **FastMCP library**. FastMCP dramatically simplifies MCP usage by providing:

- 🎯 **Simplified API** - Intuitive decorators and patterns
- ⚡ **Rapid Development** - Less boilerplate, more functionality
- 🛡️ **Built-in Best Practices** - Error handling, type safety, and validation
- 🔧 **Developer Experience** - Rich tooling and debugging capabilities

This allows you to focus on learning MCP concepts rather than wrestling with implementation details.

For more information about FastMCP, visit the [FastMCP Getting Started Guide](https://gofastmcp.com/getting-started/welcome).

## Quick Start

### Prerequisites

Make sure you have Python 3.12+ and [`uv`](https://github.com/astral-sh/uv) installed.

### General Usage Pattern

Each example folder follows the same pattern for easy testing:

1. **Start the MCP Server**
   ```bash
   cd [folder-name]
   uv run server.py
   ```
   
2. **Run the Client** (in a new terminal)
   ```bash
   cd [folder-name]
   uv run client.py
   ```

The server will typically run on `http://localhost:8000/mcp` and provide various MCP tools, resources, or prompts that the client can interact with.

## Repository Structure

| Folder | Goal & Learning Objectives |
|--------|-------------|
| **01-tools** | **Basic Tools & Configuration** - Learn fundamental MCP tool creation, duplication handling, tag-based filtering, and LLM annotations. Master structured outputs, type safety, and behavioral hints for optimal LLM interaction. |
| **01b-routes** | **Custom HTTP Endpoints** - Explore custom route handling beyond standard MCP patterns, demonstrating direct HTTP endpoint creation for specialized server behaviors. |
| **02-resources** | **Resource Management** - Understand MCP's resource system for serving files, templates, and dynamic content. Learn MIME type handling, binary data serving, and resource metadata management. |
| **03-prompts** | **Dynamic Prompt Templates** - Master prompt template creation with variable substitution, argument validation, and structured prompt generation for consistent LLM interactions. |
| **04-context** | **Context & State Management** - Explore how MCP servers maintain context across requests, manage session state, and provide contextual information to tools and resources. |
| **05-composition** | **Multi-Server Architecture** - Learn to compose multiple MCP servers together, enabling distributed functionality and specialized service coordination in complex systems. |
| **06-elicitation** | **Interactive User Input** - Implement real-time user interaction patterns within MCP workflows, including confirmation dialogs, data collection, and dynamic user-driven decision making. |
| **07-logging** | **Remote Logging & Monitoring** - Set up comprehensive logging systems where MCP servers can send structured logs to clients for monitoring, debugging, and audit trails. |
| **08-progress** | **Long-Running Operations** - Handle extended operations with progress reporting, status updates, and user feedback for tasks that require time to complete. |
| **09-sampling** | **LLM Orchestration** - Discover how MCP servers can leverage client-side LLM capabilities through sampling, enabling distributed AI architectures and intelligent server coordination. |
| **10-roots** | **Secure File System Access** - Implement MCP's security model for controlled file system access through client-authorized root directories, ensuring safe server-to-filesystem interactions. |
| **11-azure_auth** | **Enterprise Authentication** - Integrate OAuth2 authentication with Azure Active Directory, demonstrating enterprise-grade security patterns and Microsoft Graph API access. |
| **12-cancellation** | **Graceful Interruption** - Build cancellation-aware tools that can be safely interrupted during long-running operations, with proper cleanup and partial result handling. |
| **13-agentic_flow** | **Server Orchestration** - Create sophisticated multi-server workflows using elicitation and sampling to demonstrate intelligent routing, delegation, and agentic decision-making patterns. |
| **15-langchain_agent** | **Framework Integration** - Integrate MCP with LangChain for advanced agent development, combining MCP's protocol benefits with LangChain's agent ecosystem. |

## Key Features Demonstrated

- 🔧 **Tool Creation & Management** - Define custom tools with annotations, type safety, and LLM guidance
- 📁 **Resource Systems** - Serve files, templates, and dynamic content with proper MIME handling
- 💬 **Prompt Engineering** - Create dynamic, reusable prompt templates with variable substitution
- � **Security Models** - Implement file system access controls and authentication patterns
- 🤖 **Agentic Workflows** - Build intelligent multi-server routing and decision-making systems
- 📊 **Progress & Monitoring** - Track long-running operations with comprehensive logging
- ⚡ **Performance Optimization** - Handle cancellation, async operations, and resource management
- 🔗 **Framework Integration** - Connect MCP with existing tools like LangChain


## Environment Setup

The repository uses `uv` for dependency management. To get started:

```bash
# Clone the repository
git clone https://github.com/corradocavalli/mcp_2_the_max.git
cd mcp_2_the_max

# Install dependencies
uv sync

# Navigate to any example folder and start exploring!
cd 01-tools
uv run server.py
```

### Port Conflicts
If port 8000 is in use, you can modify the port in the server.py files or stop other services using that port.

### Dependencies
Make sure you're in the repository root when running `uv sync` to install all required dependencies.

## Contributing

This repository is designed for learning and experimentation. Feel free to:
- Add new examples
- Improve existing ones
- Fix bugs or issues
- Enhance documentation

## Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP GitHub Repository](https://github.com/jlowin/fastmcp)

---

**Happy exploring! 🎉**

Each example is self-contained and ready to run. Start with the basics and work your way up to more advanced concepts as you become comfortable with MCP patterns and capabilities.