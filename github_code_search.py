"""
python3 github_code_search.py
"""

import os
import requests
import csv
import json
import time
from datetime import datetime

def github_code_search():
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

    # API URL and parameters
    base_url = "https://api.github.com/search/code"
    query = "com.google.android.gms.car.application+android.media.browse.MediaBrowserService+filename:AndroidManifest.xml"
    
    # Headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "VSCode-RestClient",
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    
    # Generate timestamp for filename
    csv_filename = "github_search_results.csv"
    
    # Pagination variables
    per_page = 100  # Maximum allowed by GitHub API
    page = 1
    all_items = []
    has_more_pages = True
    total_count = 0
    
    # Fetch all pages until we have all results or hit GitHub API limits
    while has_more_pages:
        try:
            print(f"Fetching page {page}...")
            response = requests.get(
                f"{base_url}?q={query}&per_page={per_page}&page={page}", 
                headers=headers
            )
            response.raise_for_status()
            
            # Parse JSON response
            page_data = response.json()
            items = page_data.get('items', [])
            
            # Get total count from first page
            if page == 1:
                total_count = page_data.get('total_count', 0)
                
            # Add current page items to our collection
            all_items.extend(items)
            
            # Check if we've reached the last page
            if len(items) < per_page:
                has_more_pages = False
                print(f"Reached the last page with {len(items)} items.")
            else:
                page += 1
                
            # GitHub API has rate limits, so we should be nice and add a delay
            if has_more_pages:
                print("Waiting before next request...")
                time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            break
    
    # Write results to CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Define CSV columns
        fieldnames = ['repository', 'path', 'name', 'url', 'html_url', 'git_url', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for item in all_items:
            writer.writerow({
                'repository': item.get('repository', {}).get('full_name', ''),
                'path': item.get('path', ''),
                'name': item.get('name', ''),
                'url': item.get('url', ''),
                'html_url': item.get('html_url', ''),
                'git_url': item.get('git_url', ''),
                'score': item.get('score', '')
            })
    
    print(f"Total results retrieved: {len(all_items)}")
    print(f"Saved {len(all_items)} items to {csv_filename}")
    
    # Return data for potential further processing
    return {"total_count": total_count, "items": all_items}

if __name__ == "__main__":
    print("Starting GitHub code search...")
    github_code_search()
