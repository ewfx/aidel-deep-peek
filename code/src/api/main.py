from base.risk_parser_agent import RiskParserAgent
from tools.risk_assessment_tool import RiskAssessmentTool
from utils import SYSTEM_MSG_PARSER, SYSTEM_MSG_POST_PROCESSOR
from base.report_generator import ReportGenerator
from base.report_postprocessor import ReportPostprocessor
import json

import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.environ.get("SERPER_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")


class RiskJSONGenerator:
    def __init__(self, query):
        self.query = query
        self.SYSTEM_MSG_PARSER = SYSTEM_MSG_PARSER
        self.SYSTEM_MSG_POST_PROCESSOR = SYSTEM_MSG_POST_PROCESSOR

    def process(self):
        parsed_transaction = RiskParserAgent().process(query=self.query,
                                                       sys_msg=self.SYSTEM_MSG_PARSER)
        print(type(parsed_transaction))
        if isinstance(parsed_transaction, str):
            parsed_transaction = json.loads(parsed_transaction)
        parsed_transaction = list(parsed_transaction)
        _tool = RiskAssessmentTool()
        _res = json.loads(_tool.forward(parsed_transaction))
        print(type(_res))
        return _res

    def generate_process(self, findings):
        processor = ReportPostprocessor(sys=self.SYSTEM_MSG_POST_PROCESSOR)
        _content = processor.process(findings)
        ReportGenerator().create_pdf(_content)
        return _content


if __name__ == "__main__":
    _query = """
        {
          "Transaction ID": "TXN-2023-7C2D",
          "Date": "2023-08-15 14:25:00",
          "Sender": {
            "Name": "Adani Group",
            "Account": "IBAN CH56 0483 5012 3456 7800 9 (Swiss Bank)",
            "Beneficiary Owner": "Maria Gonzalez",
            "Address" : "rue du marche 17, geneva, switzerland",
            "notes" : "Consulting fees for project aurora"
          },
          "Receiver": {
            "Name": "Aramco",
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
              "Linked invoice missing. Processed via intermediary BSM Marine Ltd",
              "Sender IP: 192.168.89.123 (VPN detected: NordVPN, exit node in Panama)"
            ]
          }
        }
    """
    _obj = RiskJSONGenerator(query=_query)
    print(_obj.process())
