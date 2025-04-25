"""
MCP tool demonstrating LLM sampling via ctx.sample for image captioning.
"""
from typing import Optional

from fastmcp import Context, mcp


@mcp.tool()
async def llm_caption_with_sampling(image_description: str, ctx: Context | None = None) -> str:
    """Generate an image caption by requesting a completion from the client LLM."""
    prompt = f"Write a creative caption for this image: {image_description}"
    if ctx:
        response = await ctx.sample(prompt, system_prompt="You are a witty visual storyteller.")
        return response.text if hasattr(response, 'text') else str(response)
    return "No LLM context available."
