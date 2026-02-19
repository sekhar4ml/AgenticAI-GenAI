from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class CalculatorState(TypedDict):
    number1: int
    number2: int
    operation: str
    result: float
    
def add_numbers(state:CalculatorState):
    
    result= state["number1"] + state["number2"]
    
    return{"number1":state["number1"], "number2":state["number2"], "operation":state["operation"], "result":result}

def subtract_numbers(state:CalculatorState):
    
    result= state["number1"] - state["number2"]
    
    return{"number1":state["number1"], "number2":state["number2"], "operation":state["operation"], "result":result}



    
def route(state: CalculatorState) -> str:
    return "add_node" if state["operation"] == "+" else "subtract_node"
    
    
graph=StateGraph(CalculatorState) 
 
graph.add_node("add_node", add_numbers) 
graph.add_node("subtract_node", subtract_numbers) 
 


graph.add_conditional_edges(
    START,
    route,
    {
        "add_node": "add_node",
        "subtract_node": "subtract_node",
    },
)
   
graph.add_edge("add_node", END)  
graph.add_edge("subtract_node", END)
   
  
app=graph.compile()
  
graphView=app.get_graph().print_ascii() 

result=app.invoke({"number1":10, "number2":5, "operation":"-"})

print(result)
   
     
     
     
     
     
     
 
    
 
 
 

