import csv, os, re, json
from urllib.parse import urlparse

def get_count(text):
    """Extract package count from the text."""
    return [int(num) for num in re.findall(r'\d+', text)][0]

def transform_string(input_string):
    """Convert string to meet url format"""
    lowercase_string = input_string.lower()
    
    # Replace spaces and ampersands with dashes
    replaced_string = re.sub(r'[\s&]+', '-', lowercase_string)
    
    # Remove any remaining special characters except dashes
    cleaned_string = re.sub(r'[^\w-]', '', replaced_string)
    
    return cleaned_string


def load_categories_from_csv(csv_file):
    """Load visited categories from a CSV file."""
    categories = set()
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                categories.add(row[0])
    return categories


def save_category_to_csv(csv_file, list):
    """Save visited categories to a CSV file."""
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in list:
            writer.writerow([item])


def save_app_info_to_csv(csv_file, app_info):
    """Save app information to a CSV file."""
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'description', 'package_name', 'category', 'link', 'issue_tracker', 'source_code', 'metadata', 'download_url'])
        if not file_exists:
            writer.writeheader()
        # for app_info in app_infos:
        writer.writerow(app_info)

def save_app_info_to_json(json_file, app_info):
    """Save app information to a JSON file."""
    with open(json_file, 'w') as file:
        json.dump(app_info, file, indent=4)

def extract_package_name(url):
    """Extract the package name from the given URL."""
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path
        # Split the path and get the second last element
        package_name = path.split('/')[-2]
        return package_name
    except Exception as e:
        print(f"An error occurred while extracting the package name: {e}")
        return None
    
def get_property_from_csv(csv_file, column):
    """Retrieve the given column from the given CSV file."""
    properties = []
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                properties.append(row[column])
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    return properties