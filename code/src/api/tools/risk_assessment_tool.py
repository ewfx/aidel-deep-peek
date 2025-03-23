from smolagents import Tool
from .money_laundering_news_retriever import MoneyLaunderingNewsRetrieverTool
from .lei_tool import LegalEntityIdentifierTool
import json


class RiskAssessmentTool(Tool):
    name = "risk_assessment_tool"
    description = (
        """
        Assesses the financial risk of an entity based on available data, including regulatory compliance, 
        news sentiment, and industry-specific risks. This tool integrates various risk assessment models 
        and external tools (e.g., LegalEntityIdentifierTool, MoneyLaunderingNewsRetrieverTool) to compute 
        an overall risk score, confidence level, and reasoning.

        The tool outputs results in JSON format with entity details, jurisdiction, industry, 
        calculated risk score, confidence score, and supporting evidence.

        Example:
        >>> tool = RiskAssessmentTool()
        >>> result = tool.forward("Wirecard AG", "Germany", "financial services")
        >>> print(result)
        {
            "entity": "Wirecard AG",
            "jurisdiction": "Germany",
            "industry": "financial services",
            "risk_score": 0.85,
            "confidence": 0.90,
            "reason": "Wirecard AG has a history of financial fraud and negative media coverage.",
            "supporting_evidence": [
                "Wirecard scandal deepens as fraud investigation expands (Source: Financial Times)",
                "Germany probes Wirecard's missing $2 billion (Source: Reuters)"
            ]
        }
        """
    )

    inputs = {
        "transaction_id": {
            "type": "string",
            "description": "Transaction ID (e.g. TXN-2023-5A9B)"
        },
        "entity": {
            "type": "string",
            "description": "name of entity (e.g., ['Goldman Sachs', 'Adani Group', etc.])."
        },
        "jurisdiction": {
            "type": "string",
            "description": "The jurisdiction of the entities (e.g., ['United States', 'EU', etc])."
        },
        "industry": {
            "type": "string",
            "description": "The industry of the entity (e.g., ['banking', 'insurance', etc.])."
        }
    }

    output_type = "string"

    def forward(self, transaction_id: str, entity: str, jurisdiction: str, industry: str) -> str:
        total_risk_score = 0.0
        total_confidence = 0.0
        ml_news_result = json.loads(MoneyLaunderingNewsRetrieverTool().forward(entity))
        lei_result = json.loads(LegalEntityIdentifierTool().forward(entity, jurisdiction, industry))

        entity_risk_score = ml_news_result.get("risk_score", 0) + lei_result.get("risk_score", 0)
        entity_confidence = ml_news_result.get("confidence", 0) + lei_result.get("confidence", 0)

        total_risk_score += entity_risk_score
        total_confidence += entity_confidence

        reason_ml_news = ml_news_result.get("supporting_evidence", [])
        reason_lei = ""
        if lei_result.get("lei") is None and lei_result.get("lei_required") is True:
            reason_lei = lei_result.get("reason")

        avg_risk_score = total_risk_score / 2
        final_risk_score = min(10.0, max(1.0, avg_risk_score))
        final_confidence = min(1.0, max(0.0, total_confidence / 2))
        res = {
            "transaction_id": transaction_id,
            "entities": entity,
            "risk_score": final_risk_score,
            "confidence": final_confidence,
            "reason": f"{reason_ml_news} {reason_lei}"
        }
        return json.dumps(res, indent=2)
