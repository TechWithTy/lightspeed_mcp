"""
Prompt demonstrating multi-message format for advanced LLM guidance.
"""
from fastmcp import mcp
from fastmcp.prompts.base import AssistantMessage, UserMessage


@mcp.prompt()
def review_image_prompt(image_context: str):
    """Prompt for a multi-turn code review of an image context."""
    return [
        UserMessage(f"Here is image context: {image_context}"),
        AssistantMessage("What specific feedback do you want about this image?")
    ]
