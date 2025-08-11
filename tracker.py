
import csv
import os
from datetime import datetime

CSV_FILE = "expenses.csv"

def load_expenses():
    """Load expenses from the CSV file."""
    if not os.path.exists(CSV_FILE):
        return []
    
    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        return list(reader)

def save_expenses(expenses):
    """Save expenses to the CSV file."""
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(expenses)

def add_expense(amount, description, date):
    """Add a new expense to the CSV file."""
    if not date:
        date = datetime.today().strftime("%d-%m-%Y")
    
    expenses = load_expenses()
    expenses.append([amount, description, date])
    save_expenses(expenses)

# def delete_last_expense():
#     """Delete the last expense entry."""
#     expenses = load_expenses()
#     if expenses:
#         expenses.pop()
#         save_expenses(expenses)
def delete_selected_expense(selected_item):
    """Delete the exact selected expense row from the CSV file."""
    expenses = load_expenses()
    
    # selected_item is a list like ['100', 'Snacks', '29-06-2025']
    
    if selected_item in expenses:
        expenses.remove(selected_item)
        save_expenses(expenses)
        print(f"✅ Deleted: {selected_item}")
        return True
    else:
        print("❌ Selected item not found in expenses.")
        return False


def get_expenses():
    """Return all expenses."""
    return load_expenses()
def modify(selected_item):
    expenses = load_expenses()
    if selected_item in expenses:
        expenses.remove(selected_item)
    save_expenses(expenses)
    