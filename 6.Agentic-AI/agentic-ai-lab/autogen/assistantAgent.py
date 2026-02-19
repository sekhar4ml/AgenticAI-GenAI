from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY","")

llnm_config = {
    
    "config_list": [
        
        {
            "model": "llama3.2",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama", 
        }
        
        ],
}

agent=AssistantAgent(
    
    name="AssistantBot",
    llm_config=llnm_config,
    code_execution_config={"work_dir":"./mycode"},
)

myproxy=UserProxyAgent(
    
 name="userProxy",
 human_input_mode="ALWAYS",    
 is_termination_msg="exit"    

)


myproxy.initiate_chat(
                      recipient=agent,
                      message="Write a python code to check if a number is prime or not."
                      )




