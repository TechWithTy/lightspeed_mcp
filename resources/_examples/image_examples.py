"""
Resources providing example images and descriptions for testing/demo.
"""
from fastmcp import mcp

@mcp.resource("image://example-url")
def get_example_image_url() -> str:
    """Return a sample image URL for demo/testing purposes."""
    return "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"

@mcp.resource("image://example-description")
def get_example_image_description() -> str:
    """Return a sample image description."""
    return "A demonstration image with a checkerboard background to show transparency."
