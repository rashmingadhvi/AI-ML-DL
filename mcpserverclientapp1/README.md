# MCP Server (Python)

This directory contains MCP servers that expose a tool to fetch user data from the Node.js microservice.

## Prerequisites

- Python 3.9+
- Install dependencies:
  ```bash
  pip install httpx mcp fastmcp
  ```
- The Node.js microservice must be running (see `nodesvc/README.md`).

## How to Run

### 1. Start the Node.js Microservice

```bash
cd nodesvc
npm install
npm start
```

### 2. Run MCP Servers

#### FastMCP HTTP Server

```bash
python fastmcpserver.py
```

Runs on `http://localhost:9000`

#### Standard MCP Server (stdio)

```bash
python mcpserver.py
```

### 3. Call MCP Server (3 Ways)

#### Method 1: VS Code MCP Extension (HTTP)

Add to VS Code `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "my-user-mcp-http": {
        "type": "http",
        "url": "http://localhost:9000"
      }
    }
  }
}
```

Start `fastmcpserver.py` first, then use VS Code MCP commands.

#### Method 2: VS Code MCP Extension (stdio)

Add to VS Code `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "my-user-mcp-stdio": {
        "type": "stdio",
        "command": "python",
        "args": ["/path/to/project/fastmcpserver.py"]
      }
    }
  }
}
```

VS Code auto-launches the server.

#### Method 3: Direct Script Call

```bash
python get_users_via_mcp.py
```

Calls the FastMCP HTTP server directly.

## Usage

- Both servers expose a `get_users` tool that fetches user data from `http://localhost:3000/users`
- Returns formatted JSON user data or error message if microservice is unavailable
