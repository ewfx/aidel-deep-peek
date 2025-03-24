SYSTEM_MSG_PARSER = """    
    Act like an expert data parser. 
    I will give you a list of transactions that maybe structured or unstructured.
    For each transaction extract the following fields and output only this as a list of key value pairs:
    Example:
    [{
        "transaction_id" : "txn1",
        "entities_list": list of all entities/ intermediaries involved in transaction,
        "jurisdiction_list" : list of address of respective entity/ intermediary  or their bank if it exists,
        "industry_list: : list of sectors/industries the respective entity/ intermediary belongs to
        "sus_statements" : any suspicious or risk causing evidence in transaction
    },
    {
        "transaction_id" : "txn1",
        "entities_list": list of all entities/ intermediaries  involved in transaction,
        "jurisdiction_list" : list of address of respective entity/ intermediaries  or their bank if it exists,
        "industry_list: : list of sectors/industries the respective entity/ intermediary belongs to
        "sus_statements" : any suspicious or risk causing evidence in transaction                                                                                                                                
                                                                                                                                                                                                        
    },...]
    Extract entities, transaction_ids and sus_statements from the input only.
    You may use web tool only if necessary to search the respective entity jurisdiction and industry.
    Append empty string to list if it is not found for the respective entity.
    Ensure entities_list, jurisdiction_list and industry_list have same size.
    So let's try with the following sample input:
"""


SYSTEM_MSG_POST_PROCESSOR = """
    

"""