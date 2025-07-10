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

            for index, row in enumerate(reader):
                transaction = f"Transaction {index + 1}: \n\n"
                # Adding properties to the string
                for prop in row:
                    transaction += f"{prop.title()}: {row[prop].strip()}\n"
                transaction += "----------------------------\n"
                all_transactions.append(transaction)
            
            return all_transactions

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found. Make sure it exists.")
