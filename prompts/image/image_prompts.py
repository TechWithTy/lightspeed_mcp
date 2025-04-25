"""
Prompts for image processing and creative tasks using FastMCP.
"""
from fastmcp.prompts.base import UserMessage, AssistantMessage
from fastmcp import mcp

@mcp.prompt()
def ask_for_image_description() -> str:
    """Prompt for describing an image."""
    return "Please describe the image you want to process or analyze."

@mcp.prompt()
def creative_image_edit_prompt(image_type: str) -> str:
    """Prompt for creative editing of a given image type."""
    return f"Describe how you would like to edit the {image_type} image."

@mcp.prompt()
def ask_for_caption(image_context: str) -> list:
    """Prompt for generating a caption for an image given its context."""
    return [
        UserMessage(f"Here is the context: {image_context}"),
        AssistantMessage("Please provide a creative caption for the image.")
    ]
