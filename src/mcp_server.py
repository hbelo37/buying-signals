from mcp.server.fastmcp import FastMCP
from buying_signals import run_signals   # your existing function

mcp = FastMCP("gtm-skills")

@mcp.tool()
def buying_signals(domain: str) -> dict:
    """
    Detect buying signals and intent for a company domain.
    """
    return run_signals(domain)

if __name__ == "__main__":
    mcp.run()