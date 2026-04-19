# server_http.py

from fastmcp import FastMCP
from src.signals import get_signals

mcp = FastMCP("buying-signals")

@mcp.tool()
def buying_signals(company: str, domain: str):
    """Get structured buying signals for a company"""
    return get_signals(company, domain)

if __name__ == "__main__":
    # This runs HTTP server on port 8000
    mcp.run(transport="http", port=8000)