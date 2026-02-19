from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class DemoState(TypedDict):
    input_text: str
    output_text: str
    
    
def to_uppercase(state:DemoState):
    
    input_text= state["input_text"]
    
    output_text= input_text.upper()
    
    return{"input_text":state["input_text"], "output_text":output_text}


def add_hi(state:DemoState):
    
    output_text= "Hi " + state["output_text"]
    
    return{"input_text":state["input_text"], "output_text":output_text}


def add_wishes(state:DemoState):
    
    output_text= state["output_text"] + ", have a great day!"
    
    return{"input_text":state["input_text"], "output_text":output_text}


def create_simple_demo_graph():
    demo_graph=StateGraph(DemoState)  
    
    demo_graph.add_node("to_uppercase_node", to_uppercase)
    demo_graph.add_node("add_hi_node", add_hi)
    demo_graph.add_node("add_wishes_node", add_wishes)
    
    
    demo_graph.add_edge(START, "to_uppercase_node")
    demo_graph.add_edge("to_uppercase_node", "add_hi_node")
    demo_graph.add_edge("add_hi_node", "add_wishes_node")
    demo_graph.add_edge("add_wishes_node", END)
    
    app=demo_graph.compile()
    
    graphView=app.get_graph().print_ascii()
    
    return app

app=create_simple_demo_graph()

results=app.invoke({"input_text":"Sekhar"})

print(results)






