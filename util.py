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
    with open(file_path, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if file_is_new:
            writer.writeheader()

        writer.writerow(transaction.to_dict())
