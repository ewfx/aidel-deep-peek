import pandas as pd
import numpy as np
from thefuzz import process;
from langchain_core.tools import tool
from sec_api import QueryApi
import requests


SEC_API_KEY = ""
queryApi = QueryApi(api_key=SEC_API_KEY)
LITIGATION_URL = "https://api.sec-api.io/sec-litigation-releases"
ENFORCEMENT_URL = "https://api.sec-api.io/sec-enforcement-actions"


@tool
def ofac_api(name:str) -> list:
    ofac_df = pd.read_csv('./ofac_sdn_list.csv')
    ofac_list = np.array(ofac_df)
    return_list = process.extractWithoutOrder(name,choices=ofac_list,limit=10,score_cutoff=80)
    return return_list


@tool
def pep_api(name:str) -> list:
    peps_df = pd.read_excel('./peps.xlsx')
    peps_list = np.array(peps_df)
    return process.extractWithoutOrder(name,choices=peps_list,limit=10,score_cutoff=80)

@tool
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