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
        lines += [f"{key}: {value}" for key, value in transaction.items()]
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
            total = get_total_amount(all_transactions)
            all_transactions = format_transactions(all_transactions)
            all_transactions.append(
                f"Total amount: {total}\n----------------------------\n"
            )
            return (
                all_transactions
                if all_transactions
                else ["No transactions were found.\n"]
            )

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found. Make sure it exists.")


def get_total_amount(transactions):
    """
    Returns the total amount of a list of transactions.
    """
    total = 0
    for transaction in transactions:
        total += float(transaction["amount"])
    return total


def filter_transactions_by_type(txn_type, file_path="./data/transactions.csv"):
    """
    Filters the transactions by a given type.

    Returns a list of transactions with the given type.
    Raises FileNotFound error if the file doesn't exist.
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            filtered_transactions = [
                row for row in reader if row["type"] == txn_type.lower()
            ]

            total = get_total_amount(filtered_transactions)
            filtered_transactions = format_transactions(filtered_transactions)
            filtered_transactions.append(
                f"Total {txn_type}: {total}\n----------------------------\n"
            )

            return (
                filtered_transactions
                if filtered_transactions
                else [f"No {txn_type} transactions were found.\n"]
            )

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found. Make sure it exists.")


def view_monthly_summary(file_path="./data/transactions.csv"):
    """
    Displays a monthly summary showing total income, expenses, and net savings for each month.

    Groups transactions by month using the date field and prints summaries to the terminal.
    """

    with open(file_path, "r") as file:
        jan = []
        feb = []
        mar = []
        apr = []
        may = []
        jun = []
        jul = []
        aug = []
        sep = []
        oct = []
        nov = []
        dec = []
        months = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
        month_names = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

        # Filtering transactions into lists based on months
        reader = csv.DictReader(file)
        for row in reader:
            month_index = int(row["date"][5:7]) - 1
            months[month_index].append(row)

        for i, month in enumerate(months):
            if month:
                expenses = [row for row in month if row["type"] == "expense"]
                income = [row for row in month if row["type"] == "income"]
                total_expense_amount = get_total_amount(expenses)
                total_income_amount = get_total_amount(income)
                print(
                    f"""===== Monthly Summary ({month_names[i]} 2025) =====

Total Income:      {total_income_amount} EGP
Total Expenses:    {total_expense_amount} EGP
-------------------------------
Net Savings:       {total_income_amount - total_expense_amount}"""
                )

    return


def filter_by_category(category, transactions):
        """"
        Filters a list of transactions by a given category.

        Returns a list of filtered transactions.
        """
        categorized_transactions = [transaction for transaction in transactions if transaction["category"] == category]
        return categorized_transactions
