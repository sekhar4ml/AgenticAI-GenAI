from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool, FileReadTool

@CrewBase
class JobFinderCrew():
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ollama_llm = LLM(
        model='ollama/llama3.2',
        base_url='http://localhost:11434',
    )

    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reader'],
            tools=[FileReadTool()],
            verbose=True,
            #llm=self.ollama_llm
        )
    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher'],
            tools=[CSVSearchTool(),FileReadTool()],
            verbose=True,
            #llm=self.ollama_llm
        
    )
        
    @task
    def read_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config['read_cv_task'],
            agent=self.cv_reader(),
        )    
    @task
    def match_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_cv_task'],
            agent=self.matcher(),
        )
    @crew
    def crew(self) -> Crew:
        """Creates the JonFinderCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            #process=Process.sequential,
        )    