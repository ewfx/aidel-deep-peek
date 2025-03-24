import json
import csv
import pandas as pd

def flatten_json(json_data):
    flattened_data = []
    
    for item in json_data:
        # Extract basic fields
        
        # Extract person-specific fields
        properties = item.get('properties', {})
        name = ';'.join(properties.get('name', []))
        aliases = ';'.join(properties.get('alias', []))
        source = properties.get('source', '')
        first_name = ';'.join(properties.get('firstName', []))
        middle_name = ';'.join(properties.get('middleName', []))
        last_name = ';'.join(properties.get('lastName', []))
        id_number = ';'.join(properties.get('idNumber', []))
        country = ';'.join(properties.get('country', []))
        position = ';'.join(properties.get('position', []))
        address = ';'.join(properties.get('address', []))
        birth_date = ';'.join(properties.get('birthDate', []))
        title = ';'.join(properties.get('title', []))
        topics = ';'.join(properties.get('topics', []))
        
        # Extract sanctions metadata
        sanctions = []
        sanction_programs = []
        sanction_types = []
        sanction_start_dates = []
        sanction_end_dates = []
        sanction_reasons = []
        sanction_authorities = []
        sanction_identifiers = []
        sanction_statuses = []
        sanction_summaries = []
        sanction_provisions = []
        sanction_listing_dates = []
        sanction_source_urls = []
        
        if 'sanctions' in properties:
            for sanction in properties['sanctions']:
                sanction_info = []
                sanction_props = sanction.get('properties', {})
                
                # Collect individual sanction details
                if 'program' in sanction_props:
                    sanction_programs.append(';'.join(sanction_props['program']))
                    sanction_info.append(f"Program: {sanction_props['program'][0]}")
                if 'type' in sanction_props:
                    sanction_types.append(';'.join(sanction_props['type']))
                    sanction_info.append(f"Type: {sanction_props['type'][0]}")
                if 'startDate' in sanction_props:
                    sanction_start_dates.append(';'.join(sanction_props['startDate']))
                    sanction_info.append(f"Start: {sanction_props['startDate'][0]}")
                if 'endDate' in sanction_props:
                    sanction_end_dates.append(';'.join(sanction_props['endDate']))
                    sanction_info.append(f"End: {sanction_props['endDate'][0]}")
                if 'reason' in sanction_props:
                    sanction_reasons.append(';'.join(sanction_props['reason']))
                    sanction_info.append(f"Reason: {sanction_props['reason'][0]}")
                if 'authority' in sanction_props:
                    sanction_authorities.append(';'.join(sanction_props['authority']))
                    sanction_info.append(f"Authority: {sanction_props['authority'][0]}")
                if 'id' in sanction:
                    sanction_identifiers.append(sanction['id'])
                    sanction_info.append(f"ID: {sanction['id']}")
                if 'status' in sanction_props:
                    sanction_statuses.append(';'.join(sanction_props['status']))
                    sanction_info.append(f"Status: {sanction_props['status'][0]}")
                if 'summary' in sanction_props:
                    sanction_summaries.append(';'.join(sanction_props['summary']))
                    sanction_info.append(f"Summary: {sanction_props['summary'][0]}")
                if 'provisions' in sanction_props:
                    sanction_provisions.append(';'.join(sanction_props['provisions']))
                    sanction_info.append(f"Provisions: {sanction_props['provisions'][0]}")
                if 'listingDate' in sanction_props:
                    sanction_listing_dates.append(';'.join(sanction_props['listingDate']))
                    sanction_info.append(f"Listing Date: {sanction_props['listingDate'][0]}")
                if 'sourceUrl' in sanction_props:
                    sanction_source_urls.append(';'.join(sanction_props['sourceUrl']))
                    sanction_info.append(f"Source URL: {sanction_props['sourceUrl'][0]}")
                
                sanctions.append(' | '.join(sanction_info))
        
        # Create flattened record with all fields
        record = {
            'name': name,
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'id_number': id_number,
            'country': country,
            'position': position,
            'address': address,
            'birth_date': birth_date,
            'title': title,
            'topics': topics,
            'aliases': aliases,
            'source': source,
            'sanctions_full': ';'.join(sanctions),
            'sanction_programs': ';'.join(set(sanction_programs)),
            'sanction_types': ';'.join(set(sanction_types)),
            'sanction_start_dates': ';'.join(set(sanction_start_dates)),
            'sanction_end_dates': ';'.join(set(sanction_end_dates)),
            'sanction_reasons': ';'.join(set(sanction_reasons)),
            'sanction_authorities': ';'.join(set(sanction_authorities)),
            'sanction_identifiers': ';'.join(set(sanction_identifiers)),
            'sanction_statuses': ';'.join(set(sanction_statuses)),
            'sanction_summaries': ';'.join(set(sanction_summaries)),
            'sanction_provisions': ';'.join(set(sanction_provisions)),
            'sanction_listing_dates': ';'.join(set(sanction_listing_dates)),
            'sanction_source_urls': ';'.join(set(sanction_source_urls))
        }
        
        flattened_data.append(record)
    
    return flattened_data

def main():
    # Read the JSON file
    json_data = []
    failed_lines = []
    total_lines = 0
    
    with open('E:/Downloads/targets.nested.consolidated.json', 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            total_lines += 1
            try:
                json_obj = json.loads(line.strip())
                json_data.append(json_obj)
            except json.JSONDecodeError as e:
                failed_lines.append((line_num, str(e)))
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    if not json_data:
        print("No valid JSON data found in the file")
        return
    
    # Flatten the data
    flattened_data = flatten_json(json_data)
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(flattened_data)
    
    # Save to CSV
    df.to_csv('code/src/consolidated_sanctions_data.csv', index=False, encoding='utf-8')
    
    # Print summary
    print("\nProcessing Summary:")
    print(f"Total lines in file: {total_lines}")
    print(f"Successfully processed: {len(flattened_data)} records")
    print(f"Failed to process: {len(failed_lines)} records")
    
    if failed_lines:
        print("\nFailed lines details:")
        for line_num, error in failed_lines:
            print(f"Line {line_num}: {error}")

if __name__ == "__main__":
    main() 