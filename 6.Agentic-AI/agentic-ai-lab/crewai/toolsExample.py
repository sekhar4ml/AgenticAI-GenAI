from crewai import Agent,Task,Crew,LLM

from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, WebsiteSearchTool

from dotenv import load_dotenv

load_dotenv()


document_tools=DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
websearch_tool = WebsiteSearchTool()


reasearcher=Agent(
    
    role="Market Research Specialist",
    goal="Provide up-to-daete market analysis of the AI Industry.",
    backstory="You are an expert in market research with a focus on the AI industry. You have access to various tools and resources to gather and analyze market data effectively.",
    llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
    verbose=True,
)

writer=Agent(
    
    role="Content Writer",
    goal="Write engaging blog post about the AI Industry",
    backstory="You are a skilled content writer with experience in creating informative and engaging blog posts. You can effectively communicate complex topics to a general audience.",
    llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
    verbose=True,
    
)


research_task=Task(
    
    description="Research the AI Industry and provide a summary",
    expected_output=" A summary of the latest trends in the AI industry",
    tools=[document_tools, file_tool, search_tool, websearch_tool],
    agent=reasearcher,
)

write_task=Task(
    
 description="Write a blog post about the AI Industry based on the research provided",  
 expected_output=" A 5 paragraph blog post about the AI Industry and latest trends",
 agent=writer,
 tools=[document_tools, file_tool], 
    
)

crew=Crew(
    
    agents=[reasearcher, writer],
    tasks=[research_task, write_task],
    
)

response=crew.kickoff()
print(response) 




