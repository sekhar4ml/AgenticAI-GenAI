from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

from dotenv import load_dotenv
load_dotenv()

@tool("Say_HI")
def Say_HI(user: str) -> str:
    """A tool that says hi to the user."""
    return f" Whats Up! , {user}! How can I assist you today?"

#greetings = Say_HI()

simple_agent = Agent(
    
    role=" You are a friendly assistant who greets users and offers help.",
    goal=" Provide a warm greeting and assist users with their requests.",
    backstory=" You have a cheerful personality and enjoy helping people feel welcome.",
    
    llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
    verbose=True
)

simple_task = Task(
    
    description="Wishing the {user}",
    expected_output=" A friendly greeting message to the {user}.",
    tools=[Say_HI],
    agent=simple_agent,
)

crew = Crew(
    
    agents=[simple_agent],
    tasks=[simple_task],
)

response = crew.kickoff(inputs={"user": "Sekhar"})
print(response)

