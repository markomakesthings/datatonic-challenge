import requests
import csv

def fetch_data(offset):
    url = f"https://openlibrary.org/subjects/artificial_intelligence.json?limit=100&offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def write_to_csv(data, writer):
    for work in data['works']:
        title = work.get('title', '')
        authors = ', '.join([author['name'] for author in work.get('authors', [])])
        first_publish_year = work.get('first_publish_year', '')
        subjects = ', '.join(work.get('subject', []))
        writer.writerow([title, authors, first_publish_year, subjects])

def main():
    offset = 0
    limit = 100
    csv_file = "part2/part2_dataset.csv"

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author(s)", "First Publish Year", "Subjects"])

        while True:
            print(f"Fetching data with offset: {offset}")
            data = fetch_data(offset)
            
            if data is None:
                break

            write_to_csv(data, writer)

            total_works = data['work_count']
            if offset + limit >= total_works:
                break

            offset += limit

    print(f"Data has been written to {csv_file}")

if __name__ == "__main__":
    main()