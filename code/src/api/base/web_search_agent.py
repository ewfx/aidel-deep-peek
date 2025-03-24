from smolagents import (
    ToolCallingAgent,
    GoogleSearchTool,
    VisitWebpageTool,
    HfApiModel
)
import os
from dotenv import load_dotenv
load_dotenv()

SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")


web_agent = ToolCallingAgent(
    model=HfApiModel(
        "Qwen/Qwen2.5-Coder-32B-Instruct", provider="together", max_tokens=4096
    ),
    tools=[
        GoogleSearchTool(provider="serper"),
        VisitWebpageTool(),
    ],
    name="web_agent",
    description="Extracts financial and legal entity data from external sources.",
    verbosity_level=0,
    max_steps=10,
)
