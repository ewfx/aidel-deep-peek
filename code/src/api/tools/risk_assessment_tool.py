from .money_laundering_news_retriever import MoneyLaunderingNewsRetrieverTool
from .lei_tool import LegalEntityIdentifierTool
from .opensanctions_tool import search_opensanctions_default_data, search_consolidated_sanctions_data, search_debarred_entities_data, search_regulatory_watchlist_data, search_warrants_criminals_data, search_peps_data
import json
from .tools import ofac_api, pep_api, sec_api, tax_havens_api


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
                ofac_result = ofac_api(entity)
                pep_result = pep_api(entity)
                tax_havens_result = tax_havens_api(jurisdiction)
                # opensanctions_master_data_result = search_opensanctions_default_data(entity)
                # opensanctions_master_data_result = []
                # consolidated_sanctions_result = search_consolidated_sanctions_data(entity)
                # debarred_entities_result = search_debarred_entities_data(entity)
                # regulatory_watchlist_result = search_regulatory_watchlist_data(entity)
                # warrants_criminals_result = search_warrants_criminals_data(entity)
                # peps_result = search_peps_data(entity)
                
                entity_risk_score = ml_news_result.get("risk_score", 0) + lei_result.get("risk_score", 0) + ofac_result.get("risk_score", 0) + pep_result.get("risk_score", 0) + tax_havens_result.get("risk_score", 0)
                entity_confidence = ml_news_result.get("confidence", 0) + lei_result.get("confidence", 0) + ofac_result.get("risk_score", 0) + pep_result.get("risk_score", 0) + tax_havens_result.get("risk_score", 0)

                total_risk_score += entity_risk_score
                total_confidence += entity_confidence
                reasons.append(ml_news_result.get("supporting_evidence", []))
                reasons.append(ofac_result.get("supporting_evidence", []))
                reasons.append(pep_result.get("supporting_evidence", []))
                reasons.append(tax_havens_result.get("supporting_evidence", []))
                # reasons.append(opensanctions_master_data_result.get("evidence", []))
                # reasons.append(consolidated_sanctions_result.get("evidence", []))
                # reasons.append(debarred_entities_result.get("evidence", []))
                # reasons.append(regulatory_watchlist_result.get("evidence", []))
                # reasons.append(warrants_criminals_result.get("evidence", []))
                # reasons.append(peps_result.get("evidence", []))


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

if __name__ == "__main__":
    tool = RiskAssessmentTool()
    print(tool.forward([{'transaction_id': 'txn0qahp',
  'entity_list': ['Global Horizons Consulting LLC',
   'Bright Future Non-Profit Inc.',
   'Maria Gonzalez',
   'Masood Azhar',
   'Mr. Ali Al-Mansoori'],
  'jurisdiction_list': ['Switzerland',
   'Cayman Islands',
   'Not specified',
   'British Virgin Islands',
   'Pakistan'],
  'industry_list': ['Consulting',
   'Non-Profit',
   'Oil and Gas',
   'Finance',
   'Trading'],
  'sus_statements': ['Lack of linked invoice',
   'Use of NordVPN with a Panama exit node']}]))

