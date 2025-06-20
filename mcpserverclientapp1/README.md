# MCP Server (Python)

This directory contains an MCP server that exposes a tool to fetch user data from the Node.js microservice.

## Prerequisites

- Python 3.9+
- Install dependencies:
  ```bash
  pip install httpx mcp
  ```
- The Node.js microservice must be running (see `nodesvc/README.md`).

## How to Run

### 1. Start the Node.js Microservice

```bash
cd nodesvc
npm install
npm start
```

### 2. Run the MCP Server

```bash
python mcpserver.py
```

### 3. Run get_users Tool

Create a test script to call the MCP tool:

```bash
python -c "import asyncio; from mcpserver import get_users; print(asyncio.run(get_users()))"
```

## VS Code Configuration

To configure the MCP server in VS Code user settings, add this to your `settings.json`:

```json
{
  "mcp.servers": {
    "user-data-server": {
      "command": "python",
      "args": ["/path/to/your/project/mcpserver.py"],
      "env": {}
    }
  }
}
```

Replace `/path/to/your/project/` with the actual path to your project directory.

## Usage

- The MCP server exposes a `get_users` tool that fetches user data from `http://localhost:3000/users`
- Returns formatted JSON user data or error message if microservice is unavailable
