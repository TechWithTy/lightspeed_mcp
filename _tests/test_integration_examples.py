"""
Integration/E2E test for MCP server: calls all demo endpoints and checks output.
"""

import pytest
from fastmcp import Client


@pytest.mark.asyncio
async def test_context_kitchen_sink_demo():
    async with Client("../tools/context_kitchen_sink_demo.py") as client:
        result = await client.call_tool(
            "context_kitchen_sink_demo", {"uri": "test://resource"}
        )
        assert "resource_content" in result
        assert "llm_sample" in result
        assert "all_ctx_attributes" in result


@pytest.mark.asyncio
async def test_user_dynamic_resource():
    async with Client("../resources/user_dynamic_resource.py") as client:
        result = await client.read_resource("user://42")
        assert result["user_id"] == "42"
        assert "Hello" in result["message"]


@pytest.mark.asyncio
async def test_send_notification():
    async with Client("../tools/pydantic_input_demo.py") as client:
        result = await client.call_tool(
            "send_notification",
            {"input": {"user_id": 123, "message": "Hi!", "notify": True}},
        )
        assert result["status"] == "sent"
        assert result["user_id"] == 123
        assert result["message"] == "Hi!"
