from smolagents import (
    ToolCallingAgent,
    GoogleSearchTool,
    VisitWebpageTool,
    HfApiModel
)
from tools import RiskAssessmentTool
import os
from dotenv import load_dotenv
load_dotenv()

SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

risk_agent = ToolCallingAgent(
    model=HfApiModel(
        "Qwen/Qwen2.5-Coder-32B-Instruct", provider="together", max_tokens=4096
    ),
    tools=[
        GoogleSearchTool(provider="serper"),
        VisitWebpageTool(),
        RiskAssessmentTool()
    ],
    name="risk_assessment_agent",
    description="""
                For a transaction, return the risk score, confidence and reason against 
                the given entity list and transaction_id in the transaction."
                """,
    verbosity_level=0,
    max_steps=10,
)
