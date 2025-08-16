# data.py
import json
import os
from datetime import datetime

DATA_FILE = "transactions.json"

# Load existing transactions safely
transactions = []
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if content:
                transactions = json.loads(content)
    except json.JSONDecodeError:
        transactions = []


def save_data():
    """Save the transactions list to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4)


# ---- UI-linked save functions ----
def save_income_ui(amount, source, notes):
    """Save income transaction with date and source."""
    transactions.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": "income",
        "amount": float(amount),
        "source": source,
        "notes": notes
    })
    save_data()


def save_expense_ui(amount, category, notes):
    """Save expense transaction with date and category."""
    transactions.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": "expense",
        "amount": float(amount),
        "category": category,
        "notes": notes
    })
    save_data()


# ---- Delete / Clear functions ----
def delete_transaction(index):
    """Delete a single transaction by index."""
    if 0 <= index < len(transactions):
        transactions.pop(index)
        save_data()


def clear_all_transactions():
    """Delete all transactions."""
    transactions.clear()
    save_data()


# ---- Data access functions ----
def get_transactions():
    """Return all transactions."""
    return transactions


def get_summary():
    """Calculate total income, total expense, and balance."""
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense
    return f"Total Income: RM{total_income:.2f}\nTotal Expense: RM{total_expense:.2f}\nBalance: RM{balance:.2f}"


def get_expense_summary():
    """Returns breakdown of expenses by category."""
    summary = {}
    for t in transactions:
        if t["type"] == "expense":
            cat = t.get("category", "Other")
            summary[cat] = summary.get(cat, 0) + t["amount"]
    return summary
