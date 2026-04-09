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

# Read standard env vars
_pk = os.environ.get("ANTS_PLATFORM_PUBLIC_KEY")
_sk = os.environ.get("ANTS_PLATFORM_SECRET_KEY")
_host = "https://app.agenticants.ai"

# Remove from os.environ AFTER reading, so CrewAI platform's own tracing
# system doesn't pick them up and create a conflicting client that sends
# our keys to the wrong endpoint (causing 401 errors).
for _key in ["ANTS_PLATFORM_PUBLIC_KEY", "ANTS_PLATFORM_SECRET_KEY", "ANTS_PLATFORM_HOST"]:
    os.environ.pop(_key, None)

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
