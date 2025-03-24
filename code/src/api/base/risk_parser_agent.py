from smolagents import (
    CodeAgent,
    HfApiModel,
    GoogleSearchTool,
    VisitWebpageTool
)
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")


class RiskParserAgent:
    def __init__(self, model="Qwen/Qwen2.5-Coder-32B-Instruct"):
        self.model = model

    def process(self, query, sys_msg, web_access=False):
        tools=[]
        if web_access:
            tools.append(GoogleSearchTool(provider="serper"),)
        processor_agent = CodeAgent(
            model=HfApiModel(self.model),
            tools=[],
            additional_authorized_imports=['collections', 'itertools', 'random',
                                     'math', 're', 'stat', 'statistics', 'time', 'queue',
                                     'unicodedata', 'datetime', 'string'],
            verbosity_level=0,
            max_steps=10,
        )
        return processor_agent.run(f"{sys_msg} <input> {query} </input>")
