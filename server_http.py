from fastmcp import FastMCP
from src.signals import get_signals
import os

mcp = FastMCP("buying-signals")

@mcp.tool()
def buying_signals(company: str, domain: str):
    return get_signals(company, domain)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        path="/mcp"
    )