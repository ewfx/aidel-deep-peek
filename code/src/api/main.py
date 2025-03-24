from base.risk_parser_agent import RiskParserAgent
from tools.risk_assessment_tool import RiskAssessmentTool
from utils import SYSTEM_MSG_PARSER, SYSTEM_MSG_POST_PROCESSOR
# from utils.integrated_report_generator import IntegratedReportGenerator
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
        # parsed_transaction = RiskParserAgent().process(query=self.query,
        #                                                sys_msg=self.SYSTEM_MSG_PARSER)
        # print(type(parsed_transaction))
        # if isinstance(parsed_transaction, str):
        #     parsed_transaction = json.loads(parsed_transaction)
        # parsed_transaction = list(parsed_transaction)
        # _tool = RiskAssessmentTool()
        # _res = json.loads(_tool.forward(parsed_transaction))
        # print(type(_res))
        _res = {"results": [
    {
      "transaction_id": "TXN-2023-7C2D",
      "entity_list": [
        "Adani Group",
        "Masood Azhar",
        "Quantum Holdings Ltd"
      ],
      "jurisdiction_list": [
        "Ahmedabad, India",
        "Cayman Islands",
        "British Virgin Islands (BVI)"
      ],
      "industry_list": [
        "Infrastructure & Resources",
        "",
        "Investment"
      ],
      "risk_score": 1,
      "confidence": 1,
      "reason": [
        "Linked invoice missing",
        "Sender IP: 192.168.89.123 (VPN detected: NordVPN, exit node in Panama)",
        [
          "Adani Group stocks plunge up to 20% after Gautam Adani’s indictment in US on bribery and fraud charges; R - The Times of India (Source: https://news.google.com/rss/articles/CBMilAJBVV95cUxQZFMyX1doQTZ2Tk5lbVgyS3BEeDZEMUZWb2V5YWF5TUI4NWFUdGR1dVF5ZmZuMnU5UmJTeEFiLUVQQXhNTmJ1dnM0MmJrUjdNTEt0ZFpQck5zeFNkQUFFZ0RrSmo1RnVrSFNQUUEtRHpjN24wdzZ1MGZHcm13ZVllbm91bklfbnN5UXVhRkh1SW43TlF3dmlQX2NyYlpuX1ozRmRIenVVYjdWcGJjOTRkWHJzSGpPNEliazlHMGdnQm9kbk1YNzFCbGh5MHBUcERLel80aUc2MXVMSmpYVFJzVm1yYjQyd2RnQ3htWTVfRm9ETk9LdzFDdndMNkF0NUtXMlM3SUJpQVZVUWdIWWE5ck85aFnSAZoCQVVfeXFMUEhsWlZEWGNORmdKU1BDcm11QUtsamt3R0psQ1NkNXJ3WmxjZlJ5dThzdEpfeHJhaFdUWF9mTkxQSkdJOHYzY1duMHZaY1g4MVE3NkRsNEJ5U0hyQmktcXd4Q0pRWWxObW51Uk1wUlludWlFZ2hub1ZVR192T1N0UDg4STZseXBGb0psMm5jQ0RRbmwtTXU4c3k0QmtYcUJ6MzRZQXFhZTcxcHRtOGV3QnNXcUV5b21mM0NOdi1VSzFHdXZJWklscm1SaU1teTdhbS1UNXJjWjRkVnJULTZwR05DSW5BOWxSNmV1NWxuZFlobklBaW1pZllaMEd1a0UtYmxYeGwxLUE5cU16M3k1MjdJT2lwNDhtRG9n?oc=5) (Published: Thu, 21 Nov 2024 08:00:00 GMT)",
          "Adani Group bonds plunge after Gautam Adani faces bribery and fraud charges in the US - Mathrubhumi English (Source: https://news.google.com/rss/articles/CBMi1gFBVV95cUxOcV9jMXAwNTZZZkg3dzd6S1JFUkNkbFZkbHhlc0NFdDd4Z2J5dnlobWpFeTFzSG9hNnJocTEySEx3T3Jra0pLcU1nbExEY2hyR0FNNVlEdGM0THBzemhyQ3puUG91UDcxZlpicWxxYk1OQzBrdFVSelNwU0otVkRMZXg5eEpsNjVJZWc2a2cyX1ZaNXhpNi1tQ200aTJvc3RNb2h1X3ZDc2xWN1E2Ri14R080QXc0NG92VE5FLV9xWUp3b2FYM2J0eFR2RlFVbU12d1ltUzdR0gHbAUFVX3lxTFAwUmowZ0JUSE1yYVd1eHplN3Y5a19SSHFjWEV0bjlWNE8zcTNsRUJHUXluZ0RWUS1ZVGF5cjAtZndLb1VYM0hSYzVZSHdDeU1GRHJUQmg0QThIX3RqTzE4LUhmQVhzcXF6Q3ZMTGI4LWFUMnZCQ0I1bnJjVEd4UGNDWlJUamVvVWprTHRwM1hxdWV3RFNlcEVzQ0ZENkhnV2I1T19udkk3cU9qa1cySl8yVHU0ZWd3a3FKVVJINURFUVo3SE5oc3VRV28yeXZPSE5qZjdSejBoMXQzNA?oc=5) (Published: Thu, 21 Nov 2024 08:00:00 GMT)",
          "Billionaire Gautam Adani of India's Adani Group charged in US with bribery, fraud - Reuters (Source: https://news.google.com/rss/articles/CBMikwFBVV95cUxObkp3aUxVVFUtcEpjbFFsdDRoLVpqQ2pnQzl0ZXBqQlFsRk1FbWcxcmRiSEliNjYwYkI3YVYzZGR4QTJCQjVNb0xpVUZrQy1UY2FWdnBOanF2enJvWE1ocTFORjRlWEJZWDQzd0tvcDd0ZU9HNlNmZ2ozX0pYRDl0V1pIY0pUd0hTR2pHZlBRN1dwZkE?oc=5) (Published: Wed, 20 Nov 2024 08:00:00 GMT)",
          "Kenya cancels proposed power transmission deal with Adani Group following US bribery indictment scandal - Mint (Source: https://news.google.com/rss/articles/CBMi9gFBVV95cUxPNmFKMlhGRkRHNFZvMXlNM3NFTWZyYmVfekpoNlJJVnpTYWhYUmp2NllkNDlzUGRUZjVLYmRWZWxZVHZmYXhnXy12WnJjV2lySTcyWmliSmRILXJ4MlNlWjU4bEtaZ1ZZR2hBVlVfajJWRTd6MllpRVFYZUl5Z18zZmtKbDF3T1pUaUJuMzZ6RV9NaXg5NHZaZ3dFYm5qNjN2ZmNBOTZXZzg0NEZsRTNSeUJBLTZManlFZ2tzZHpCX2VqaExMaXdWS3h3OWM0bzlPWnNubXMwMVAzM0xrbGpPYTBTQXhoS1MzZ1pBbkg4ZWpSMGFuQlHSAfsBQVVfeXFMTzRmaGlPYjU0UUNiSEpVbDZJQWFtNlRRR0ljTmZiMW02Nm42T2gtLXpyTGlFNFA1RUZ4cEJNSUJ4WjF1eTB2NEU0bTZXQjNxajFTZnJJamZuYVg2MjBLcmRRbEYtOExyUURHZklqbkJ5aHIzaXhfVTFUeThYMHdWb2hyZ1RoS0pjOTJEbEhncTdlaUtEcnJuQzVzb0dUeU41UFVBNTVNODFPeF9rRjE3VC1DUjF6aGMtMlozREFER1pxb2xoNDY2YV9xc2hjX2JDajNOS1R0cTB6WGFCcGhocmtQNGRJeU5YZ1FvYUZUSV9teHBueTRWYUlRNk0?oc=5) (Published: Thu, 21 Nov 2024 08:00:00 GMT)",
          "Kenya eyes $1.85bn JKIA deal with Adani Group amid fraud, tax evasion concerns - The Africa Report (Source: https://news.google.com/rss/articles/CBMitwFBVV95cUxQSGZLYy01ZWw4bDZnMV9YeGtmNjZOaEVGS0RhX2hvLV93Vkt0VHpZdEFyM1lhYnVRQnRNMkhKdl9YLUZRRGE4SXBnSDlxR1U1RGwybXJhVTlPMk5qYzJNLUx2S211LTQ3eGFhRExST0xJZU1McUpwY2RHbUNVcUs2cl9VMEd6amlsMVFmdjVDSUNpT0hPbEFKckgxeTdENzAxVUFNY25BbkpIdG9adl9kdUNheWktZE0?oc=5) (Published: Mon, 05 Aug 2024 07:00:00 GMT)"
        ],
        "",
        "",
        "",
        "",
        "",
        [
          "Pakistan fails to fulfil 6 key mandates of FATF; no action against Masood Azhar, Hafiz Saeed - Mint (Source: https://news.google.com/rss/articles/CBMi3wFBVV95cUxQRlZleFI5VmU1bllwV0RidzdKeGVqOGwxN2laODJrTTR2czUzM2RxZ3RKLUNNR0dscFFnX2JXdHhFVjNDZl9rbEtyMHNoRTRSblRfZTZSUExSSEhXcXpMNF80TXJWNmVmUFlaVzV0YncxUmtjVHJVVFBvb0lsTlFPQ0FvSHhpa2ZadFl6ZFJjOVp3SDNzR2YxVndXdWdGb0RhVV9ub2l5UzFZZHZJcTJlU1VDaHVfcEp0Qjg3TUJRem12LWExeF80cjI4NUY3U0VkSk81al9YSDBIN2o3WXow0gHkAUFVX3lxTE9Vczl3bVZuZ3V0TUJnOUhoa1lwZUx6VnhnQi1TU1lCaVlweng1X0JIZFNJQmxBRl9mRTVOQXdIek1JZXFzREpEbW5PZUVjSW9PaTRnbEFxdG93MmtMQ1FObEhRdXlvS0l5M2s2S2ZvcE14MU0tazdrQUdKc29paUFoMWRWX1BmR3ZKNHhvR3c2Zmk2UDNwVkhLM3lhTU1pRkFITlQ4a0x1dGdkMF9VVTdCZXpJQmpteG1tYXNad1JvMnRMajVYbk14QXhOWW1JS1ltdm5OLXM2VktPVlVERWVXSkEzeA?oc=5) (Published: Sun, 18 Oct 2020 07:00:00 GMT)",
          "Pakistan puts Dawood Ibrahim, Masood Azhar, Hafiz Saeed, Zaki-ur-Rahman Lakhvi on terror list - The Hindu (Source: https://news.google.com/rss/articles/CBMi6gFBVV95cUxNNS12eThCRWF4X05pOEpmVEpUVkNaeHNJbGlDblhneWthVm9Qc3p6RlA3cHlHOU1KaHhwQ2xkSzhwWlRfVEZ2RTgwV2FINFEwNFlTTzJnRWFuVlJXVW5nZ1lQbWFNZzRiWEFMRFp3OHVoSW1OTExfOGZWY0stZjhiZ1VFU0hCTjhaMURFbkE5anFRUkF2UlVPbWVROWJLLUNpNGZZdmNtZjNIRzVBa094eUZFb3RwTmpabklra1BKRlYxSnBwaGxucVRxV0RlcDRfUTlRazZ1NzdRaXZZeEh4bFNZVGxiTkwxV1HSAfABQVVfeXFMUFpCSWYtX2JoOEFET1o1dnM4dUVheDhOa1V2N0x3YU1RTXNIamV4WG5UakZkdHF2WFk3TjM3ZDhUSTFmRFc0Y1NBa2gyZWJIZ3oyOG1mQUdkZ3llYVVNRHozNDFzS3FnQlRuRDNCQmkwWmZKdmlDVHc4eE1oMUhVZ05rSnFTRzNoc19UTmo2TFdmZFdndTR1alNnMF9lRmdWWlhsaGVWTUlGbmoxU2FkS3UzTU5YeVE0UTFZSzNRcGNzSTZRa0VFMGptMUFScUdJRU9RNnRieXVqZW1yOU40aXhxdlFkc0VCMmo4ejVVRHBf?oc=5) (Published: Sat, 22 Aug 2020 07:00:00 GMT)"
        ],
        "ofac: [1528 'ALVI, Mohammad Masood Azhar'] is a ofac.",
        "",
        "",
        "",
        "",
        [],
        "",
        "",
        "",
        "",
        ""
      ]
    }
  ]
}
        return _res

    # def post_process(self, ):
    #     IntegratedReportGenerator().generate()


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
