import os
import atexit
import logging

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from ants_platform import AntsPlatform
from ants_platform.crewai import EventListener

_logger = logging.getLogger("ants_crew_init")

# TEMP: hardcode new keys to test if they work from CrewAI platform network
_pk = "pk-ap-ee83027c-f011-448e-aa65-7bf5fe857ee7"
_sk = "sk-ap-2c13e4d7-33b4-4157-8051-0b2424929910"
_host = "https://app.agenticants.ai"

_logger.warning("ANTS_INIT PK=%s SK=%s HOST=%s", bool(_pk), bool(_sk), _host)

_ants_client = AntsPlatform(public_key=_pk, secret_key=_sk, host=_host, timeout=30)
_ants_listener = EventListener(
    public_key=_pk,
    agent_name="research_and_blog_crew",
    agent_display_name="Research & Blog Crew v1.0",
)
atexit.register(_ants_client.flush)

_logger.warning("ANTS_INIT_DONE")


# define the class for our crew
@CrewBase
class ResearchAndBlogCrew():

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

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

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
