import pandas as pd
import os
import re
from rapidfuzz import process, fuzz

# Path to TAX_HAVEN.csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'data/tax_haven_data/TAX_HAVEN.csv')

# Load CSV into DataFrame
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print("CSV loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    # Remove numbers and common address words like PO, street, town
    text = re.sub(r'\b(po|box|street|road|town)\b', '', text)
    text = ''.join(e for e in text if e.isalnum() or e.isspace())
    text = re.sub(r'\b(of|the)\b', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def search_country(df, search_term, column_name, threshold=80):
    search_term = normalize_text(search_term)
    
    # Apply both token_set_ratio and token_sort_ratio
    matches_set = process.extract(search_term, df[column_name].dropna().apply(normalize_text), limit=5, scorer=fuzz.token_set_ratio)
    matches_sort = process.extract(search_term, df[column_name].dropna().apply(normalize_text), limit=5, scorer=fuzz.token_sort_ratio)
    
    # Convert matches_sort to a dictionary with string and score
    sort_dict = {match[0]: match[1] for match in matches_sort}
    
    # Combine and deduplicate results
    combined_matches = {match[0]: max(match[1], sort_dict.get(match[0], 0)) for match in matches_set}
    
    # Find the best match above the threshold
    best_match = max(combined_matches.items(), key=lambda x: x[1], default=None)
    
    if best_match and best_match[1] >= threshold:
        matched_index = df[df[column_name].apply(normalize_text) == best_match[0]].index[0]
        country_name = df.at[matched_index, 'Countries']
        evidence = f"{country_name} is identified as a tax haven country. Source: https://cthi.taxjustice.net/full-list"
        return {
            "country": country_name,
            "evidence": evidence,
            "risk_score": best_match[1] * 0.01
        }

    return {"country": "", "evidence": "", "risk_score": 0}

# Main function
def main(input_address):
    df = load_csv(file_path)
    result = search_country(df, input_address, "Countries", threshold=65)
    print(input_address)
    print("Search Result:", result)
    return result

# Example Usage
if __name__ == "__main__":
    country_address = "PO 1234, George Town,Cayman Island"
    main(country_address)

# def main(input_address):
#     df = load_csv(file_path)
#     print(input_address)
#     for country in input_address:
#         result = search_country(df, country, "Countries", threshold=60)
#         print(country)
#         print("Search Result:", result)
        
#     return result

# # Example Usage
# if __name__ == "__main__":
#     countries = ['Switzerland',
#    'Cayman Islands',
#    'Not specified',
#    'British Virgin Islands',
#    'Pakistan']
#     main(countries)