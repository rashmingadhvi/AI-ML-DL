"""
fastmcp.py
-------------
A simple MCP server implementation using FastMCP v2 that exposes a single tool to fetch user data from a Node.js microservice.

This server demonstrates how to use FastMCP for rapid development of MCP-compatible tool servers.
"""

import json
import httpx
from fastmcp import FastMCP

# Initialize the FastMCP server with HTTP transport
mcp = FastMCP(
    name="user-data-mcp-server"
)

@mcp.tool
def get_users() -> str:
    """
    Fetch user data from the Node.js microservice.

    Makes an HTTP GET request to the local microservice running on port 3000
    and returns the user data as a formatted JSON string.

    Returns:
        str: User data as a pretty-printed JSON string, or error message.
    """
    try:
        # httpx can be used synchronously here for simplicity
        response = httpx.get("http://localhost:3000/users")
        response.raise_for_status()
        users = response.json()
        return json.dumps(users, indent=2)
    except Exception as e:
        return f"Error fetching users: {str(e)}"

if __name__ == "__main__":
    # Run as HTTP server on port 9000
    mcp.run(transport="streamable-http", host="localhost", port=9000)
