import pandas as pd
from rapidfuzz import fuzz, process
import sys

def load_data(csv_path):
    """Load the CSV data into a pandas DataFrame"""
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

def search_entity(df, query, threshold=80):
    """
    Perform fuzzy search on the DataFrame
    Returns matches above the threshold with their details
    """
    # Combine name fields for better matching
    df['search_text'] = df['name'].fillna('') + ' ' + \
                       df['first_name'].fillna('') + ' ' + \
                       df['last_name'].fillna('') + ' ' + \
                       df['aliases'].fillna('')
    
    # Get matches using rapidfuzz
    matches = process.extract(query, df['search_text'], limit=5)
    
    results = []
    for match, score, idx in matches:
        if score >= threshold:
            record = df.iloc[idx]
            results.append({
                'match_score': score,
                'name': record['name'],
                'aliases': record['aliases'],
                'sanctions': {
                    'programs': record['sanction_programs'],
                    'types': record['sanction_types'],
                    'reasons': record['sanction_reasons'],
                    'authorities': record['sanction_authorities'],
                    'statuses': record['sanction_statuses'],
                    'summaries': record['sanction_summaries'],
                    'provisions': record['sanction_provisions'],
                    'listing_dates': record['sanction_listing_dates'],
                    'source_urls': record['sanction_source_urls'],
                    'summary': record['sanctions_full']
                }
            })
    
    return results

def print_results(results):
    """Print the search results in a formatted way"""
    if not results:
        print("No matches found above the threshold.")
        return
    
    for result in results:
        print("\n" + "="*80)
        print(f"Match Score: {result['match_score']}%")
        print(f"Name: {result['name']}")
        print(f"Aliases: {result['aliases']}")
        
        print("\nSanction Details:")
        print("-"*40)
        sanctions = result['sanctions']
        
        if sanctions['programs']:
            print(f"Programs: {sanctions['programs']}")
        if sanctions['types']:
            print(f"Types: {sanctions['types']}")
        if sanctions['reasons']:
            print(f"Reasons: {sanctions['reasons']}")
        if sanctions['authorities']:
            print(f"Authorities: {sanctions['authorities']}")
        if sanctions['statuses']:
            print(f"Statuses: {sanctions['statuses']}")
        if sanctions['summaries']:
            print(f"Summaries: {sanctions['summaries']}")
        if sanctions['provisions']:
            print(f"Provisions: {sanctions['provisions']}")
        if sanctions['listing_dates']:
            print(f"Listing Dates: {sanctions['listing_dates']}")
        if sanctions['source_urls']:
            print(f"Source URLs: {sanctions['source_urls']}")
        if sanctions['summary']:
            print(f"Summary: {sanctions['summary']}")

def main():
    # Load the CSV data
    df = load_data('consolidated_sanctions_data.csv')
    if df is None:
        return
    
    while True:
        # Get search query from user
        query = input("\nEnter the entity name to search (or 'q' to quit): ").strip()
        
        if query.lower() == 'q':
            break
        
        if not query:
            print("Please enter a search term.")
            continue
        
        # Perform search
        results = search_entity(df, query)
        
        # Print results
        print_results(results)

if __name__ == "__main__":
    main()