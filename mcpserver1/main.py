from mcp.server.fastmcp import FastMCP
import httpx
import logging

mcpserver = FastMCP(port=9000, debug=True, name="RMK-MCP Server Demo", host="127.0.0.1")
class MCPServerDemo:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s -> %(message)s')
    
    server: FastMCP
    def __init__(self):
        self.server = mcpserver
        self.logger= logging.getLogger("MCPServerDemo")
    def start(self):
        self.logger.info(f"MCP Server started on port {9000}")
        self.logger.info(f"Server name: {mcpserver.name}")
      
        self.server.run()
        
    """
    This tool declares a method that can be called from the client.
    The method name is "fetchWeather" and it takes no arguments.
    The method returns a json of weather details with lat and long.
    """
    @mcpserver.tool()
    async def fetchWeather():
      
        return httpx.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41"
                         +"&current=temperature_2m,wind_speed_10m&hourly=temperature_2m"
                         +",relative_humidity_2m,wind_speed_10m").json()
    
if __name__ == "__main__":
    mcpserverdemo = MCPServerDemo()
    mcpserverdemo.start()   
    mcpserverdemo.fetchWeather()                              
    

