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

def conversation():
    
    messages=[]
    
    try:
        
        while True:
            
            user_q=input("You: ").strip()
            
            messages.append({"content":user_q,"role":"user"})
            
            reply=agent.generate_reply(
                
                messages=messages
            )
            
            print("Bot:", reply)
            
    except KeyboardInterrupt:
        
        print("\nConversation Ended.")        
            
if __name__ == "__main__":
    
    conversation()

