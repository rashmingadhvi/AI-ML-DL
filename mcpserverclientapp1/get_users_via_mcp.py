import asyncio
from fastmcp import Client


async def main():
    # Connect to the FastMCP HTTP server
    async with Client("http://localhost:9000/mcp") as client:
        # Call the get_users tool
        result = await client.call_tool("get_users", {})
        print("User data from MCP server:")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
