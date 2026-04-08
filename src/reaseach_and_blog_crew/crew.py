from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from ants_platform import AntsPlatform
from ants_platform.crewai import EventListener

# Initialize Ants Platform observability at module load time
# so it works both locally and on CrewAI platform
_ants_platform = AntsPlatform(timeout=30)
_listener = EventListener(
    agent_name="research_and_blog_crew",
    agent_display_name="Research & Blog Crew v1.0",
)

# define the class for our crew
@CrewBase
class ResearchAndBlogCrew():
    
    agents: list[BaseAgent]
    tasks: list[Task]
    
    # define the paths of config files
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # ============= Agents ====================
    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["report_generator"]
        )
        
    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["blog_writer"]
        )
        
    # ============== Tasks ===========================
    # order of task definition matters
    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config["report_task"]
        )
        
    @task
    def blog_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["blog_writing_task"],
            output_file="blogs/blog.md"
        )
        
    # ================ Crew ===============================
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )