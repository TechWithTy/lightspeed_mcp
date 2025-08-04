import pytest
import asyncio
from fastmcp import Client
from PIL import Image as PILImage
from io import BytesIO

@pytest.mark.asyncio
async def test_add_tool():
    """Test the add tool directly using a Client connected to the MCP server."""
    # Connect to the running MCP server
    server_url = "http://localhost:8000"  # Adjust if using a different port
    
    async with Client(server_url) as client:
        # Call the add tool with test parameters
        result = await client.call_tool("add", {"a": 5, "b": 7})
        
        # The result should be an Image with metadata
        assert result[0].format == "png"
        assert "sum" in result[0].info
        assert result[0].info["sum"] == 12
        
        # Verify the image data can be loaded
        image_data = BytesIO(result[0].data)
        img = PILImage.open(image_data)
        assert img.size == (1, 1)
        
        print("✅ MCP 'add' tool test passed!")

# For direct execution
if __name__ == "__main__":
    asyncio.run(test_add_tool())