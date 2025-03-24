from utils.searchUtil_opensanctions_datasets import search_opensanctions, forward

def search_opensanctions_default_data(entity_name: str):
    csv_path = "E:/Hackathon 2025/aidel-deep-peek/code/src/api/tools/opensanctions_data/opensanctions_default_data.csv"
    matches = search_opensanctions(entity_name, csv_path, 90, 1)
    return forward(entity_name, matches)

def search_consolidated_sanctions_data(entity_name: str):
    csv_path = "E:/Hackathon 2025/aidel-deep-peek/code/src/api/tools/opensanctions_data/consolidated_sanctions.csv"
    matches = search_opensanctions(entity_name, csv_path, 90, 1)
    return forward(entity_name, matches)

def search_debarred_entities_data(entity_name: str):
    csv_path = "E:/Hackathon 2025/aidel-deep-peek/code/src/api/tools/opensanctions_data/debarred_companies_individuals.csv"
    matches = search_opensanctions(entity_name, csv_path, 90, 1)
    return forward(entity_name, matches)

def search_regulatory_watchlist_data(entity_name: str):
    csv_path = "E:/Hackathon 2025/aidel-deep-peek/code/src/api/tools/opensanctions_data/regulatory_watchlist.csv"
    matches = search_opensanctions(entity_name, csv_path, 90, 1)
    return forward(entity_name, matches)

def search_warrants_criminals_data(entity_name: str):
    csv_path = "E:/Hackathon 2025/aidel-deep-peek/code/src/api/tools/opensanctions_data/warrants_criminals.csv"
    matches = search_opensanctions(entity_name, csv_path, 90, 1)
    return forward(entity_name, matches)

def search_peps_data(entity_name: str):
    csv_path = "E:/Hackathon 2025/aidel-deep-peek/code/src/api/tools/opensanctions_data/peps.csv"
    matches = search_opensanctions(entity_name, csv_path, 90, 1)
    return forward(entity_name, matches)


def main():
    # Example usage
    try:
        result = search_debarred_entities_data("masood azhar")
        
        if result:
            print("Match found:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("No matches found")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 





