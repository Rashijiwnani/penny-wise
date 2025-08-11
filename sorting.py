import csv
from datetime import datetime

input_file = "expenses.csv"
output_file = "expenses_sorted.csv"  # You can overwrite input_file if you want

def read_and_sort_csv_by_date(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Optional: Skip empty rows or malformed rows
    rows = [row for row in rows if len(row) == 3]

    # Sort rows by the 3rd column (date)
    sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row[2], "%d-%m-%Y"))

    return sorted_rows

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    sorted_expenses = read_and_sort_csv_by_date(input_file)
    write_csv(output_file, sorted_expenses)
    print(f"Expenses sorted by date and written to: {output_file}")
