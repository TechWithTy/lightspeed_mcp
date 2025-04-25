"""
A tool demonstrating Pydantic model input for complex argument schemas.
"""

from fastmcp import mcp
from pydantic import BaseModel


class NotificationInput(BaseModel):
    user_id: int
    message: str
    notify: bool = True


@mcp.tool()
def send_notification(input: NotificationInput) -> dict:
    """Send a notification to a user if requested."""
    if input.notify:
        # Simulate sending notification
        return {"status": "sent", "user_id": input.user_id, "message": input.message}
    return {"status": "skipped", "user_id": input.user_id}
