import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

#export POSTGRES_DSN="postgresql://postgres:pg1234@localhost:5432/srg"
#python mcp/postgres/client.py

async def main():
    # Pass env vars to server process
    env = dict(os.environ)
    if "POSTGRES_DSN" not in env:
        raise RuntimeError("Please set POSTGRES_DSN before running client.")

    # Start server.py as a subprocess (stdio transport)
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/sreesekhar/IAI/1.AgenticAI/week-8/agents-lab/postgres/server.py"],
        env=env
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            # Call db_time tool
            t1 = await session.call_tool("db_time", arguments={})
            print("db_time result:", t1.content)

            # Call list_tables tool
            t2 = await session.call_tool("list_tables", arguments={})
            print("list_tables result:", t2.content)

            # Example: select from a table (change "your_table")
            # t3 = await session.call_tool("select_top", arguments={"table": "your_table", "limit": 3})
            # print("select_top result:", t3.content)

if __name__ == "__main__":
    asyncio.run(main())
