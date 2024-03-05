# budget.py
class Expense:
    def __init__(self, amount, category):
        self.amount = amount
        self.category = category

class Budget:
    def __init__(self, initial_income):
        self.income = initial_income
        self.expenses = []

    def add_income(self, amount):
        self.income += amount

    def add_expense(self, amount, category):
        if amount <= self.get_remaining_budget():
            expense = Expense(amount, category)
            self.expenses.append(expense)
            return True  # Expense added successfully
        else:
            return False  # Expense exceeds remaining budget

    def get_remaining_budget(self):
        total_expenditures = sum(expense.amount for expense in self.expenses)
        remaining_budget = self.income - total_expenditures
        return remaining_budget / self.income * 100  # return remaining budget as a percentage of income

    def get_expenditures(self):
        return [(expense.amount, expense.category) for expense in self.expenses]
    def get_income(self):
        return self.income