from langgraph.graph import StateGraph, START, END

from typing import TypeDict


class BMIState(TypeDict):
    weight: float 
    height: float
    bmi: float
    result: str
    
def calculate_bmi(state:BMIState):
    
    weight=state["weight"]
    height=state["height"]
    
    bmi= weight / (height ** 2)
    
    return{"weight":weight, "height":height, "bmi":bmi, "result":""}

def label_bmi(state:BMIState):
    
    bmi=state["bmi"]
    
    if bmi < 18.5:
        result="Underweight"
    elif 18.5 <= bmi < 24.9:
        result="Normal weight"
    elif 25 <= bmi < 29.9:
        result="Overweight"
    else:
        result="Obesity"
        
    return{"weight":state["weight"], "height":state["height"], "bmi":bmi, "result":result}

bmi_graph=StateGraph(BMIState)

bmi_graph.add_node("calculate_bmi_node", calculate_bmi)
bmi_graph.add_node("label_bmi_node", label_bmi)


bmi_graph.add_edge(START, "calculate_bmi_node")
bmi_graph.add_edge("calculate_bmi_node", "label_bmi_node")
bmi_graph.add_edge("label_bmi_node", END)

app=bmi_graph.compile()

graphView=app.get_graph().print_ascii()

result=app.invoke({"weight":70, "height":1.75})
print(result["result"])


