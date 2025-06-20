import asyncio
from fastmcp import Client
import json

async def main():
    # Connect to the local MCP server script
    async with Client("fastmcpserver.py") as client:
        # Call the get_users tool (no arguments required)
        result = await client.call_tool("get_users", {})
        print("User data from MCP server:")
        print(result)  # Print the result directly

if __name__ == "__main__":
    asyncio.run(main())
