from tools.risk_assessment_tool import RiskAssessmentTool
from datetime import datetime, timedelta
tool = RiskAssessmentTool()
print(tool.forward([{'transaction_id': 'txn0qahp',
  'entities_list': ['Global Horizons Consulting LLC',
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

