import pandas as pd
from collections import Counter

# Load the CSV data
file_path = 'part2_dataset.csv'
data = pd.read_csv(file_path)

# Define a function to count subjects
def count_subjects(subject_column):
    subject_counts = Counter()
    for subjects in subject_column:
        for subject in subjects.split(','):
            cleaned_subject = subject.strip().lower()
            if cleaned_subject != "artificial intelligence":
                subject_counts[cleaned_subject] += 1
    return subject_counts

# Count subjects in the 'Subjects' column
subject_counts = count_subjects(data['Subjects'])

# Convert the counts to a DataFrame and sort by the counts
subject_counts_df = pd.DataFrame(subject_counts.items(), columns=['Subject', 'Count']).sort_values(by='Count', ascending=False)

# Save the result to a new CSV file
output_file_path = 'subject_counts.csv'
subject_counts_df.to_csv(output_file_path, index=False)

print(subject_counts_df)