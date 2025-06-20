import asyncio
import json
import httpx
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl


server = Server("user-data-server")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_users",
            description="Fetch user data from the Node.js microservice",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_users":
        return await get_users()
    else:
        raise ValueError(f"Unknown tool: {name}")


async def get_users() -> list[TextContent]:
    """
    Fetch user data from the Node.js microservice.
    
    Makes an HTTP GET request to the local microservice running on port 3000
    and returns the user data as JSON.
    
    Returns:
        list[TextContent]: User data from the microservice
        
    Raises:
        Exception: If the microservice is not running or returns an error
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:3000/users")
            response.raise_for_status()
            users = response.json()
            
            return [TextContent(
                type="text",
                text=json.dumps(users, indent=2)
            )]
    except Exception as e:
        return [TextContent(
            type="text", 
            text=f"Error fetching users: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="user-data-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())