# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY ../../../../requirements.txt ./
RUN uv pip install --no-cache-dir -r requirements.txt

# Ensure FastMCP and FastAPI are installed, regardless of requirements.txt
RUN uv pip install --no-cache-dir fastmcp fastapi

# Copy the MCP server code
COPY . .

# Set default envs for host/port, can be overridden by Docker Compose or .env
ENV MCP_SERVER_HOST=0.0.0.0
ENV MCP_SERVER_PORT=8000

# Expose port (default FastAPI/uvicorn port)
EXPOSE 8000

# Entrypoint to run the MCP server
CMD ["python", "server.py"]
