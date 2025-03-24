import pandas as pd
from rapidfuzz import fuzz
from typing import List, Dict, Tuple
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def normalize_text(text: str) -> str:
    """m
    Normalize text for comparison by:
    1. Converting to lowercase
    2. Removing extra whitespace
    3. Removing special characters
    4. Normalizing spaces
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Normalized text
    """
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

def get_highest_similarity(search_term: str, name: str, aliases: str) -> float:
    """
    Calculate the highest similarity score between search term and name/aliases.
    
    Args:
        search_term (str): The term to search for
        name (str): The entity name
        aliases (str): Semicolon-separated string of aliases
        
    Returns:
        float: Highest similarity score found
    """
    # Normalize all text inputs
    search_term = normalize_text(search_term)
    name = normalize_text(name)
    
    # Calculate similarity with main name
    name_similarity = fuzz.ratio(search_term, name)
    
    # Calculate similarity with aliases
    alias_similarity = 0
    try:
        # Handle semicolon-separated aliases
        if pd.isna(aliases) or aliases == '':
            return name_similarity
            
        # Split aliases by semicolon and clean up
        aliases_list = [alias.strip() for alias in str(aliases).split(';') if alias.strip()]
        
        # Process each alias
        for alias in aliases_list:
            alias = normalize_text(alias)
            current_similarity = fuzz.ratio(search_term, alias)
            alias_similarity = max(alias_similarity, current_similarity)
            
    except Exception as e:
        logger.warning(f"Error processing aliases: {str(e)}")
        # If there's any error, just use the name similarity
    
    return max(name_similarity, alias_similarity)

def search_opensanctions(entity_name: str, csv_path: str, threshold: int = 90, max_matches: int = 3) -> List[Tuple[Dict, float]]:
    """
    Perform fuzzy search on sanctions data to find matching entities.
    Searches both the name and aliases fields for matches.
    
    Args:
        entity_name (str): The name of the entity to search for
        csv_path (str): Path to the consolidated sanctions CSV file
        threshold (int): Minimum similarity score (0-100) to consider a match
        max_matches (int): Maximum number of matches to return (default: 3)
        
    Returns:
        List[Tuple[Dict, float]]: List of tuples containing (entity_data, match_percentage)
        where entity_data includes all fields from the CSV:
        - enity_type, name, aliases
        - countries
        - addresses
        - sanctions
        - dataset
    """
    try:
        # Read the CSV file in chunks to handle large files
        chunk_size = 10000
        matches = []
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            # Convert entity names to string to handle any non-string values
            chunk['name'] = chunk['name'].astype(str)
            chunk['aliases'] = chunk['aliases'].fillna('')
            
            # Calculate similarity scores for each row
            for _, row in chunk.iterrows():
                similarity = get_highest_similarity(entity_name, row['name'], row['aliases'])
                
                if similarity >= threshold:
                    # Convert row to dict and organize data according to CSV structure
                    entity_data = {
                        'enity_type': row.get('schema'),
                        'name': row.get('name'),
                        'aliases': row.get('aliases'),
                        'countries': row.get('countries'),
                        'addresses': row.get('addresses'),
                        'sanctions': row.get('sanctions'),
                        'dataset': row.get('dataset'),
                    }
                    matches.append((entity_data, similarity))
        
        # Sort matches by similarity score in descending order and take top 3
        matches.sort(key=lambda x: x[1], reverse=True)
        matches = matches[:max_matches]
        
        return matches
    
    except Exception as e:
        logger.error(f"Error performing sanctions search: {str(e)}")
        raise

def forward(entity_name: str, matches: List[Tuple[Dict, float]]) -> Dict:
    """
    Format the search results into a standardized response dictionary.
    
    Args:
        entity_name (str): The original search query
        matches (List[Tuple[Dict, float]]): List of matches from search_opensanctions
        dataset_name (str): Name of the dataset being searched
        
    Returns:
        Dict: Formatted response with entity_name, entity_type, confidence, and evidence
    """
    if not matches:
        return None
        
    entity_data, similarity = matches[0]  # Get the top match
    return {
        "entity_name": entity_name,
        "entity_type": entity_data.get("enity_type", "Unknown"),
        "confidence": similarity,
        "evidence": f"sanctions: {entity_data.get('sanctions', 'None')}; dataset: {entity_data.get('dataset', 'None')}"
    }

