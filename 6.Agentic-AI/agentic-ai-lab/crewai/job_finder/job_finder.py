from crew import JobFinderCrew

input_files={
    
    'cv_file':'/Users/sreesekhar/IAI/1.AgenticAI/week-9/agentic-ai-lab/crewai/job_finder/data/cv.md',
    'csv_file':'/Users/sreesekhar/IAI/1.AgenticAI/week-9/agentic-ai-lab/crewai/job_finder/data/jobs.csv',
    
}

def run_job_finder():
    job_finder_crew=JobFinderCrew()
    response=JobFinderCrew().crew().kickoff(inputs=input_files)
    print(response)
    
run_job_finder()   