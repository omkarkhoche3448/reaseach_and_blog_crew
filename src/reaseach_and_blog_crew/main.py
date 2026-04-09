import os
import atexit
import logging

from ants_platform import AntsPlatform
from ants_platform.crewai import EventListener

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Initialize at module level — BEFORE crew.py is imported.
# This ensures EventListener is registered on the event bus
# before CrewBase triggers any events during import.
_public_key = os.environ.get("ANTS_PLATFORM_PUBLIC_KEY")
_secret_key = os.environ.get("ANTS_PLATFORM_SECRET_KEY")
_host = os.environ.get("ANTS_PLATFORM_HOST", "https://app.agenticants.ai")

logger.debug(f"Public key loaded: {'Yes' if _public_key else 'No'}")
logger.debug(f"Secret key loaded: {'Yes' if _secret_key else 'No'}")
logger.debug(f"Host: {_host}")

_ants_platform = AntsPlatform(
    public_key=_public_key,
    secret_key=_secret_key,
    host=_host,
    timeout=30,
)
_listener = EventListener(
    public_key=_public_key,
    agent_name="research_and_blog_crew",
    agent_display_name="Research & Blog Crew v1.0",
)
atexit.register(_ants_platform.flush)

# Import crew AFTER SDK is initialized
from reaseach_and_blog_crew.crew import ResearchAndBlogCrew  # noqa: E402


def run():
    """
    Run the crew.
    """
    inputs = {
        "topic": "The impact of artificial intelligence on the job market"
    }

    try:
        ResearchAndBlogCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    finally:
        _ants_platform.flush()
