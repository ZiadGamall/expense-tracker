from datetime import datetime, date, time
from difflib import get_close_matches

"""
transaction.py

Defines the Transaction class used in the expense tracker.
Each transaction includes type, amount, category, description, date, and time, with validation logic to ensure proper formats.
"""


class Transaction:
    """
    Represents a single financial transaction.

    Attributes:
        type (str): Either 'income' or 'expense'.
        amount (float): Must be a non-negative number.
        category (str): The transaction category (e.g., 'food', 'rent').
        description (str): Optional additional details.
        date (datetime.date): Date of the transaction. Defaults to today.
        time (datetime.time): Time of the transaction. Defaults to current time (HH:MM).
    """

    def __init__(self, type, amount, category, description="", dt=None, time=None):
        self.type = type
        self.amount = amount
        self.category = category
        self.description = description
        self.date = dt if dt else date.today()
        self.time = (
            time if time else datetime.now().replace(second=0, microsecond=0).time()
        )
        # Display formatted confirmation with full date and 24-hour time
        print(
            f"A {self.type} transaction was created on {self.date.strftime('%B %d, %Y')} at {self.time.strftime('%I:%M %p')}"
        )

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        """
        Validate the provided type.
        Accepts only 'income' or 'expense', while accounting for typos.
        Raises a ValueError otherwise.
        """
        valid_input = ["income", "expense"]
        if match := get_close_matches(value, valid_input, n=1, cutoff=0.6):
            self._type = match[0]
        else:
            raise ValueError(
                "Incorrect transaction type. Accepted types are 'income' and 'expense'"
            )

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        """
        Parse and validate the provided date.
        Accepts a string (YYYY-MM-DD), datetime, or date object.
        """

        if isinstance(value, str):
            # Parse and validate the date if provided as a string
            try:
                self._date = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format, please use YYYY-MM-DD")

        elif isinstance(value, datetime):
            # Extract date if provided as a datetime object
            self._date = value.date()
        elif isinstance(value, date):
            # Use directly if already a date object
            self._date = value
        else:
            raise TypeError(
                "Date must be a string in YYYY-MM-DD format, or a date/datetime object"
            )

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        """
        Parse and validate the provided time.
        Accepts a string (HH:MM), datetime, or time object.
        Strips seconds and microseconds.
        """

        if isinstance(value, str):
            # Parse and validate the time if provided as a string
            try:
                parsed_time = datetime.strptime(value, "%H:%M").time()
            except ValueError:
                raise ValueError(
                    "Invalid time format. Please use HH:MM (24-hour format)."
                )
        elif isinstance(value, datetime):
            # Extract and format time if provided as a datetime object
            parsed_time = value.time().replace(second=0, microsecond=0)

        elif isinstance(value, time):
            # Extract and format time if provided as a time object
            parsed_time = value.replace(second=0, microsecond=0)
        else:
            raise TypeError(
                "Time must be a string in HH:MM format or a time/datetime object."
            )

        self._time = parsed_time

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        """
        Validate that the amount is a non-negative number and convert it to float.
        """
        try:
            if float(value) < 0:
                raise ValueError("The amount cannot be a negative number.")
            self._amount = float(value)
        except ValueError:
            raise ValueError("Invalid amount format. Must be a number.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        """
        Validate the provided category.
        Accepts only written categories, while accounting for typos.
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
        if self.type == "expense":
            if matched := get_close_matches(value, categories, n=1, cutoff=0.6):
                self._category = matched[0]
            else:
                # If no match fallback to 'other'
                self._category = "other"
        else:
            self._category = value.strip().lower()

    def to_dict(self):
        """
        Convert the transaction to a dictionary for CSV storage.
        """
        return {
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.strftime("%Y-%m-%d"),
            "time": self.time.strftime("%H:%M"),
        }
