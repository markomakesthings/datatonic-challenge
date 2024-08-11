import requests
import csv
import re

def get_publish_year(book):
    """
    Extracts the earliest publish year from a book record

    Args:
    book (dict): The book record

    Returns:
    int or str: The earliest publish year or 'N/A' if not available
    """
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
    """
    Checks if a book has a desired format

    Args:
    book (dict): The book record

    Returns:
    bool: True if the book has a desired format, False otherwise
    """
    # List of keywords associated with book formats
    desired_keywords = ["paperback", "paper", "softcover", "hardcover", "binding", "bind", "bound", "book"]
    if 'format' in book:
        for format_item in book['format']:
            if any(keyword in format_item.lower() for keyword in desired_keywords):
                return True
    return False

def fetch_data(base_url, params):
    """
    Fetches data from an API

    Args:
    base_url (str): The base URL of the API
    params (dict): The query parameters for the API request

    Returns:
    dict: The response data or an empty dictionary if an error occurred
    """
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

def write_to_csv(csv_file, base_url, params, num_found):
    """
    Writes book data to a CSV file

    Args:
    csv_file (str): The path to the CSV file
    base_url (str): The base URL of the API
    params (dict): The query parameters for the API request
    num_found (int): The total number of books found
    """
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Author(s)", "Publish Year", "Publisher(s)", "Language"])

            total_pages = (num_found // 100) + 1

            for page in range(1, total_pages + 1):
                params['page'] = page
                data = fetch_data(base_url, params)

                if not data:
                    print(f"Failed to fetch data for page {page}")
                    continue

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

    except IOError as e:
        print(f"Error opening or writing to file {csv_file}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error while writing to CSV: {str(e)}")

def main():
    """
    Main function for data fetching and CSV writing
    """
    base_url = 'https://openlibrary.org/search.json'
    query = 'lord of the rings'
    params = {'q': query, 'page': 1}

    # Fetch initial data to calculate the total number of pages to go through in the response
    data = fetch_data(base_url, params)
    if not data:
        print("Failed to fetch initial data")
        return

    num_found = data.get('numFound', 0)
    csv_file = "part1/part1_dataset.csv"

    write_to_csv(csv_file, base_url, params, num_found)

if __name__ == "__main__":
    main()