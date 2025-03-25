import pandas as pd
import os
import re
from rapidfuzz import process, fuzz

# Path to AML.csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'data/aml_data/AML.csv')

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
    
    # Get matches with scores using normalized values
    matches = process.extract(search_term, normalized_values, limit=1, scorer=fuzz.token_set_ratio)

    # Filter matches above threshold
    best_matches = [(df.iloc[match[2]], match[1]) for match in matches if match[1] >= threshold]
    
    # Prepare JSON output
    result = []
    if best_matches:
        for match, score in best_matches:
            if column_name == "Countries":
                country_name = match['Countries']
                evidence = f"{country_name} is present in the list of top anti-money laundering countries. Source: https://www.knowyourcountry.com/ratings-table/"
                result.append({
                    "country": country_name,
                    "aml_score": float(match['AML_Score']) if pd.notna(match['AML_Score']) else None,
                    "evidence": evidence,
                    "risk_score": score * 0.01
                })
            else:
                result.append({
                    "entity": '',
                    "aml_score": '',
                    "evidence": "",
                    "risk_score": 0
                })
    return result[0] if result else {"entity": '',"aml_score": '',"evidence": "","risk_score": 0}

# Main function
def main(input_address):
    df = load_csv(file_path)
    result = search_country(df, input_address,"Countries", threshold=65)
    print(input_address)
    print("Search Result:", result)
    return result

# Example Usage
if __name__ == "__main__":
    country_address = "Uzbekistan"
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