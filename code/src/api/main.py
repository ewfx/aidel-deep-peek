from base.entity_risk_agent import EntityRiskAgent
import os
from dotenv import load_dotenv
load_dotenv()

SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

task = """
{
  "Transaction ID": "TXN-2023-7C2D",
  "Date": "2023-08-15 14:25:00",
  "Sender": {
    "Name": "Global Horizons Consulting LLC",
    "Account": "IBAN CH56 0483 5012 3456 7800 9 (Swiss Bank)",
    "Beneficiary Owner": "Maria Gonzalez",
    "Address" : "rue du marche 17, geneva, switzerland",
    "notes" : "Consulting fees for project aurora"
  },
  "Receiver": {
    "Name": "Bright Future non profit inc",
    "Account": "9847654321 (Cayman National Bank, KY)",
    "Adress": "PO Box 1234, George Town, Cayman Islands"
    "Tax ID" : "KY-45678"
  },
  "Transaction Details": {
    "Amount": "$49,850.00",
    "Currency Exchange": "N/A",
    "Transaction Type": "Wire Transfer",
    "Reference": "Charitable Donation - Ref #DR-2023-0815",
    "Notes": [
      "Urgent Transfer approved by Mr Ali Al-Mansoori(Director).",
      "Linked invoice missing. Processed via intermediary Quantum Holdings Ltd (BVI)",
      "Sender IP: 192.168.89.123 (VPN detected: NordVPN, exit node in Panama)"
    ]
  }
}
"""

input = f"""
You are an AI agent tasked with identifying, verifying, and risk-scoring entities involved
in financial transactions. Given a set of structured and unstructured transaction details, your job is to:
For each transaction in the input:
1. Extract entities involved and prepare an entity_list.
2. Find out the jurisdiction (E.g. US, UK, EU, etc.) for respective entity to create a jurisdiction_list.
3. Find out industry of the respective entity (e.g. banking, insurance, commodities, etc.) to create an industry_list.
4. Use the RiskAssessmentAgent to compute risk score, confidence and reason
5. Use web search whenever necessary and you may formulate a general risk score, confidence and reason for the transaction
   in general and add to the risk assessment tool response.
Do this for each transaction and prepare a final collected output that looks like this for each transaction in input:
Expected Output Format (JSON):
<json>
  "Transaction ID": "TXN001",
  "Extracted Entities": ["Acme Corporation", "SovCo Capital Partners"],
  "Risk Score": 0.65,
  "Confidence Score": 0.85,
  "Reason": "SovCo Capital Partners is owned by Russian businessmen and has direct links to Socombank PJSC, a sanctioned entity."
</json> 
Ensure the results are accurate, well-structured, and provide actionable insights.
Here is the input:
{task}
"""

risk_agent = EntityRiskAgent().manager_agent
print("FINAL ANSWER--------------------------------------------")
print(risk_agent.run(input))
