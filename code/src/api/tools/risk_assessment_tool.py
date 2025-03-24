from .money_laundering_news_retriever import MoneyLaunderingNewsRetrieverTool
from .lei_tool import LegalEntityIdentifierTool
import json


class RiskAssessmentTool:
    name = "risk_assessment_tool"
    description = """
    Assesses the financial risk of entities from multiple transactions.
    Extracts relevant fields and applies risk assessment tools to compute overall risk score,
    confidence level, and reasoning.
    """

    inputs = {
        "transactions": {
            "type": "list",
            "description": "A list of transaction dictionaries, each containing entity details."
        }
    }

    output_type = "string"

    def forward(self, transactions: list[dict]) -> str:
        results = []

        for txn in transactions:
            transaction_id = txn.get("transaction_id", "Unknown")
            entity_list = txn.get("entities_list", [])
            jurisdiction_list = txn.get("jurisdiction_list", [])
            industry_list = txn.get("industry_list", [])
            sus_statements = txn.get("sus_statements", [])

            total_risk_score = 0.0
            total_confidence = 0.0
            n_tools = 2
            reasons = sus_statements if isinstance(sus_statements, list) else [sus_statements]

            for entity, jurisdiction, industry in zip(entity_list, jurisdiction_list, industry_list):
                ml_news_result = json.loads(MoneyLaunderingNewsRetrieverTool().forward(entity))
                lei_result = json.loads(LegalEntityIdentifierTool().forward(entity, jurisdiction, industry))

                entity_risk_score = ml_news_result.get("risk_score", 0) + lei_result.get("risk_score", 0)
                entity_confidence = ml_news_result.get("confidence", 0) + lei_result.get("confidence", 0)

                total_risk_score += entity_risk_score
                total_confidence += entity_confidence
                reasons.append(ml_news_result.get("supporting_evidence", []))

                if lei_result.get("lei") is None and lei_result.get("lei_required") is True:
                    reasons.append(lei_result.get("reason", ""))

            avg_risk_score = total_risk_score / (len(entity_list) * n_tools) if entity_list else 0.0
            final_risk_score = min(10.0, max(0.0, avg_risk_score))
            final_confidence = min(1.0, max(0.0, total_confidence / (len(entity_list) * n_tools) if entity_list else 1.0))

            txn_result = {
                "transaction_id": transaction_id,
                "entity_list": entity_list,
                "jurisdiction_list": jurisdiction_list,
                "industry_list": industry_list,
                "risk_score": final_risk_score,
                "confidence": final_confidence,
                "reason": reasons
            }
            results.append(txn_result)

        return json.dumps(results, indent=2)
