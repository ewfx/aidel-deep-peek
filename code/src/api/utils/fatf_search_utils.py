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

def search_country(df, search_term, column_name, threshold=40):
    search_term = normalize_text(search_term)
    
    # Get matches with scores
    matches = process.extract(search_term, df[column_name].dropna().apply(normalize_text), limit=1, scorer=fuzz.token_set_ratio)

    # Filter matches above threshold
    best_matches = [(df.iloc[match[2]], match[1]) for match in matches if match[1] >= threshold]
    
    # Prepare JSON output
    result = []
    if best_matches:
        for match, score in best_matches:
            if column_name == "Countries":
                result.append({
                    "country": match['Countries'],
                    "category": match['Category'],
                    "evidence": "https://www.fatf-gafi.org/en/countries/black-and-grey-lists.html",
                    "risk_score": score * 0.01
                })
            else:
                result.append({
                    "entity": "",
                    "category": "",
                    "evidence": "",
                    "risk_score": 0
                })
    return result

# Main function
def main(input_address):
    df = load_csv(file_path)
    result = search_country(df,input_address,"Countries")
    print("Search Result:", result)
    return result

# Example Usage
if __name__ == "__main__":
    country_address = "12 Main Street, Pretoria, 0001, South Africa"
    main(country_address)