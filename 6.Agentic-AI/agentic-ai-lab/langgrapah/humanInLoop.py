
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
from langgraph.types import Command, interrupt
from langgraph.checkpoint.sqlite import SqliteSaver


from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode

import re
import operator

llm=ChatOllama(model="llama3.2")


class AgentState(TypedDict):
    messages: Annotated[list,operator.add]


@tool
def transfer_money(amount: float, recipient: str):
    """
    Transfer money. Large transfers require approval.

    Args:
        amount: Amount in dollars
        recipient: Recipient name
    """
  
    if amount > 1000:
        
       approval = interrupt(
    {
        "type": "approval_required",
        "amount": amount,
        "recipient": recipient,
    }
)

    # Expect approval like {"decision": "approved"} from Command(resume=...)
    if approval.get("decision") != "approved":
        return "Transfer denied by approver."
    
    return f"Transferred ${amount} to {recipient}."


# PII Pattern Definitions
patterns = {
        "SSN": r'\b\d{3}-\d{2}-\d{4}\b',  # SSN: 123-45-6789
        "Credit Card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit Card: 1234-5678-9012-3456
        "Mobile Number": r'\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',  # Mobile: +1-234-567-8900
        "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email: user@example.com
        "URL/Link": r'https?://[^\s]+|www\.[^\s]+'  # URL: http://example.com or www.example.com
    }


def guardrail_check(state:AgentState):
    
    last_message = state["messages"][-1]

    for pii_type, pattern in patterns.items():
        if re.search(pattern, last_message.content):
            return {
                "messages": [SystemMessage(content=f"PII detected: {pii_type}. Please remove it before proceeding.")]
            }
    return {"messages": [last_message]}  


def agent_transfer(state:AgentState):
    
    tools=[transfer_money]
    model=llm.bind_tools(tools)
    
    system_msg=SystemMessage(content="You are a banking assistant. Help users transfer money securely using the transfer_money tool.")
    
    messages=[system_msg] + state["messages"]
    
    response=model.invoke(messages)
    
    if hasattr(response, "tool_calls") and response.tool_calls:
        
        for tc in response.tool_calls:
            
             print(f"[AGENT] called Tool {tc.get('name', '?')} with args {tc.get('args', '?')}")
    
    else:
        print(f"AI Response:")
     
            
    return {"messages":[response]}


def should_continue(state:AgentState):
    
    last_msg=state["messages"][-1]
    
    if hasattr(last_msg,"tool_calls") and len(last_msg.tool_calls) > 0:
        return "tools"
    
    else:
        return END
    
def guardrail_router(state:AgentState):
    
    last_msg=state["messages"][-1]
    
    if isinstance(last_msg, SystemMessage):
        last_msg.pretty_print()
        return END
    
    return "agent"


import os

db_name="db/checkpoint.db"

import sqlite3

os.makedirs("db", exist_ok=True)



def create_graph():
    
    graph=StateGraph(AgentState)
    
    graph.add_node("guardrail", guardrail_check)
    graph.add_node("agent", agent_transfer)
    graph.add_node("tools", ToolNode([transfer_money]))
    
    
    
    graph.add_edge(START, "guardrail")
    graph.add_conditional_edges("guardrail", guardrail_router,["agent", END])
    
    graph.add_conditional_edges("agent", should_continue, ["tools", END])
    
    graph.add_edge("tools", "agent")
    
    conn=sqlite3.connect(db_name,check_same_thread=False)
    checker=SqliteSaver(conn)
    
    graph=graph.compile(checkpointer=checker)
    
    graph.get_graph().print_ascii()
    
    return graph

graph=create_graph()


def chat(query, thread_id):
    
    config={"configurable":{"thread_id": thread_id}}
    
    response=graph.invoke({"messages":[HumanMessage(content=query)]}, config=config)
    #print(response)
    
    if '__interrupt__' in response:
        interrupt_info=response["__interrupt__"][0]
        
        result = graph.invoke(
                Command(resume={"decision": input("Approve this transfer? (approved/deny): ")}),
                config=config,
               )
    
        result['messages'][-1].pretty_print()
    
    
chat("Transfer 5000 to phone 1 614-333-3456", "user1")
    
    
    
    
    
    