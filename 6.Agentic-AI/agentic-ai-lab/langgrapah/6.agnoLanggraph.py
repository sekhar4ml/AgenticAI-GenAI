from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# ---- Agno imports ----
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# ---- Define two Agno agents ----
researcher = Agent(
    name="researcher",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=(
        "You are a research agent. Produce bullet findings with sources/claims clearly separated."
    ),
)

writer = Agent(
    name="writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=(
        "You are a writer agent. Turn findings into a crisp executive summary with headings."
    ),
)

# ---- LangGraph state ----
class State(TypedDict):
    topic: str
    findings: str
    summary: str

# ---- LangGraph nodes that CALL Agno agents ----
def researcher_node(state: State) -> dict:
    prompt = f"Research this topic and produce 6-10 bullets:\n\n{state['topic']}"
    out = researcher.run(prompt)
    return {"findings": out.content}

def writer_node(state: State) -> dict:
    prompt = (
        "Write a clear executive summary based on the findings below.\n\n"
        f"FINDINGS:\n{state['findings']}\n"
    )
    out = writer.run(prompt)
    return {"summary": out.content}

# ---- Build graph ----
g = StateGraph(State)
g.add_node("researcher", researcher_node)
g.add_node("writer", writer_node)

g.add_edge(START, "researcher")
g.add_edge("researcher", "writer")
g.add_edge("writer", END)

app = g.compile()
app.get_graph().print_ascii()

result = app.invoke({"topic": "how to do time travel"})
print(result["summary"])
