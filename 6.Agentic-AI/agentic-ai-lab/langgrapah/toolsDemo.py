from langgraph.graph import StateGraph, START, END, MessagesState

from langchain_core.tools import tool

from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage

from langchain_openai import ChatOpenAI

llm=ChatOpenAI(model="gpt-4o-mini")


@tool
def search_web(query: str) -> str:
    """Search the web using Tavily and return the results."""
    tavily = TavilySearch()
    results = tavily.run(query)
    return results

@tool
def write_summary(content: str) -> str:
    """Write a brief summary of the given content."""
    return f"Summary:\n\n {content[:100]}..."

tools=[search_web, write_summary]


class AgentState(MessagesState):
    pass

def researcher(state:AgentState):
    
    system_msg= SystemMessage(content="You are a research assistant. Use the tools to gather information and summarize it.")
    
    model=llm.bind_tools(tools)
    
    response=model.invoke([system_msg] + state["messages"])
    return {"messages":[response]}


def wrter(state:AgentState):
    
    system_msg= SystemMessage(content="You are a writing assistant. Use the tools to write a summary based on research.")
    
    model=llm.bind_tools(tools)
    
    response=model.invoke([system_msg] + state["messages"])
    return {"messages":[response]}

def route_after_researcher(state:AgentState) -> str:
    """If the last message contains tool calls, route to tools, else to writer."""
    
    last=state["messages"][-1]
    
    if getattr(last, "tool_calls", None):
        return "tools"
    return "writer"
    
    
graph=StateGraph(AgentState)

graph.add_node("researcher", researcher)
graph.add_node("writer", wrter)
graph.add_node("tools", ToolNode(tools))


graph.set_entry_point("researcher")

graph.add_conditional_edges(
    
    "researcher",
    
    route_after_researcher,{
        
        "tools":"tools",
        "writer":"writer",
    },
    
    
)

graph.add_edge("tools", "researcher")
graph.add_edge("writer", END)

app=graph.compile()
graphView=app.get_graph().print_ascii()

result=app.invoke({"messages":[{"role":"user", "content":"Write a summary about the NVIDIA Stocks and Stock value for today."}]})


print(result["messages"][-1].content)







