from crewai import Agent,Task,Crew,LLM

from crewai.flow.flow import Flow, listen, start

from dotenv import load_dotenv
from litellm import completion

load_dotenv()


class FlowExample(Flow) :
    
    @start()
    def pick_random_city_name(self):
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        import random
        city = random.choice(cities)
        return city
    
    @listen(pick_random_city_name)
    def generate_interesting_fact(self, city_name: str):
        
        response=completion(
            
            model="gpt-4o-mini",
            messages=[{
                
                "role": "user",
                "content": f"Provide an interesting fact about the city {city_name}."
                
            }])
            
        intesting_fact=response["choices"][0]["message"]["content"]
        return intesting_fact
        
        
        
        
        
    
       
        
flow=FlowExample()
flow.plot()
   
result=flow.kickoff()
   
print("Interesting Fact:", result) 
    
