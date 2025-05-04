# --- MCP Server Dockerfile ---
# IMAGE OPTIONS (choose one by editing the FROM line below):
# 1. Official Python (default, recommended for custom/secure builds)
#    FROM python:3.11-slim AS base
# 2. Prebuilt FastMCPServer: jayprasad10/fastmcpserver:latest
#    FROM jayprasad10/fastmcpserver:latest AS fastmcp-prebuilt
# 3. Hardened FastAPI by Demisto (Verified Publisher): demisto/fastapi:latest
#    FROM demisto/fastapi:latest AS demisto-fastapi
# See: https://hub.docker.com/r/demisto/fastapi
# See: https://hub.docker.com/r/jayprasad10/fastmcpserver

FROM python:3.11-slim AS base
FROM jayprasad10/fastmcpserver:latest AS fastmcp-prebuilt
FROM demisto/fastapi:latest AS demisto-fastapi

# Set working directory
WORKDIR /app

# Install dependencies (update path if requirements.txt is elsewhere)
COPY ../../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Ensure all required third-party dependencies for server.py are present
# (fastapi, fastmcp, pillow)
RUN pip install --no-cache-dir fastapi fastmcp pillow

# Copy MCP server code
COPY ../../ .

# Optional: Copy mcp-server-ssl.conf for HTTPS support (if present)
# COPY docker/mcp-server-ssl.conf ./mcp-server-ssl.conf

# Expose MCP server port (default 8000, can be overridden)
EXPOSE ${MCP_SERVER_PORT:-8000}
EXPOSE ${MCP_SERVER_HTTPS_PORT:-8443}

# Health check (customize as needed for your app)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:${MCP_SERVER_PORT:-8000}/docs || exit 1

# Entrypoint (can be overridden by docker-compose)
CMD ["python", "-u", "server.py"]

# --- USAGE NOTES ---
# - Default build uses python:3.11-slim for maximum control and security.
# - To use jayprasad10/fastmcpserver or demisto/fastapi as your base, comment out the default FROM and uncomment the desired image above.
# - All dependencies for server.py (importlib, os, pkgutil, sys, io, fastapi, fastmcp, pillow) are installed.
# - See Docker Hub for more info:
#   https://hub.docker.com/r/jayprasad10/fastmcpserver
#   https://hub.docker.com/r/demisto/fastapi
# - For production, always review the security and update policies of any base image you use.