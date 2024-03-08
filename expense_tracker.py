from expense import Expense
import calendar
import datetime
import matplotlib.pyplot as plt


def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000
    print(f"💵 Starting Budget: ${budget:.2f}")

    expense = get_user_expense()
    save_expense_to_file(expense, expense_file_path)
    summarize_expenses(expense_file_path, budget)

    expenses = read_expenses_from_file(expense_file_path)
    amount_by_category = calculate_amount_by_category(expenses)
    visualize_expenses_by_category(amount_by_category)


def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = get_valid_amount("Enter expense amount: ")
    expense_category = get_valid_category()
    return Expense(name=expense_name, category=expense_category, amount=expense_amount)


def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                raise ValueError("Expense amount must be greater than zero.")
            return amount
        except ValueError:
            print("Error: Please enter a valid number for expense amount.")


def get_valid_category():
    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Misc",
    ]
    print("Select a category: ")
    for i, category_name in enumerate(expense_categories, start=1):
        print(f"  {i}. {category_name}")

    while True:
        try:
            selected_index = int(
                input(f"Enter a category number [1 - {len(expense_categories)}]: "))
            if selected_index < 1 or selected_index > len(expense_categories):
                raise ValueError("Invalid category number.")
            break
        except ValueError:
            print(
                f"Error: Please enter a valid number between 1 and {len(expense_categories)}.")

    return expense_categories[selected_index - 1]


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense")
    expenses = read_expenses_from_file(expense_file_path)
    amount_by_category = calculate_amount_by_category(expenses)
    print_expenses_by_category(amount_by_category)
    total_spent = sum(expense.amount for expense in expenses)
    print(f"💵 Total Spent: ${total_spent:.2f}")
    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")
    daily_budget = calculate_daily_budget(remaining_budget)
    print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))


def read_expenses_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            expenses = []
            for line in lines:
                name, amount, category = line.strip().split(",")
                expenses.append(
                    Expense(name=name, amount=float(amount), category=category))
            return expenses
    except FileNotFoundError:
        print("File not found. No expenses to summarize.")
        return []


def calculate_amount_by_category(expenses):
    amount_by_category = {}
    for expense in expenses:
        amount_by_category[expense.category] = amount_by_category.get(
            expense.category, 0) + expense.amount
    return amount_by_category


def print_expenses_by_category(amount_by_category):
    print("Expenses By Category 📈:")
    for category, amount in amount_by_category.items():
        print(f"  {category}: ${amount:.2f}")


def calculate_daily_budget(remaining_budget):
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    return remaining_budget / remaining_days


def green(text):
    return f"\033[92m{text}\033[0m"


def visualize_expenses_by_category(amount_by_category, output_file="expenses_by_category.png"):
    print(f"🎯 Visualizing User Expense and saving file to {output_file}")

    categories = list(amount_by_category.keys())
    amounts = list(amount_by_category.values())

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    plt.legend(title='Categories', loc='upper right',
               bbox_to_anchor=(1, 0, 0.5, 1))
    plt.axis('equal')

    # Save the graph as a PNG file
    plt.savefig(output_file)

    plt.close()  # Close the plot to free up memory


if __name__ == "__main__":
    main()
