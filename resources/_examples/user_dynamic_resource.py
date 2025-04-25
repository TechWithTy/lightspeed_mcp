"""
A dynamic MCP resource template example.
Returns a greeting and echoes the user_id from the URI.
"""
from fastmcp import mcp

@mcp.resource("user://{user_id}")
def get_user_dynamic_resource(user_id: str) -> dict:
    """Return a greeting and echo the user_id from the URI."""
    return {"message": f"Hello, user {user_id}!", "user_id": user_id}
