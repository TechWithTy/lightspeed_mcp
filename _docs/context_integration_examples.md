# MCP Context Integration & Reproducibility Examples

This document explains the implementation and testing of advanced Model Context Protocol (MCP) features in this codebase. It describes how to use and verify all core MCP server capabilities, including the Context object, dynamic resources, Pydantic tool inputs, and integration/E2E testing.

---

## 1. Kitchen Sink Context Tool
- **File:** `context/_examples/context_kitchen_sink_demo.py`
- **Purpose:** Demonstrates all major Context features:
  - Logging (`debug`, `info`, `warning`, `error`)
  - Progress reporting at multiple stages
  - Resource access (`await ctx.read_resource`)
  - Access to all available context attributes
  - LLM sampling (`await ctx.sample`)
  - Returns a summary of all context features/values
- **Usage:** Call the tool with a resource URI to see all context features in action.

## 2. Dynamic Resource Template
- **File:** `resources/_examples/user_dynamic_resource.py`
- **Purpose:** Example of a dynamic MCP resource using a URI template (`user://{user_id}`).
- **Usage:** Read the resource with any user ID (e.g., `user://42`) to get a personalized greeting and echo the ID.

## 3. Pydantic Model Input Tool
- **File:** `tools/_examples/pydantic_input_demo.py`
- **Purpose:** Demonstrates using a Pydantic model as a tool input for complex argument schemas.
- **Usage:** Call the tool with a JSON object matching the Pydantic schema.

## 4. Multi-Message Prompt
- **Files:** `prompts/image/_examples/image_prompts.py`, `prompts/image/_examples/advanced_image_prompts.py`
- **Purpose:** Shows how to return a list of `UserMessage`/`AssistantMessage` objects for richer LLM guidance.

## 5. Integration/E2E Test
- **File:** `_tests/test_integration_examples.py`
- **Purpose:** Uses `pytest` and `fastmcp.Client` to call each demo endpoint and check output for correctness and reproducibility.
- **Tests:**
  - `test_context_kitchen_sink_demo`: Calls the kitchen sink tool and checks for all features in the result.
  - `test_user_dynamic_resource`: Reads the dynamic resource and checks the greeting and user ID.
  - `test_send_notification`: Calls the Pydantic-input tool and checks the notification logic.

---

## How to Use
1. **Start your MCP server** (ensure all demo files are present in their respective `_examples` folders).
2. **Run the integration tests** with `pytest _tests/test_integration_examples.py`.
3. **Review the code in each demo for reference on best-practice MCP server design.**

---

## Why This Matters
These examples ensure your MCP server is fully reproducible, testable, and demonstrates all advanced features of FastMCP and the Model Context Protocol. They serve as both a reference and a test suite for robust, production-grade MCP development.
