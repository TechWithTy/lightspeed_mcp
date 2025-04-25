"""
Advanced image-related prompts for FastMCP.
"""
from fastmcp import mcp
from fastmcp.prompts.base import AssistantMessage, UserMessage


@mcp.prompt()
def ask_for_image_resize() -> str:
    """Prompt for resizing an image."""
    return "Specify the new width and height for the image."

@mcp.prompt()
def ask_for_grayscale_conversion() -> str:
    """Prompt for converting an image to grayscale."""
    return "Would you like to convert the image to grayscale? Reply yes or no."

@mcp.prompt()
def ask_for_metadata_extraction() -> list:
    """Prompt for extracting metadata from an image."""
    return [
        UserMessage("Would you like to see the metadata for this image?"),
        AssistantMessage("I can extract format, mode, size, and additional info from the file.")
    ]
