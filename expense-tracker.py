# Add expense categories and allow users to filter expenses by category.
# Allow users to set a budget for each month and show a warning when the user exceeds the budget.
# Allow users to export expenses to a CSV file.
import argparse
import json
import os
from datetime import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))
database_folder = "database"

if not os.path.exists(database_folder):
    os.makedirs(database_folder)

database_path = os.path.join(current_directory, database_folder)
file_name = "database.json"
file_path = os.path.join(database_path, file_name)

default_arguments: dict = {
    0: {
        'id': 0,
        'description': "No Expense Found With ID: ",
        'category': "No Category",
        'amount': 0,
        'created': datetime.now().strftime("%Y-%m-%D")
    }
}
months = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: "June",
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
}


def collect_arguments() -> dict:
    my_parser = argparse.ArgumentParser("Expense Tracker")
    my_parser.add_argument("operation", choices=["add", "list", "summary", 'delete'])
    my_parser.add_argument('-description', "--description", help="Description of the Expense")
    my_parser.add_argument('-amount', '--amount', help='Amount Spent in dollars')
    my_parser.add_argument('-id', '--id', help="Enter the id of the expense")
    my_parser.add_argument('-category', '--category', help="Enter the category of the")
    my_parser.add_argument('-month', '--month', help="Enter the month of the  current year of the expense")
    args = my_parser.parse_args()
    return args.__dict__


def initialise_database() -> bool:
    try:
        with open(file_path, "r") as file:
            json.load(file)
            return True
    except FileNotFoundError:
        with open(file_path, "w") as file:
            json.dump(default_arguments, file, indent=4)
            return True


def load_expenses() -> dict:
    with open(file_path, "r") as file:
        return json.load(file)


class UserOperationHandler:
    def __init__(self):
        parser = self.__parser_kwargs()
        try:
            self.operation = parser['operation']
            self.description = parser['description']
            self.amount = parser['amount']
            self.month = parser['month']
            self.category = parser['category']
            self.id = parser['id']
            self.__handle_operation()
        except KeyError:
            raise KeyError("Missing Key")

    @staticmethod
    def __parser_kwargs():
        parser = collect_arguments()
        return parser

    def __handle_operation(self):

        if self.operation == 'list':
            return self.__list_expense()

        if self.operation == 'delete':
            return self.__delete_expense()

        if self.operation == 'summary':

            if self.month:
                return self.__print_summary(month=self.month)

            return self.__print_summary()

        if self.operation == 'add':
            return self.__add_expense()

    @staticmethod
    def __list_expense():
        expenses = load_expenses()
        print("ID\tDate\t\tDescription\tAmount") if len(expenses) > 1 else print("No Expenses")
        for expense in expenses.values():
            if expense['id'] != 0:
                print(f"{expense['id']}\t{expense['created']}\t{expense['description']}\t\t$ {expense['amount']}")
        return

    def __add_expense(self):
        new_expense = {
            "description": self.description,
            "amount": self.amount,
            "category": self.category if self.category else default_arguments[0]['category']
        }
        new_key = self.save_expenses(new_expense)
        print(f"Expense added successfully (ID: {new_key})")

    def __print_summary(self, month=None):
        expenses = load_expenses()
        if expenses:
            amount = [int(expense['amount']) for expense in expenses.values()]
            if month:
                amount = [int(expense['amount']) for expense in expenses.values() if
                          datetime.fromisoformat(expense['created']).month == int(month)]

            total = sum(amount)

            print(f"Total expenses: $ {total} {f"for {months.get(int(month))} . " if self.month else ".  "}")
        return

    def __delete_expense(self):
        expense_id = self.id
        if int(expense_id) <= 0:
            print("Invalid ID")
            return
        expenses = load_expenses()
        try:
            removed = expenses.pop(expense_id)
            self.save_expenses(expenses, write=True)
            print(f'ID: {removed['id']} Expense deleted successfully')
        except KeyError:
            print(f'{default_arguments[0]['description']}{self.id}')

    def save_expenses(self, validated_data: dict, write=False) -> int:
        data = validated_data
        virtual_key = -1
        if not write:
            current_data = load_expenses()

            key = int(max(current_data.keys())) + 1

            current_data[key] = self.update_default_expense(default_arguments[0], validated_data, key)

            data, virtual_key = current_data, key

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            return virtual_key if self.operation else "0"

    @staticmethod
    def update_default_expense(new_expense: dict, validated_data: dict, key: int) -> dict:
        new_expense['id'] = key
        new_expense['description'] = validated_data['description']
        new_expense['amount'] = validated_data['amount']
        new_expense['category'] = validated_data['category']
        new_expense['created'] = datetime.now().strftime("%Y-%m-%d")
        return new_expense

    def __repr__(self) -> str:
        return f''


def main():
    if initialise_database():
        return UserOperationHandler()
    raise RuntimeError("Run Run Run before it burns the end is here motherfucker !")


if __name__ == "__main__":
    print(main())
