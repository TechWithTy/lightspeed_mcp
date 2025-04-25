"""
Resources for image metadata and supported formats.
"""
from fastmcp import mcp

@mcp.resource("image://supported-formats")
def get_supported_image_formats() -> list[str]:
    """Return a list of supported image file formats."""
    return ["jpeg", "png", "gif", "bmp", "tiff", "webp"]

@mcp.resource("image://example-metadata")
def get_example_image_metadata() -> dict:
    """Return an example image metadata dictionary."""
    return {
        "format": "jpeg",
        "mode": "RGB",
        "size": [1920, 1080],
        "info": {"dpi": (72, 72), "compression": "baseline"},
    }
