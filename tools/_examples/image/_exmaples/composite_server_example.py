"""
Example of MCP server composition/mounting for image tools.
"""

from fastmcp import FastMCP

# Standalone sub-server for watermarking
watermark_mcp = FastMCP("Watermark Service")


@watermark_mcp.tool()
def add_watermark(image_path: str, watermark_text: str) -> str:
    """Stub: Add watermark to image (demo only)."""
    return f"Would add '{watermark_text}' to {image_path}"


# Mount into main server if running as script
if __name__ == "__main__":
    main_mcp = FastMCP("Main Composite")
    main_mcp.mount("watermark", watermark_mcp)
    main_mcp.run()
