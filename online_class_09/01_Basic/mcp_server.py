from mcp.server.fastmcp import FastMCP


# --- 1. Create and Configure the FastMCP Application ---
mcp_app = FastMCP(
    name="SharedStandAloneMCPServer",
    stateless_http=True,
    # json_response=True, # Generally easier for HTTP clients if they don't need full SSE parsing
)

# --- 2. Define a simple tool ---
@mcp_app.tool(
    name="special_greeting",
    description="Returns a personalized greeting from the shared MCP server."
)
def greet(name: str = "World") -> str:
    print(f"Tool 'special_greeting' called with name: {name}")
    response_message = f"Hello {name}! Welcome to the shared MCP server."
    return response_message

@mcp_app.tool(
    name="get_my_mood",
    description="Returns a personalized greeting from the shared MCP server."
)
def mood(name: str = "World") -> str:
    """A simple greeting tool."""
    print(f"Tool 'moo' called with name: {name}")
    return "I am happy"



mcp_app = mcp_app.streamable_http_app()