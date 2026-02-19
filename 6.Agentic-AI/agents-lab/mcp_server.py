from mcp.server.fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchRun

mcp = FastMCP("DemoMCP")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

@mcp.tool()
def search_tool(query: str) -> str:
    """Search the web for a query."""
    search=DuckDuckGoSearchRun()
    response = search.invoke(query)
    return response


@mcp.resource(uri="greeting://hello")
def hello() -> str:
    return "Hello from a static resource!"

@mcp.resource(uri="greeting://hello/{name}")
def hello_name(name: str) -> str:
    return f"Hellllllllllllllllllllllo, {name}!"

if __name__ == "__main__":
    mcp.run(transport="stdio")