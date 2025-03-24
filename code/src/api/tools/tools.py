import pandas as pd
import numpy as np
from thefuzz import process

def ofac_api(name:str) -> dict:
    
    ofac_df = pd.read_csv(r'C:\Users\nmabh\Desktop\DeepPeek\aidel-deep-peek\code\src\api\tools\ofac_sdn_list.csv')
    ofac_list = np.array(ofac_df)
    return_list = process.extractOne(name,choices=ofac_list,score_cutoff=90)
    risk_score = return_list[1] if return_list!=None else 0
    supporting_evidence= "" if return_list==None else (f"ofac: {return_list[0]} is listed on OFAC sanctions list, particularly the Specially Designated Nationals and Blocked Persons List(SDN List), which includes individuals and entities such as terrorists, officials of certain regimes, and international criminals. Their U.S. assets are blocked, and U.S. persons are generally prohibited from dealing with them. Source - https://sanctionslist.ofac.treas.gov/Home/SdnList .")
    return {"risk_score":risk_score,"supporting_evidence":supporting_evidence}


def pep_api(name:str) -> dict:
    peps_df = pd.read_excel(r'C:\Users\nmabh\Desktop\DeepPeek\aidel-deep-peek\code\src\api\tools\peps.xlsx')
    peps_list = np.array(peps_df)
    pep_result = process.extractOne(name,choices=peps_list,score_cutoff=90)
    risk_score = pep_result[1] if pep_result!=None else 0
    supporting_evidence = "" if pep_result==None else (f"pep: {pep_result[0]} is a pep.")
    return {"risk_score":risk_score,"supporting_evidence":supporting_evidence}


def tax_havens_api(country:str) -> dict:
    tax_havens_df = open(r'C:\Users\nmabh\Desktop\DeepPeek\aidel-deep-peek\code\src\api\tools\tax_havens.txt')
    tax_havens_list = tax_havens_df.readlines()
    score = 1 if country in tax_havens_list else 0
    evidence = f"country: {country} is a tax haven." if score == 1 else ""
    return {"risk_score":score,"supporting_evidence": evidence}
