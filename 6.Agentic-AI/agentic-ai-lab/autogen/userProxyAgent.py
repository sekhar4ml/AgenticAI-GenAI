from autogen import ConversableAgent, UserProxyAgent
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

agent=ConversableAgent(
    
    name="ChatBot",
    llm_config=llnm_config,
    human_input_mode="NEVER",
    system_message="You are a helpful assistant that answers questions for useerProxy"
)

myproxy=UserProxyAgent(
    
 name="userProxy",
 human_input_mode="ALWAYS",    
 is_termination_msg="exit"    

)


myproxy.initiate_chat(agent)




