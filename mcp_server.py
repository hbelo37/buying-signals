from mcp.server.fastmcp import FastMCP
from src.signals import get_signals

server = FastMCP("buying-signals")

@server.tool()
def buying_signals(company: str, domain: str):
    try:
        return get_signals(company, domain)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    server.run()