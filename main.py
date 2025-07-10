from transaction import Transaction
import util

"""
main.py

Command-line interface for the expense tracker.
Handles user input, transaction creation, and menu navigation.
"""


while True:
    print(
        f"""Welcome to Expense Tracker!

----------------------------------
          
1. Add a transaction
2. View all transactions
3. View income
4. View expenses
5. Show monthly summary
6. Filter by category
7. Exit
"""
    )
    # Validate menu choice and handle non-integer or out-of-range input
    try:
        choice = int(input("Process: "))
        if choice not in range(1, 8):
            raise ValueError
    except ValueError:
        print("\nInvalid input, please try again.\n")
        continue

    match choice:
        # Create a Transaction object from user input
        case 1:
            type = input("Transaction type: ").strip()
            amount = input("Amount: ").strip()
            category = input("Category: ").strip()
            description = input("Description: ").strip()
            date = input("Date: ").strip()
            time = input("Time: ").strip()

            # Handle validation errors from amount, date, or time
            try:
                transaction = Transaction(
                    type, amount, category, description, date, time
                )
            except (TypeError, ValueError) as e:
                print(f"Error: {e}")
                continue
            # Save the created transaction to the csv file
            try:
                util.save_transaction(transaction)
                print("Transaction saved successfully!")
            except Exception:
                print("An error occured while saving.")
        case 2:
            try:
                # Get all the transactions using view_transaction function
                transactions = util.view_transactions()
                for transaction in transactions:
                    print(transaction)
            except FileNotFoundError as e:
                print(f"Error: {e}")

        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            print("Thank you! Bye bye!")
            break
        case _:
            print("\n\nInvalid input, please try again.\n\n")
            continue
