"""
Example of proxying another MCP server (stub for image tools).
"""
from fastmcp import Client, FastMCP
from fastmcp.client.transports import PythonStdioTransport

# Proxy to a (hypothetical) stdio-based image MCP server
proxy_client = Client(transport=PythonStdioTransport('path/to/image_stdio_server.py'))
proxy = FastMCP.from_client(proxy_client, name="Image Proxy")

if __name__ == "__main__":
    proxy.run(transport='sse')
