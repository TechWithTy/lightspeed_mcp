"""
MCP tool demonstrating progress reporting for long-running image processing.
"""
import time

from fastmcp import Context, mcp


@mcp.tool()
async def simulate_long_image_processing(image_path: str, ctx: Context) -> str:
    """Simulate a long-running image processing task with progress updates."""
    total_steps = 5
    for i in range(total_steps):
        # Simulate work
        time.sleep(0.5)
        await ctx.report_progress(i + 1, total_steps)
        await ctx.info(f"Step {i+1}/{total_steps} complete.")
    return f"Finished processing {image_path} in {total_steps} steps."
