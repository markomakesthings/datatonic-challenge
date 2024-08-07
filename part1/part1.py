import requests
import csv
import re

def get_publish_year(book):
    if 'first_publish_year' in book:
        return book['first_publish_year']
    elif 'publish_date' in book:
        years = []
        for date in book['publish_date']:
            match = re.search(r'\b(\d{4})\b', date)  # Find four-digit numbers (years)
            if match:
                years.append(int(match.group(1)))
        if years:
            return min(years)  # Return the earliest year
    return 'N/A'

def has_desired_format(book):
    desired_keywords = ["paperback", "paper", "softcover", "hardcover", "binding", "bind", "bound"]
    if 'format' in book:
        for format_item in book['format']:
            if any(keyword in format_item.lower() for keyword in desired_keywords):
                return True
    return False

def fetch_docs(base_url, params):
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

# API URL
base_url = 'https://openlibrary.org/search.json'
query = 'lord of the rings'
params = {'q': query, 'page': 1}

# Initial GET request to the API for starting info
data = fetch_docs(base_url, params)

# Calculate the total number of pages of the response to go through
num_found = data['numFound']
total_pages = (num_found // 100) + 1

# Define the CSV file name
csv_file = "part1/part1_dataset.csv"

# Open the CSV file for writing
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["Title", "Author", "Publish Year", "Publisher", "Language"])
    
    # Iterate through each page of results
    for page in range(1, total_pages + 1):
        # Update the page parameter
        params['page'] = page
        
        # Fetch the current page data from the API
        data = fetch_docs(base_url, params)
        if not data:
            print(f"Failed to fetch data for page {page}")
            continue
        
        # Iterate through the list of books and write the relevant data to the CSV file
        for book in data.get('docs', []):
            # Using .get() to avoid KeyErrors
            title = book.get('title', '')
            author_name = ', '.join(book.get('author_name', []))
            publisher = ', '.join(book.get('publisher', ['N/A']))
            language = ', '.join(book.get('language', ['N/A']))
            publish_year = get_publish_year(book)
            
            # Include only books with "lord of the rings" in the title and an author
            # and ensure the book has the desired format (paperback, hardcover, etc.)
            if "lord of the rings" in title.lower() and author_name and has_desired_format(book):
                writer.writerow([title, author_name, publish_year, publisher, language])

print(f"Data has been written to {csv_file}")