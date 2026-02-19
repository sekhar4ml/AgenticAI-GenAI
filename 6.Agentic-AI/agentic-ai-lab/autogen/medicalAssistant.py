from autogen import ConversableAgent, UserProxyAgent, AssistantAgent,GroupChatManager, GroupChat
import os
from dotenv import load_dotenv

load_dotenv()

llm_config = {
    
    "config_list": [
        
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY",""),
        }
    ]
    
}


symptom_collection_agent=ConversableAgent(
    
    name="symptom_collection_agent",
    system_message="""You are a medical assistant that collects symptoms from patients in a friendly and empathetic manner.
                      Ask relevant questions and ensure all the symptomps are recorded accurately.
                      Return "TERMINATE" when the symptom collection is complete.
    
    
    """,
    
    llm_config=llm_config,
    human_input_mode="ALWAYS"
    
)

medical_histrory_agent=ConversableAgent(
    
    name="medical_histrory_agent",
    system_message="""You are responsible for collecting detailed medical history from patients.
    Ask relevant questions and ensure all the medical history is recorded accurately.
    Return "TERMINATE" when the medical history collection is complete.""",
    
    llm_config=llm_config,
    human_input_mode="ALWAYS"
    
)

diagnostic_analysis_agent=AssistantAgent(
    
    name="diagnostic_analysis_agent",
    system_message="""You are a diagnostic analysis agent that provides insights based on the the symptoms and medical history collected.
    
    Analyze the collected data and provide summary of potential conditions or next tretment plan,
    
    Return "TERMINATE" when the analysis is complete.""",
    
    llm_config=llm_config,
    human_input_mode="NEVER",
    
    
)

treatment_planning_agent=AssistantAgent(
    
    name="treatment_planning_agent",
    system_message="""You are a treatment planning agent that suggests treatment plans based on the diagnostic analysis provided.
    provide detailed treatment plans and medications, lifestyle changes, food habits etc.
    
    Return "TERMINATE" when the treatment planning is complete.
    
    
    """,
    
    llm_config=llm_config,
    human_input_mode="NEVER",
    
    
)


primary_care_agent=AssistantAgent(
    
    
    name="primary_care_agent",
    system_message="""You are the primary care agent for cooordinating the diagnostic analysis and treatment planning workflow.
    Ensure the the symptom collection, medical history collection, diagnostic analysis, and treatment planning agents work together seamlessly.
    
    Return "TERMINATE" when the entire process is complete.""",
    
    llm_config=llm_config,
    human_input_mode="NEVER",
    
    
)

user_proxy=UserProxyAgent(
    
    name="user_proxy",
    human_input_mode="ALWAYS",
)


chats=[
    
    {
       "recipient":symptom_collection_agent,
       "message":"Hello! I am here to help you with your medical concerns. Could you please describe your symptoms?",
       "summary_method":"reflection_with_llm",
       "summary_args":{
           
           "summary_prompt":"Summarize the patient's symptoms as JSON: {'symptoms':'','next_steps':''}",
           "max_turns":1,
           "clear_history":True
           
           }
       
    },
    
     {
       "recipient":medical_histrory_agent,
       "message":"Please start collecting the patient's medical history based on the symptoms provided.",
       "summary_method":"reflection_with_llm",
       "summary_args":{
           
           "summary_prompt":"Summarize medical history as JSON: {'medical_history':'','next_steps':''}",
           "max_turns":1,
           "clear_history":True
           
           }
       
    },
       
     {
       "recipient":diagnostic_analysis_agent,
       "message":"Please analayze the collected symptoms and medical history.",
       "summary_method":"reflection_with_llm",
       "summary_args":{
           
           "summary_prompt":"Summarize diagnostic analysis as JSON: {'diagnosis':'','next_steps':''}",
           "max_turns":1,
           "clear_history":True
           
           }
       
    },
       
    {
       "recipient":treatment_planning_agent,
       "message":"Please create a treatment plan based on the diagnosis analysis.",
       "summary_method":"reflection_with_llm",
       "summary_args":{
           
           "summary_prompt":"Summarize the treatment plans as JSON: {'treatment_plan':'','next_steps':''}",
           "max_turns":1,
           "clear_history":True
           
           }
       
    },   
    
    
]


primary_care_agent.register_nested_chats(chats,trigger=user_proxy)

chat_results=primary_care_agent.initiate_chat(
    
    recipient=user_proxy,
    message="Hello, how are you feeling today?. What brings to you here.",
    max_round=2,
    summary_method="last_msg",
    
)


print(chat_results)






















