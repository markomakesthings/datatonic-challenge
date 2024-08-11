import requests
import csv

def fetch_data(base_url, params):
    """
    Fetch data from the Open Library API
    
    Args:
    base_url (str): The base URL of the API
    params (dict): The query parameters for the API request
    
    Returns:
    dict or None: The JSON response if successful, None otherwise
    """
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

def write_to_csv(csv_file, base_url, params, limit):
    """
    Writes works data to a CSV file

    Args:
    csv_file (str): The path to the CSV file
    base_url (str): The base URL of the API
    params (dict): The query parameters for the API request
    limit (int): The limit of items per page
    """
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Author(s)", "Publish Year", "Subjects"])

            while True:
                print(f"Fetching data with offset: {params['offset']}")
                data = fetch_data(base_url, params)

                if not data:
                    print(f"Failed to fetch data")
                    continue

                for work in data['works']:
                    # Using .get() to avoid KeyErrors
                    title = work.get('title', '')
                    authors = ', '.join([author.get('name', '') for author in work.get('authors', [])])
                    first_publish_year = work.get('first_publish_year', '')
                    subjects = ', '.join(work.get('subject', []))
                    writer.writerow([title, authors, first_publish_year, subjects])

                total_works = data.get('work_count', 0)
                if params['offset'] + limit >= total_works:
                    break  # Exit loop if we've fetched all works

                params['offset'] += limit  # Increase offset for next batch

        print(f"Data has been written to {csv_file}")

    except IOError as e:
        print(f"Error opening or writing to file {csv_file}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error while writing to CSV: {str(e)}")

def main():
    """
    Main function for data fetching and CSV writing
    """
    base_url = "https://openlibrary.org/subjects/artificial_intelligence.json"
    offset = 0
    limit = 100 # Number of items to fetch per request
    params = {'limit': limit, 'offset': offset}

    csv_file = "part2/part2_dataset.csv"

    write_to_csv(csv_file, base_url, params, limit)

if __name__ == "__main__":
    main()