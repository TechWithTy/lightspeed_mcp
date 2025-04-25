"""
MCP tool demonstrating roots access for secure file listing.
"""
import os

from fastmcp import Context, mcp


@mcp.tool()
async def list_image_files_in_root(directory_uri: str, ctx: Context) -> list[str]:
    """List image files in a directory, respecting roots access (client must allow)."""
    # In practice, ctx.read_resource or ctx.roots would be used for secure access
    # Here we just simulate a local listing
    try:
        files = os.listdir(directory_uri)
        image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))]
        await ctx.info(f"Found {len(image_files)} image files in {directory_uri}.")
        return image_files
    except Exception as e:
        await ctx.error(f"Error listing files: {e}")
        return []
