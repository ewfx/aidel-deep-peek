import requests
import pandas as pd
import os
from datetime import datetime
from rapidfuzz import process
import re
import json

# API URLs
SDN_URL = "https://sanctionslistservice.ofac.treas.gov/api/download/SDN.CSV"
ALT_URL = "https://sanctionslistservice.ofac.treas.gov/api/download/ALT.CSV"

# Get the current script's directory (src)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder Paths
SDN_FOLDER = os.path.join(BASE_DIR, "ofac_sanctions_data", "SDN")
ALT_FOLDER = os.path.join(BASE_DIR, "ofac_sanctions_data", "ALT")

# Create directories if not exists
os.makedirs(SDN_FOLDER, exist_ok=True)
os.makedirs(ALT_FOLDER, exist_ok=True)

# Download and save CSV
def download_and_save_csv(url, folder, prefix):
    try:
        print(f"Downloading from: {url}")
        response = requests.get(url)
        response.raise_for_status()

        # Generate filename with current date
        date_str = datetime.now().strftime('%Y-%m-%d')
        file_path = os.path.join(folder, f"{prefix}_{date_str}.csv")

        # Save file
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"File saved at: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error downloading CSV: {e}")
        return None

# Check if today's file exists
def is_file_present(folder, prefix):
    date_str = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{prefix}_{date_str}.csv"
    return os.path.exists(os.path.join(folder, file_name))

# Perform task - Download if necessary
def perform_task():
    current_time = datetime.now().strftime('%H:%M')
    print(f"Current Time: {current_time}")

    # Check for 12:00 AM
    if current_time == "00:00" or not is_file_present(SDN_FOLDER, "sdn") or not is_file_present(ALT_FOLDER, "alt"):
        print("Downloading files...")
        download_and_save_csv(SDN_URL, SDN_FOLDER, "sdn")
        download_and_save_csv(ALT_URL, ALT_FOLDER, "alt")
    else:
        print("Files are already present. No need to download.")

# Get the latest file from folder
def get_latest_file(folder, prefix):
    files = [f for f in os.listdir(folder) if f.startswith(prefix) and f.endswith('.csv')]
    if not files:
        print(f"No files found in {folder}. Please download first.")
        return None
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(folder, f)))
    print(f"Using latest file: {latest_file}")
    return os.path.join(folder, latest_file)

# Load CSV without headers (for SDN)
def load_csv(file_path, has_headers=True):
    try:
        print(f"Loading CSV: {file_path}")
        return pd.read_csv(file_path, dtype=str, on_bad_lines='skip', header=0 if has_headers else None)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

# Extract columns from SDN
def extract_sdn_data(df):
    try:
        df_sdn = df.iloc[:, [1, 3]]
        df_sdn.columns = ["Entity Name", "Country"]
        return df_sdn
    except Exception as e:
        print(f"Error extracting SDN data: {e}")
        return pd.DataFrame()

# Extract columns from ALT
def extract_alt_data(df):
    try:
        df_alt = df.iloc[:, [3]]
        df_alt.columns = ["Alias Name"]
        return df_alt
    except Exception as e:
        print(f"Error extracting ALT data: {e}")
        return pd.DataFrame()

def normalize_text(text: str) -> str:
    if pd.isna(text):
        return ""
    
    # Convert to string and lowercase
    text = str(text).lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Normalize spaces (replace multiple spaces with single space)
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing spaces
    return text.strip()

# Perform Fuzzy Search
from rapidfuzz import process

# Perform Fuzzy Search and Return Top 3 Results with Scores
# def fuzzy_search_data(df, search_term, column_name, threshold=80):
#     search_term = normalize_text(search_term)
    
#     # Get matches with scores
#     matches = process.extract(search_term, df[column_name].dropna().apply(normalize_text), limit=3)
    
#     # Filter matches above threshold
#     best_matches = [(df.iloc[match[2]], match[1]) for match in matches if match[1] >= threshold]
    
#     if best_matches:
#         print(f"\n✅ Top {len(best_matches)} results for '{search_term}' in the {column_name} with their similarity scores:")
#         if column_name == "Entity Name":
#             for match, score in best_matches:
#                 print(f"Entity: {match['Entity Name']} | Country: {match['Country']} | Score: {score}")
#         else:
#             for match, score in best_matches:
#                 print(f"Alias: {match['Alias Name']} | Score: {score}")
#     else:
#         print(f"\n❌ No matches found for '{search_term}' in the {column_name}.")
def fuzzy_search_data(df, search_term, column_name, threshold=80):
    search_term = normalize_text(search_term)
    
    # Get matches with scores
    matches = process.extract(search_term, df[column_name].dropna().apply(normalize_text), limit=3)
    
    # Filter matches above threshold
    best_matches = [(df.iloc[match[2]], match[1]) for match in matches if match[1] >= threshold]
    
    # Prepare JSON output
    result = []
    if best_matches:
        for match, score in best_matches:
            if column_name == "Entity Name":
                result.append({
                    "entity": match['Entity Name'],
                    "country": match['Country'],
                    "score": score
                })
            else:
                result.append({
                    "entity": match['Alias Name'],
                    "country": None,
                    "score": score
                })
    return result

def main(search_term):
    perform_task()

    sdn_file = get_latest_file(SDN_FOLDER, "sdn")
    alt_file = get_latest_file(ALT_FOLDER, "alt")
    results = {
        "SDN Results": [],
        "ALT Results": []
    }

    if sdn_file:
        sdn_df = load_csv(sdn_file, has_headers=False)
        sdn_data = extract_sdn_data(sdn_df)
        print("Searching in SDN List (Entity Name Only)...")
        results["SDN Results"] = fuzzy_search_data(sdn_data, search_term, "Entity Name")

    if alt_file:
        print("Searching in Alias List...")
        alt_df = load_csv(alt_file, has_headers=False)
        alt_data = extract_alt_data(alt_df)
        results["ALT Results"] = fuzzy_search_data(alt_data, search_term, "Alias Name")

    return json.dumps(results, indent=2)

# Main Function
# def main():
#     perform_task()

#     sdn_file = get_latest_file(SDN_FOLDER, "sdn")
#     alt_file = get_latest_file(ALT_FOLDER, "alt")

#     if sdn_file:
#         sdn_df = load_csv(sdn_file, has_headers=False)
#         sdn_data = extract_sdn_data(sdn_df)

#     if alt_file:
#         alt_df = load_csv(alt_file, has_headers=False)
#         alt_data = extract_alt_data(alt_df)

#     # Choose Search Option
#     search_term = input("Enter Entity Name: ").strip()

#     if sdn_file:
#         print("Searching in SDN List (Entity Name Only)...")
#         fuzzy_search_data(sdn_data, search_term, "Entity Name")
#     else:
#         print("SDN data not available.")

#     if alt_file:
#         print("\nSearching in Alias List...")
#         fuzzy_search_data(alt_data, search_term, "Alias Name")
#     else:
#         print("ALT data not available.")

# if __name__ == "__main__":
#     main()