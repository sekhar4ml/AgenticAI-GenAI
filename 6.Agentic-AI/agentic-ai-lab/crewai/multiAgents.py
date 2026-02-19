from crewai import Agent,Task,Crew,LLM, Process


reseasrch_agent = Agent(
    
    role=" You are a research expert specializing in gathering and analyzing information on various topics. Your role is to conduct thorough research, evaluate sources for credibility, and synthesize findings into clear and concise reports.",
    goal=" Provide accurate and comprehensive research reports to assist users in making informed decisions.",
    backstory=" You have a strong background in research methodologies and are skilled at navigating academic databases, online resources, and other information repositories. Your expertise allows you to efficiently gather relevant data and present it in an organized manner.",
    
    llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
    verbose=True
)

writing_agent = Agent(
    
    role=" You are a skilled writer with expertise in crafting engaging and informative content on a wide range of topics. Your role is to take research findings and transform them into well-structured articles, blog posts, and reports that are easy to understand and captivating for readers.",
    goal=" Provide informed and engaging content to assist users in making informed decisions.",
    backstory=" You have a strong background in writing and communication, with experience in various writing styles and formats. Your expertise allows you to effectively convey complex information in a clear and accessible manner.",
    llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
    verbose=True
)

research_task=Task(
    
    description="Research the latest trends in Quantum AI and its impact on various industries. Summarize your findings in a comprehensive report., ",
    expected_output=" A detailed report summarizing the latest trends in Quantum AI, including its applications, benefits, challenges, and potential impact on industries such as healthcare, finance, and technology.",
    agent=reseasrch_agent,
)

writing_task=Task(
    
    description=" Based on the research report provided, write an engaging article that highlights the key trends and implications of Quantum AI for a general audience.",
    expected_output=" An engaging article that discusses the key trends and implications of Quantum AI, written in a clear and accessible style suitable for a general audience.",
    agent=writing_agent,
)

crew =Crew(
    
    agents=[reseasrch_agent, writing_agent],
    tasks=[research_task, writing_task],
)


response=crew.kickoff()
print(response)


