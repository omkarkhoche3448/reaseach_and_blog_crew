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

# Initialize SDK at module level in crew.py as well.
# On CrewAI platform, the Celery worker may import crew.py directly
# without going through main.py, so we need init here too.
_pk = os.environ.get("ANTS_PLATFORM_PUBLIC_KEY")
_sk = os.environ.get("ANTS_PLATFORM_SECRET_KEY")
# Host is hardcoded — CrewAI platform may override ANTS_PLATFORM_HOST env var
_host = "https://app.agenticants.ai"

_logger.warning("ANTS_CREW_INIT PK=%s SK=%s HOST_HARDCODED=%s ENV_HOST=%s", bool(_pk), bool(_sk), _host, os.environ.get("ANTS_PLATFORM_HOST", "NOT_SET"))

_ants_client = AntsPlatform(public_key=_pk, secret_key=_sk, host=_host, timeout=30)
_ants_listener = EventListener(
    public_key=_pk,
    agent_name="research_and_blog_crew",
    agent_display_name="Research & Blog Crew v1.0",
)
atexit.register(_ants_client.flush)

_logger.warning("ANTS_CREW_INIT_DONE")


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
