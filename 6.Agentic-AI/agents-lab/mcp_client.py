# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.resources import load_mcp_resources
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
from dotenv import load_dotenv
load_dotenv()
model = ChatOpenAI(model="gpt-4o", temperature=0)

server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your mcp_server.py file
    args=["/Users/sreesekhar/IAI/1.AgenticAI/week-8/agents-lab/mcp_server.py"],
)



async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            print(f"Loaded tools: {[tool.name for tool in tools]}")
            
            resources = await load_mcp_resources(session)
            print("Loaded resources:", resources)
            
            
            

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": "Add 5 and 10, then multiply the result by 2"})
         

            #print(agent_response["messages"][-1].content)
            #agent_response = await agent.ainvoke({"messages": "Get a greeting message for  'Sekhar'"})
            return agent_response

# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result["messages"][-1].content)
   
   