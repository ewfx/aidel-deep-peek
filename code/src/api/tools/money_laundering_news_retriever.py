from typing import Dict, List, Any

from smolagents import Tool
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from utils.news_utils import NewsUtils
import numpy as np
import json


class MoneyLaunderingNewsRetrieverTool(Tool):
    name = "money_laundering_news_retriever"
    description = (
        """
        Retrieves and analyzes negative financial news for a given entity (company). 
        It fetches news using Google News RSS and computes a risk score and confidence based on negative sentiment. 
        The tool outputs results in JSON format with extracted entity details, risk score, and supporting evidence.
        Example:
        >>> retriever = MoneyLaunderingNewsRetriever()
        >>> result = retriever.forward("Wirecard AG")
        >>> print(result)
        {
            "entity": "Wirecard AG",
            "risk_score": 0.78,
            "confidence": 0.92,
            "supporting_evidence": [
                "Wirecard scandal deepens as fraud investigation expands (Source: Financial Times)",
                "Germany probes Wirecard's missing $2 billion (Source: Reuters)"
            ]
        }
        """
    )
    inputs = {
        "entity": {
            "type": "string",
            "description": "The name of the company (e.g., 'Adani Enterprises Limited')."
        }
    }
    output_type = "dict"

    KEYWORDS = "money laundering OR fraud OR tax evasion OR corruption OR scandal"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def forward(self, entity: str) -> dict[str, str | float | None | list[str]]:
        assert isinstance(entity, str), "Entity name must be a string."
        news_list = NewsUtils.get_google_news(entity, self.KEYWORDS)
        top_negative_news = NewsUtils.filter_top_negative_news(news_list, top_n=5)
        output = {
            "entity": entity,
            "risk_score": None,
            "confidence": None,
            "supporting_evidence": []
        }
        risk_scores = []
        confidences = []
        for article in top_negative_news:
            risk_scores.append(article.get("neg_sentiment_score", 0))
            confidences.append(article.get("confidence", 0))
            evidence = f"{article['title']} (Source: {article['link']}) (Published: {article['published']})"
            output["supporting_evidence"].append(evidence)
        if risk_scores:
            avg_risk = np.mean(risk_scores)
            avg_confidence = np.mean(confidences)
        else:
            avg_risk = 0
            avg_confidence = 0
        output["risk_score"] = round(avg_risk / 10, 2)
        output["confidence"] = round(avg_confidence / 100, 2)
        return output


if __name__ == "__main__":
    tool = MoneyLaunderingNewsRetrieverTool()
    result = tool.forward("Adani Enterprises Limited")
    print("AML News Retriever Tool Output:")
    print(result)
