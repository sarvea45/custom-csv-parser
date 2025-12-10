import csv
import os

FILE_NAME = "test_data.csv"
ROW_COUNT = 10000

def generate_test_data(row_count=ROW_COUNT):
    """Generates a large CSV file (10k+ rows) with edge cases for benchmarking."""
    if os.path.exists(FILE_NAME):
        print(f"✅ Skipping generation: {FILE_NAME} already exists.")
        return

    data = []
    # Headers
    data.append(["ID", "Name", "Quoted_Field", "Comma_Field", "Newline_Field"])

    for i in range(1, row_count + 1):
        # Data includes mandatory edge cases for quoting/escaping
        name = f"User_{i}"
        # A field containing an internal quote, forcing escaping ( "" -> " )
        quoted_field = f'A value with an internal "quote" (will be written as """").'
        # A field with commas, forcing external quotes
        comma_field = f"Data, with, commas, in row {i}"
        # A field with a newline, forcing external quotes
        newline_field = f"Line 1 for {i}\nLine 2"
        data.append([i, name, quoted_field, comma_field, newline_field])

    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print(f"✅ Generated {row_count} rows in {FILE_NAME} for benchmarking.")

if __name__ == "__main__":
    generate_test_data()