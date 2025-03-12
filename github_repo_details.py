"""
python3 github_repo_details.py
"""

import requests
import csv
import time
import os
from datetime import datetime

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com/repos/"

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Input and output CSV files
INPUT_CSV = "github_search_results.csv"  # CSV containing repo names in "owner/repo" format
OUTPUT_CSV = "github_repo_details.csv"

# Filter criteria
MIN_STARS = 50
MIN_COMMIT_DATE = datetime.strptime("2024-01-01", "%Y-%m-%d")

# Headers for authentication (if using a token)
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# Function to check if the output file exists and initialize it if needed
def initialize_output_file():
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Repository", "Created At", "Stars", "Forks", "Last Commit Date", "HTML URL", "Description", "Meets Criteria"])  # Header row

# Function to load already fetched repositories
def load_fetched_repos():
    fetched_repos = set()
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if row:  # Ensure row is not empty
                    fetched_repos.add(row[0])  # First column is the repo name
    return fetched_repos

# Function to get repository details
def fetch_repo_details(repo_full_name):
    url = f"{GITHUB_API_URL}{repo_full_name}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 403:  # Rate limit exceeded
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait_time = reset_time - int(time.time()) + 1
            print(f"⚠️ Rate limit exceeded. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            return fetch_repo_details(repo_full_name)  # Retry request
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch {repo_full_name}: {response.status_code}")
            return None
        
        data = response.json()
        
        # Check if repo is a fork - skip if it is
        if data.get("fork", False):
            print(f"⏩ Skipping {repo_full_name} - it's a fork.")
            return None
        
        # Check star count - skip if below minimum
        star_count = data.get("stargazers_count", 0)
        if star_count < MIN_STARS:
            print(f"⏩ Skipping {repo_full_name} - only has {star_count} stars (minimum: {MIN_STARS}).")
            return None
        
        # Get the most recent commit date
        commits_url = data["commits_url"].replace("{/sha}", "")
        commit_response = requests.get(commits_url, headers=HEADERS, params={"per_page": 1})
        
        if commit_response.status_code != 200:
            print(f"⚠️ Couldn't fetch commits for {repo_full_name}: {commit_response.status_code}")
            latest_commit_date = "N/A"
            meets_criteria = "No (Commit date unknown)"
        else:
            try:
                latest_commit_date = commit_response.json()[0]["commit"]["committer"]["date"]
                # Check if the last commit is recent enough
                last_commit_datetime = datetime.strptime(latest_commit_date.split("T")[0], "%Y-%m-%d")
                
                if last_commit_datetime < MIN_COMMIT_DATE:
                    print(f"⏩ Skipping {repo_full_name} - last commit ({latest_commit_date}) before {MIN_COMMIT_DATE.strftime('%Y-%m-%d')}.")
                    return None
                
                meets_criteria = "Yes"
            except (IndexError, KeyError, ValueError) as e:
                print(f"⚠️ Error parsing commit date for {repo_full_name}: {str(e)}")
                latest_commit_date = "N/A"
                meets_criteria = "No (Date parsing error)"
        
        # Prepare the detailed information for the repository
        return [
            repo_full_name,
            data.get("created_at"),
            star_count,
            data.get("forks_count"),
            latest_commit_date,
            data.get("html_url"),
            data.get("description"),
            meets_criteria
        ]
    
    except Exception as e:
        print(f"⚠️ Error fetching {repo_full_name}: {str(e)}")
        return None

# Main execution
def main():
    print(f"🚀 Starting GitHub repo analysis with filters:")
    print(f"   - Not a fork")
    print(f"   - Last commit after {MIN_COMMIT_DATE.strftime('%Y-%m-%d')}")
    print(f"   - At least {MIN_STARS} stars")
    
    # Ensure output file is ready
    initialize_output_file()
    
    # Load already fetched repositories
    fetched_repos = load_fetched_repos()
    
    try:
        # Read repository names from input CSV with known header format:
        # repository,path,name,url,html_url,git_url,score
        with open(INPUT_CSV, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            repo_list = []
            for row in reader:
                # Get the repository name from the 'repository' column
                repo_name = row.get('repository', '').strip()
                if repo_name and '/' in repo_name:
                    repo_list.append(repo_name)
    except Exception as e:
        print(f"❌ Error reading input CSV: {str(e)}")
        return
    
    if not repo_list:
        print("⚠️ No repositories found in the input CSV.")
        return
    
    print(f"📊 Found {len(repo_list)} repositories to process.")
    
    # Track metrics
    total_processed = 0
    total_matching = 0
    
    # Process repositories
    for repo in repo_list:
        if repo in fetched_repos:
            print(f"⏩ Skipping {repo}, already fetched.")
            continue
        
        print(f"🔍 Fetching details for {repo}...")
        details = fetch_repo_details(repo)
        total_processed += 1
        
        if details:
            # Append data immediately
            with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(details)
            
            if details[-1] == "Yes":
                total_matching += 1
                print(f"✅ Saved {repo} to {OUTPUT_CSV} - Meets all criteria!")
            else:
                print(f"⚠️ Saved {repo} to {OUTPUT_CSV} - Does not meet all criteria.")
        
        # Sleep to avoid hitting rate limits
        time.sleep(15)
    
    print(f"🎯 Script completed.")
    print(f"   - Data saved in {OUTPUT_CSV}")

if __name__ == "__main__":
    main()