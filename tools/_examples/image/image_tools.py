"""
FastMCP image processing tools for LLM/MCP interaction.
Extends with additional tools: image resizing, grayscale, and metadata extraction.
"""

from io import BytesIO
from typing import Optional

from fastmcp import Context, Image, mcp

try:
    from PIL import Image as PILImage
except ImportError:
    raise ImportError("Please install the `pillow` library to use image tools.")


@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image file and return as Image object."""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return Image(data=buffer.getvalue(), format="png")


@mcp.tool()
def convert_image_format(image_path: str, format: str = "jpeg") -> Image:
    """Convert an image to a different format (e.g., jpeg, png)."""
    img = PILImage.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format=format.upper())
    return Image(data=buffer.getvalue(), format=format.lower())


@mcp.tool()
def caption_image(image_path: str, ctx: Optional[Context] = None) -> str:
    """Generate a caption for an image using the LLM (delegated to client via ctx.sample)."""
    img = PILImage.open(image_path)
    description = f"Image size: {img.size}, mode: {img.mode}"
    if ctx:
        prompt = f"Generate a creative caption for the following image: {description}"
        response = ctx.sample(prompt)
        return response.text if hasattr(response, "text") else str(response)
    return description


@mcp.tool()
def resize_image(image_path: str, width: int, height: int) -> Image:
    """Resize an image to the specified width and height."""
    img = PILImage.open(image_path)
    img = img.resize((width, height))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return Image(data=buffer.getvalue(), format="png")


@mcp.tool()
def grayscale_image(image_path: str) -> Image:
    """Convert an image to grayscale."""
    img = PILImage.open(image_path).convert("L")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return Image(data=buffer.getvalue(), format="png")


@mcp.tool()
def extract_image_metadata(image_path: str) -> dict:
    """Extract basic metadata from an image file."""
    img = PILImage.open(image_path)
    return {
        "format": img.format,
        "mode": img.mode,
        "size": img.size,
        "info": dict(img.info),
    }
