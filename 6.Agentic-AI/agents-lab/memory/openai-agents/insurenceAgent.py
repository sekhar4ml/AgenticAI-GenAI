from agents import Agent,Runner, InputGuardrail, GuardrailFunctionOutput

from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()



class InsuranceAdviseOutput(BaseModel):
   
    """ output model for insurance advise agent """ 
    is_insurenceQuestion: bool
    advise:str
    
    
health_insurence_agent= Agent(
     
     
     name="HealthInsurenceAgent",
     instructions="You are a helpful assistant that provides advise on health insurence related questions.",
    
     model="gpt-4o"
 )   
 
property_insurence_agent= Agent(
     
     name="PropertyInsurenceAgent",
     instructions="You are a helpful assistant that provides advise on property insurence related questions.",
     model="gpt-4o"
    
 )
guardrail_agent= Agent(
    
    name="InsurenceGuardrailAgent",
    instructions="You are an output guardrail agent that ensures the output of the insurence advise agents conform to the specified output model.",
    output_type=InsuranceAdviseOutput,
)
 
 
master_insurence_agent= Agent(
     
     name="MasterInsurenceAgent",
     instructions="You are a master insurence assistant that routes user questions to the appropriate specialized insurence agent (health or property). Based on the user's question, decide which specialized agent is best suited to provide an answer. If neither is appropriate, respond accordingly.",
     handoffs=[health_insurence_agent,property_insurence_agent,guardrail_agent],
 )


 
async def main():
     
     user_input="What are the best places to visit in India?"
     response= await Runner.run(master_insurence_agent,user_input)
     
     print(response.final_output)
 
 
if __name__=="__main__":
        import asyncio
        asyncio.run(main())
 
 
 
     
     
 
 
 
   