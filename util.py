import csv
import os

"""
util.py

Helper functions for the expense tracker, including saving transactions to CSV.
"""


def save_transaction(transaction, file_path="./data/transactions.csv"):
    """
    Save a transaction to a CSV file.

    Creates the files and writes headers if it's new or empty.
    """

    file_is_new = not os.path.exists(file_path) or os.path.getsize(file_path) == 0

    fields = ["type", "amount", "category", "description", "date", "time"]
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if file_is_new:
            writer.writeheader()

        writer.writerow(transaction.to_dict())


def format_transactions(all_transactions):
    """
    Formats transactions into strings.

    Returns a list of formatted transactions to be printed.
    """
    formatted_transactions = ["\n----------------------------\n"]
    for index, transaction in enumerate(all_transactions):
        if not transaction:
            continue
        lines = [f"Transaction {index + 1}: \n"]
        lines += [f"{key}: {value}" for key,value in transaction.items()]
        lines.append("----------------------------\n")
        formatted_transactions.append("\n".join(lines))
    return formatted_transactions


def view_transactions(file_path="./data/transactions.csv"):
    """
    Read all the transactions from the csv file.

    Returns all transactions as a list of formatted strings.
    Raises FileNotFoundError if the file doesn't exist.
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            all_transactions = []
            for transaction in reader:
                all_transactions.append(transaction)
            return format_transactions(all_transactions)

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found. Make sure it exists.")