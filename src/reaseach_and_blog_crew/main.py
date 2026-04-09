from reaseach_and_blog_crew.crew import ResearchAndBlogCrew ##, _ants_client


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
    ## finally:
    ##     _ants_client.flush()
