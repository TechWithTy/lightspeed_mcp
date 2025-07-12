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
from fastmcp import Context, FastMCP
from fastmcp.utilities.types import Image
from PIL import Image as PILImage
import logging
logging.basicConfig(level=logging.DEBUG)

import os
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["FASTMCP_TELEMETRY_ENABLED"] = "false"

# Dynamically import your FastAPI app and block certain routes
try:
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
    app_module = importlib.import_module("app.main")
    fastapi_app: FastAPI = app_module.app

    # Remove/block sensitive routes for security
    # Block authentication, user management, admin, debug, and other sensitive endpoints
    blocked_prefixes = (
        "/system", "/service", "/mcp_deny",  # Original blocks
        "/login", "/auth",  # Authentication routes
        "/users", "/user",  # User management routes  
        "/password-recovery", "/reset-password",  # Password reset routes
        "/debug", "/admin",  # Debug and admin routes
        "/messaging",  # Internal messaging
        "/metrics",  # Metrics endpoints
        "/private",  # Private endpoints
    )
    
    # Also block specific sensitive patterns
    blocked_patterns = [
        "signup", "password", "token", "admin", "debug", 
        "superuser", "delete", "reset", "recovery"
    ]
    
    routes_to_keep = []
    for route in fastapi_app.router.routes:
        route_path = str(route.path).lower()
        
        # Check blocked prefixes
        if any(route_path.startswith(prefix) for prefix in blocked_prefixes):
            continue
            
        # Check blocked patterns in the path
        if any(pattern in route_path for pattern in blocked_patterns):
            continue
            
        # Block HTTP methods that modify data for security
        if hasattr(route, 'methods'):
            if any(method in ['DELETE', 'PUT', 'PATCH'] for method in route.methods):
                continue
        
        routes_to_keep.append(route)
    
    fastapi_app.router.routes = routes_to_keep
    print(f"MCP Server: Blocked {len(fastapi_app.router.routes) - len(routes_to_keep)} sensitive routes")
    print(f"MCP Server: Keeping {len(routes_to_keep)} safe routes")

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
mcp = None
if fastapi_app:
    try:
        # Try to rebuild models to ensure they're fully defined
        print("Rebuilding Pydantic models for MCP server...")
        from app.models import User, Item, UserCreate, ItemCreate, UserUpdate, ItemUpdate
        for model in [User, Item, UserCreate, ItemCreate, UserUpdate, ItemUpdate]:
            try:
                model.model_rebuild()
            except Exception as e:
                print(f"Warning: Could not rebuild {model.__name__}: {e}")
        
        mcp = FastMCP.from_fastapi(fastapi_app, name="Fast Supabase MCP Server")
        print("MCP Server integrated with FastAPI successfully")
    except Exception as e:
        print(f"Warning: Could not integrate FastAPI with MCP server: {e}")
        print("Creating standalone MCP server...")
        mcp = FastMCP(name="Fast Supabase MCP Server")
else:
    mcp = FastMCP(name="Fast Supabase MCP Server")



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
    try:
        # Use environment variables for host/port configuration
        # For Render deployment, use 0.0.0.0 and PORT from environment
        host = os.getenv("MCP_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_PORT", os.getenv("PORT", 8000)))
        
        print(f"Starting MCP server on {host}:{port}")
        mcp.run(transport="http", host=host, port=port)
        print("This should never print — server should block here.")
    except Exception as e:
        print(f"ERROR: Failed to start MCP server: {e}")
        import traceback
        traceback.print_exc()
