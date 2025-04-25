# Model Context Protocol (MCP) Integration Guide

## Overview
This package demonstrates a robust integration between [FastAPI](https://fastapi.tiangolo.com/) and [FastMCP](https://github.com/typpo/fastmcp), enabling dynamic, modular, and scalable LLM/MCP workflows. It features automatic registration of tools, resources, and prompts for seamless extension.

---

## Key Features

- **FastAPI + FastMCP Integration:**
  - Leverages `FastMCP.from_fastapi()` to expose all FastAPI endpoints as MCP resources/tools via OpenAPI.
- **Automatic Discovery & Import:**
  - All Python modules in `tools/image/`, `prompts/image/`, and `resources/` are dynamically imported and registered with MCP at server startup.
  - No manual import maintenance required—just add new modules to the correct folders.
- **Type-Checked, Extensible Design:**
  - All tools, resources, and prompts use Python type hints for clarity and safety.
  - Modular structure supports rapid extension and testing.
- **LLM/Context/Image Support:**
  - Tools/resources can use `Context` for logging, progress, and LLM sampling.
  - `Image` support for image data workflows.

---

## Directory Structure

```
model_context_protocol/
├── server.py                 # Main MCP server, integrates FastAPI and MCP
├── tools/
│   └── image/                # All image-related MCP tools
│       └── ...
├── prompts/
│   └── image/                # All image-related MCP prompts
│       └── ...
├── resources/                # All MCP resources
│   └── ...
```

---

## How Integration Works

### 1. **FastAPI + FastMCP**
- `server.py` imports your FastAPI app and passes it to `FastMCP.from_fastapi`, exposing all FastAPI endpoints as MCP tools/resources.

### 2. **Automatic Module Import**
- At startup, `server.py` uses `pkgutil` and `importlib` to dynamically import **all** modules in:
  - `tools/image/`
  - `prompts/image/`
  - `resources/`
- This ensures that any MCP-decorated function (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`) in these modules is auto-registered with the MCP server.
- **To add new functionality:** just drop a `.py` file with MCP-decorated functions into the appropriate folder—no need to edit `server.py`.

### 3. **Context, Image, and Advanced Features**
- Tools/resources can use `Context` for:
  - Logging (`ctx.info`, `ctx.error`)
  - Progress reporting (`ctx.report_progress`)
  - LLM sampling (`ctx.sample`)
- Support for `Image` return types for image workflows.

---

## Example: Adding a New Tool

1. Create a new file in `tools/image/`, e.g. `resize_tool.py`:
   ```python
   from fastmcp import mcp

   @mcp.tool()
   def resize_image(image_path: str, width: int, height: int) -> str:
       """Resize an image and return the new file path."""
       # ... your logic here ...
       return new_path
   ```
2. Restart your MCP server. The new tool will be auto-registered and available to all MCP clients.

---

## Advanced Usage
- **LLM Sampling:** Use `await ctx.sample(...)` in tools/resources to request completions from the client LLM.
- **Progress Reporting:** Use `await ctx.report_progress(current, total)` for long-running tasks.
- **Multi-message Prompts:** Return a list of `UserMessage`/`AssistantMessage` in prompt modules for richer LLM guidance.
- **Server Composition/Proxy:** See example modules for mounting or proxying other MCP servers.

---

## Requirements
- Python 3.9+
- `fastapi`, `fastmcp`, and dependencies installed in your environment.

---

## Contributing
- Follow DRY, SOLID, and clean code principles.
- Use type hints, write tests, and document your tools/resources.

---

## Credits
- Inspired by [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) and [The Clean Coder](https://www.oreilly.com/library/view/the-clean-coder/9780132542913/).
- Built with ❤️ by Ty the Programmer.
