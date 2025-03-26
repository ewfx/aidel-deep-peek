import pandas as pd
import os
import re
from rapidfuzz import process, fuzz

# Path to FATF.csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'data/fatf_data/FATF.csv')

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
    # Remove non-alphanumeric characters except spaces
    text = ''.join(e for e in text if e.isalnum() or e.isspace())
    # Remove "of" and "the" as whole words using regex
    text = re.sub(r'\b(of|the)\b', '', text)
    # Remove extra spaces
    return re.sub(r'\s+', ' ', text).strip()

def search_country(df, search_term, column_name, threshold=80):
    # Normalize the search term
    search_term = normalize_text(search_term)
    
    # Normalize all values in the specified column
    normalized_values = df[column_name].dropna().apply(normalize_text)
    
    # Get matches using both token_set_ratio and token_sort_ratio
    matches_set = process.extract(search_term, normalized_values, limit=5, scorer=fuzz.token_set_ratio)
    matches_sort = process.extract(search_term, normalized_values, limit=5, scorer=fuzz.token_sort_ratio)

    # Combine and deduplicate results by taking the best score for each match
    combined_matches = {}
    for match in matches_set + matches_sort:
        if match[0] not in combined_matches:
            combined_matches[match[0]] = match[1]
        else:
            combined_matches[match[0]] = max(combined_matches[match[0]], match[1])

    # Find the best match above the threshold
    best_match = max(combined_matches.items(), key=lambda x: x[1], default=(None, 0))
    
    if best_match[1] >= threshold:
        matched_index = normalized_values[normalized_values == best_match[0]].index[0]
        match = df.loc[matched_index]
        if column_name == "Countries":
            return {
                "country": match['Countries'],
                "evidence": f"This country is present in FATF {match['Category']} List. Source: https://www.fatf-gafi.org/en/countries/black-and-grey-lists.html",
                "risk_score": best_match[1] * 0.01
            }
        else:
            return {
                "entity": "",
                "evidence": "",
                "risk_score": 0
            }
    
    return {"entity": "", "evidence": "", "risk_score": 0}

# Main function
def main(input_address):
    df = load_csv(file_path)
    result = search_country(df,input_address,"Countries",threshold=65)
    print(input_address)
    print("Search Result:", result)
    return result

# Example Usage
if __name__ == "__main__":
    country_address = "Jean-Pierre, Rue 15, 23, Port-au-Prince, Ouest, HAITI"
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