"""
FastMCP Server for Model Context Protocol

- Exposes tools and resources for LLM/MCP interaction
- Integrates FastAPI via OpenAPI spec using FastMCP's from_fastapi
- Type-checked, documented, and ready for extension
"""

import importlib
import os
import pkgutil
import sys
from io import BytesIO

from fastapi import FastAPI
from fastmcp import Context, FastMCP, Image
from PIL import Image as PILImage

# Dynamically import your FastAPI app and block certain routes
try:
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
    app_module = importlib.import_module("app.api.main")
    fastapi_app: FastAPI = app_module.app

    # Remove/block routes starting with /system, /service, or /mcp_deny
    blocked_prefixes = ("/system", "/service", "/mcp_deny")
    routes_to_keep = []
    for route in fastapi_app.router.routes:
        if not any(str(route.path).startswith(prefix) for prefix in blocked_prefixes):
            routes_to_keep.append(route)
    fastapi_app.router.routes = routes_to_keep

except Exception as e:
    fastapi_app = None
    print(f"Warning: Could not import FastAPI app for OpenAPI integration: {e}")

# --- Dynamically import all modules in specified subpackages for MCP registration ---
def import_all_modules_recursively(package_path, package_name):
    # Skip entire _examples folders
    if os.path.basename(package_path).startswith("_examples"):
        return
    for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
        # Skip modules or packages that start with _example or _examples
        if module_name.startswith("_example") or module_name.startswith("_examples"):
            continue
        full_module_name = f"{package_name}.{module_name}"
        try:
            importlib.import_module(full_module_name)
        except Exception as e:
            print(f"Warning: Could not import {full_module_name}: {e}")
        if is_pkg:
            sub_path = os.path.join(package_path, module_name)
            import_all_modules_recursively(sub_path, full_module_name)

# Import all submodules in tools, prompts, and resources recursively (not just image)
base_dir = os.path.dirname(__file__)
import_all_modules_recursively(os.path.join(base_dir, "tools"), "app.model_context_protocol.tools")
import_all_modules_recursively(os.path.join(base_dir, "prompts"), "app.model_context_protocol.prompts")
import_all_modules_recursively(os.path.join(base_dir, "resources"), "app.model_context_protocol.resources")

# Use FastMCP OpenAPI integration if FastAPI app is available
if fastapi_app is not None:
    mcp = FastMCP.from_fastapi(fastapi_app, name="Fast Supabase MCP Server")
else:
    mcp = FastMCP("Fast Supabase MCP Server")


@mcp.tool()
def add(a: int, b: int, ctx: Context = None) -> Image:
    """Add two numbers, return result as an annotated Image (demo purpose)."""
    result = a + b
    # For demo: create a 1x1 white PNG with result in metadata

    img = PILImage.new("RGB", (1, 1), (255, 255, 255))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    image_result = Image(data=buffer.getvalue(), format="png", info={"sum": result})
    if ctx:
        ctx.info(f"Addition result: {result}")
    return image_result


@mcp.resource("config://app-version")
def get_app_version(ctx: Context = None) -> str:
    """Returns the application version."""
    if ctx:
        ctx.info("Returning app version v1.0.0")
    return "v1.0.0"


if __name__ == "__main__":
    # Allow host/port override via environment variables
    import os
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    mcp.run(host=host, port=port)
