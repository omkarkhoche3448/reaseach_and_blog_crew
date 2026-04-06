# Research & Blog Crew

A multi-agent AI system powered by [CrewAI](https://crewai.com) that researches a topic and generates a blog post.

## Agents

| Agent | Role |
|-------|------|
| Report Generator | Researches a topic and creates a detailed ~2000 word report |
| Blog Writer | Converts the report into a fun, easy-to-read blog post |

**Process:** Sequential (Report Generator → Blog Writer)

## Prerequisites

- Python >= 3.10, < 3.14
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- (Optional) Ants Platform SDK for observability

## Setup

### 1. Install uv

```bash
pip install uv
```

### 2. Clone the repo

```bash
git clone https://github.com/omkarkhoche3448/crewai.git
cd crewai
```

### 3. Install dependencies

```bash
crewai install
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4o-mini
```

Get your OpenAI API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

### 5. Ants Platform SDK Setup (Optional — for observability)

This crew integrates with [Ants Platform](https://cloud.ants-platform.com) to track LLM calls, agent steps, tool usage, and costs.

#### Using the published SDK

```bash
pip install ants-platform[crewai]
```

#### Using the local SDK (for development/testing)

If you have the SDK source locally, the `pyproject.toml` already points to it:

```toml
"ants-platform[crewai] @ file:///C:/Users/Abcom/Desktop/Ants-platform/ants-platform-python"
```

To install or update after SDK changes:

```bash
uv sync --reinstall-package ants-platform
```

#### Add Ants Platform keys to `.env`

```env
ANTS_PLATFORM_PUBLIC_KEY=pk-ap-your-public-key
ANTS_PLATFORM_SECRET_KEY=sk-ap-your-secret-key
ANTS_PLATFORM_HOST=http://localhost:3000
```

For production, change `ANTS_PLATFORM_HOST` to `https://cloud.ants-platform.com`.

#### How it works

The SDK is initialized in `main.py` with just 3 lines:

```python
from ants_platform import AntsPlatform
from ants_platform.crewai import EventListener

ants_platform = AntsPlatform(timeout=30)
listener = EventListener(
    agent_name="research_and_blog_crew",
    agent_display_name="Research & Blog Crew v1.0",
)
```

This auto-captures all crew executions, agent steps, LLM calls (model, tokens, cost), and tool usage into Ants Platform traces.

Always call `ants_platform.flush()` at the end to ensure all spans are exported.

#### Local SDK development workflow

```bash
# 1. Make changes to the SDK source
# 2. Reinstall the updated SDK in the crew project
cd C:/Users/Abcom/Desktop/CrewAI/research_and_blog_crew
uv sync --reinstall-package ants-platform

# 3. Run the crew to test
uv run run_crew
```

## Running the Crew

```bash
crewai run
```

Or with `uv` directly (recommended when using Ants Platform):

```bash
uv run run_crew
```

**Note (Windows):** If you see emoji encoding errors, run with:

```bash
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 crewai run
```

The crew will generate a blog post at `blogs/blog.md`.

## Customizing the Topic

Edit `src/reaseach_and_blog_crew/main.py` and change the `topic` value:

```python
inputs = {
    'topic': 'Your topic here'
}
```

## Customizing Agents & Tasks

- `src/reaseach_and_blog_crew/config/agents.yaml` — Agent roles, goals, backstories
- `src/reaseach_and_blog_crew/config/tasks.yaml` — Task descriptions and expected outputs
- `src/reaseach_and_blog_crew/crew.py` — Agent/task logic and tools

## Deploy to CrewAI Platform

```bash
crewai login
crewai deploy create
crewai deploy push
crewai deploy status
```

## Project Structure

```
research_and_blog_crew/
├── .env                          # API keys (not committed)
├── pyproject.toml                # Project config
├── blogs/                        # Generated blog output
│   └── blog.md
└── src/reaseach_and_blog_crew/
    ├── config/
    │   ├── agents.yaml           # Agent definitions
    │   └── tasks.yaml            # Task definitions
    ├── crew.py                   # Crew orchestration
    ├── main.py                   # Entry point
    └── tools/
        └── custom_tool.py        # Custom tools
```
