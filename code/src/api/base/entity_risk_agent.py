from smolagents import (
    CodeAgent,
    HfApiModel,
    GoogleSearchTool,
    VisitWebpageTool
)

from .web_search_agent import web_agent
from .risk_assessment_agent import risk_agent

import os
from dotenv import load_dotenv
load_dotenv()

SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

class EntityRiskAgent:
    """
   A multi-agent system for evaluating financial entity risks.
   The system consists of:
   - A Web Agent: Extracts financial and legal entity data from external sources.
   - A Risk Assessment Agent: Uses news sentiment analysis and LEI verification to determine risk.
   - A Manager Agent: Oversees the workflow and generates a consolidated risk report.
   """

    def __init__(self):
        """Initialize the agents within the system."""

        self.web_search_agent = web_agent
        self.risk_assessment_agent = risk_agent

        self.manager_agent = CodeAgent(
            model=HfApiModel("deepseek-ai/DeepSeek-R1", provider="together", max_tokens=8096),
            tools=[],
            managed_agents=[self.web_search_agent, self.risk_assessment_agent],
            additional_authorized_imports=["json", "pandas", "numpy"],
            planning_interval=5,
            verbosity_level=2,
            max_steps=20,
        )
