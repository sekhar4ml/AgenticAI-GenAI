from langgraph.graph import StateGraph, START, END, MessagesState

from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

llm=ChatOpenAI(model="gpt-4o-mini")



def call_llm(state:MessagesState):
    
   response=llm.invoke(state["messages"])
   return {"messages":response}

graph=StateGraph(MessagesState)

graph.add_node("llm_node", call_llm)


graph.add_edge(START, "llm_node")
graph.add_edge("llm_node", END)

app= graph.compile()

graphView=app.get_graph().print_ascii()


result=app.invoke({"messages":[{"role":"user", "content":"What are best attractions in Florida?"}]})

for m in result["messages"]:
    print(f"{m.type}: {m.content}")


