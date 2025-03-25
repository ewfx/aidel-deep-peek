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
    text = ''.join(e for e in text if e.isalnum() or e.isspace())
    text = re.sub(r'\b(of|the)\b', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def search_country(df, search_term, column_name, threshold=80):
    search_term = normalize_text(search_term)
    
    # Get matches with scores
    matches = process.extract(search_term, df[column_name].dropna().apply(normalize_text), limit=1, scorer=fuzz.token_set_ratio)
    
    # Filter matches above threshold
    best_matches = [(df.iloc[match[2]], match[1]) for match in matches if match[1] >= threshold]
    
    # Prepare JSON output
    result = []
    if best_matches:
        for match, score in best_matches:
            country_name = match['Countries']
            evidence = f"{country_name} is identified as a tax haven country. Source: https://cthi.taxjustice.net/full-list"
            result.append({
                "country": country_name,
                "evidence": evidence,
                "risk_score": score * 0.01
            })
    else:
        result.append({
            "country": "",
            "evidence": "",
            "risk_score": 0
        })
    
    return result[0] if result else {"country": "","evidence": "","risk_score": 0}

# Main function
def main(input_address):
    df = load_csv(file_path)
    result = search_country(df, input_address, "Countries", threshold=60)
    print(input_address)
    print("Search Result:", result)
    return result

# Example Usage
if __name__ == "__main__":
    country_address = "Cayman Island national bank"
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