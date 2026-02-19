from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class myCountState(TypeDict):
    number: int


def increment(state:myCountState ):
    
    new_value= state["number"] + 1
    
    returun{"number":new_value}


def mulitiply_by_two(state:myCountState ):
    
    new_value= state["number"] * 2
    
    return{"number":new_value}


    
 mygraph=StateGraph(myCountState)  
 
 mygraph.add_node("increment_node", increment)
 mygraph.add_node("multiply_node", mulitiply_by_two)
 
 
 mygraph.add_edge(START, "increment_node")
 mygraph.add_edge("increment_node", "multiply_node")
 mygraph.add_edge("multiply_node", END)
 
 app=mygraph.compile()
 
 graphView=app.get_graph().print_ascii()
 
 
 result=app.invoke("number",10)
 print(result)
 
 
 
 
 
 
 
 
 
 
 
    



