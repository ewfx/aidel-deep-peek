import pandas as pd
import os
import re

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

def search_country(input_address, df):
    if df.empty:
        return {"country": "", "category": "", "evidence": "", "risk_score": 0}
    
    # Normalize input address and countries
    input_words = set(normalize_text(input_address).split())
    df['Normalized_Country'] = df['Countries'].apply(normalize_text)

    # Check for any word match
    for _, row in df.iterrows():
        country_words = set(row['Normalized_Country'].split())
        if input_words.intersection(country_words):
            return {
                "country": row['Countries'],
                "category": row['Category'],
                "evidence": "https://www.fatf-gafi.org/en/countries/black-and-grey-lists.html",
                "risk_score": 1
            }
    
    # No match found
    return {"country": "", "category": "", "evidence": "", "risk_score": 0}

# Main function
def main(input_address):
    df = load_csv(file_path)
    result = search_country(input_address, df)
    print("Search Result:", result)
    return result

# Example Usage
if __name__ == "__main__":
    country_address = "Democratic Republic of the Congo"
    main(country_address)