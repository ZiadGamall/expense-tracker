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
        all_transactions = get_transactions(file_path)
        total = get_total_amount(all_transactions)
        all_transactions = format_transactions(all_transactions)
        all_transactions.append(
            f"Total amount: {total}\n----------------------------\n"
        )
        return (
            all_transactions if all_transactions else ["No transactions were found.\n"]
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
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist.")

    if os.path.getsize(file_path) == 0:
        return "No data available.\n"
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
    monthly_summary = []
    # Filtering transactions into lists based on months
    transactions = get_transactions(file_path)

    for row in transactions:
        month_index = int(row["date"][5:7]) - 1
        months[month_index].append(row)

    for i, month in enumerate(months):
        if month:
            expenses = [row for row in month if row["type"] == "expense"]
            income = [row for row in month if row["type"] == "income"]
            total_expense_amount = get_total_amount(expenses)
            total_income_amount = get_total_amount(income)

            monthly_summary.append(
                f"""===== Monthly Summary ({month_names[i]} 2025) =====

Total Income:      {total_income_amount} EGP
Total Expenses:    {total_expense_amount} EGP
-------------------------------
Net Savings:       {total_income_amount - total_expense_amount}

{format_expenses(expenses)}

Transactions this month: {len(month)}

======================================="""
            )
    return "\n".join(monthly_summary)


def format_expenses(expenses):
    """
    Format expense transactions into a summary string.

    Calculates total spending, highlights the top expense category, and
    provides a breakdown of all non-zero categories.

    Returns a formatted string to be printed in the monthly summary.
    """
    formatted_text = []
    categories = [
        "food",
        "utilities",
        "transport",
        "shopping",
        "entertainment",
        "rent",
        "health",
        "education",
        "subscriptions",
        "other",
    ]

    # Store the categories with their total amount in a dict
    category_totals = {cat: 0 for cat in categories}
    for txn in expenses:
        # Increase the amount for each category by the amount in each matching expense
        category_totals[txn["category"]] += float(txn["amount"])
    total_expenses = get_total_amount(expenses)

    if total_expenses == 0:
        return "No expenses this month."

    # Get the top expense and value
    top_expense = max(category_totals, key=category_totals.get)
    top_value = category_totals[top_expense]

    formatted_text.append(f"Top Expense Category: {top_expense.title()}")
    formatted_text.append(
        f"  → Total: {top_value} EGP ({(top_value/total_expenses * 100):.1f}% of expenses)\n"
    )
    formatted_text.append("Category breakdown:")

    # Display the categories that are not zero valued as "-Cateogry:     value EGP"
    for key, value in category_totals.items():
        if value:
            formatted_text.append(f"- {key.title():<15} {value:>8.2f} EGP")

    return "\n".join(formatted_text)


def get_transactions(file_path="./data/transactions.csv"):
    """
    Return a list of transactions from the transactions file.

    Raises a FileNotFoundError if the file is not found.
    """
    transactions = []
    try:
        with open(file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)
            return transactions
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found. Make sure it exists.")


def filter_by_category(category, transactions):
    """
    Filters a list of transactions by a given category.

    Returns a list of filtered transactions.
    """
    categories = [
        "food",
        "utilities",
        "transport",
        "shopping",
        "entertainment",
        "rent",
        "health",
        "education",
        "subscriptions",
        "other",
    ]

    if category not in categories:
        raise ValueError(f"Invalid category. Choose from: {', '.join(categories)}.")
    categorized_transactions = [
        transaction
        for transaction in transactions
        if transaction["category"].lower() == category.lower()
    ]
    return categorized_transactions
