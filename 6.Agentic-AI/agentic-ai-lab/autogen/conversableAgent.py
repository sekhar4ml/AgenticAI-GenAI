from autogen import ConversableAgent
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY","")

llnm_config = {
    
    "config_list": [
        
        {
            "model": "gpt-4o-mini",
            "api_key": api_key, 
        }
        
        ],
}

agent=ConversableAgent(
    
    name="ChatBot",
    llm_config=llnm_config,
    human_input_mode="NEVER"
)

question="How to learn Quantum AI"
response=agent.generate_reply(
    
    messages=[{"content":question,"role":"user"}]
)

print("Response:", response)


