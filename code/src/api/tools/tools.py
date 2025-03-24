import pandas as pd
import numpy as np
from thefuzz import process;
from langchain_core.tools import tool
from sec_api import QueryApi
import requests

ans = process.extractOne("name",choices=["namesz"],score_cutoff=90)
print(ans[1])


SEC_API_KEY = ""
queryApi = QueryApi(api_key=SEC_API_KEY)
LITIGATION_URL = "https://api.sec-api.io/sec-litigation-releases"
ENFORCEMENT_URL = "https://api.sec-api.io/sec-enforcement-actions"


def ofac_api(name:str) -> dict:
    
    ofac_df = pd.read_csv('E:\\Hackathon 2025\\aidel-deep-peek\\code\\src\\api\\tools\\ofac_sdn_list.csv')
    ofac_list = np.array(ofac_df)
    return_list = process.extractOne(name,choices=ofac_list,score_cutoff=90)
    risk_score = return_list[1] if return_list!=None else 0
    supporting_evidence= "" if return_list==None else (f"ofac: {return_list[0]} is a ofac.")
    return {"risk_score":risk_score,"supporting_evidence":supporting_evidence}


def pep_api(name:str) -> dict:
    peps_df = pd.read_excel('E:\\Hackathon 2025\\aidel-deep-peek\\code\\src\\api\\tools\\peps.xlsx')
    peps_list = np.array(peps_df)
    pep_result = process.extractOne(name,choices=peps_list,score_cutoff=90)
    risk_score = pep_result[1] if pep_result!=None else 0
    supporting_evidence = "" if pep_result==None else (f"pep: {pep_result[0]} is a pep.")
    return {"risk_score":risk_score,"supporting_evidence":supporting_evidence}


def sec_api(ticker:str,date:str) -> dict:
    
    start_date = date[:(len(date)-4)] + str(int(date[(len(date)-4):])-1)
    query = "releasedAt:["+start_date+"TO"+date+"]"
    query = query + "AND" + " entities.ticker:" + ticker
    page = "0"
    size = "50"
    sort = '[{ "releasedAt": { "order": "desc" } }]'
    request = {
        "query":query,
        "from":page,
        "size":size,
        "sort":sort
    }
    litigationData = requests.post(url=LITIGATION_URL,params=request,headers={"Authorization": SEC_API_KEY})
    enforcementData = requests.post(url=ENFORCEMENT_URL,params=request,headers={"Authorization": SEC_API_KEY})
    return {
        "litigation":litigationData.json(),
        "enforcement":enforcementData.json()
    }


def tax_havens_api(country:str) -> dict:
    tax_havens_df = open('E:\\Hackathon 2025\\aidel-deep-peek\\code\\src\\api\\tools\\tax_havens.txt')
    tax_havens_list = tax_havens_df.readlines()
    score = 1 if country in tax_havens_list else 0
    return {"risk_score":score,"supporting_evidence":f"country: {country} is a tax haven."}
