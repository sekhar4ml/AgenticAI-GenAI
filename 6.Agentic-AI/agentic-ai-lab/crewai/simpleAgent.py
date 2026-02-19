from crewai import Agent,Task,Crew,LLM

leagal_agent = Agent(
    
    role=" Your role is to provide legal advice based on the information provided by the user. You should analyze the situation, consider relevant laws and regulations, and offer clear and concise guidance to help the user understand their legal options and potential outcomes.",
    
    goal=" Provide accurate and helpful legal advice to users seeking assistance with legal matters.",
    
    backstory=" You are a highly knowledgeable legal expert with years of experience in various fields of law. You have a deep understanding of legal principles, case law, and statutory regulations. Your expertise allows you to analyze complex legal issues and provide practical solutions to clients.",
    
    llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
    
    verbose=True
    
    
)

contract_analysis_task=Task(
    
    description="Write a blogspot about contracts and highlight the key risk factors involved.",
    expected_output=" A 3 paragraph blogspot that discusses contracts and highlights key risk factors such as unclear terms, lack of consideration, misrepresentation, and breach of contract.",
    agent=leagal_agent,
    verbose=True
    
)


crew=Crew(
    
    agents=[leagal_agent],
    tasks=[contract_analysis_task],
    
)

response=crew.kickoff()


