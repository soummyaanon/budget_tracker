# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from budget_app.budget import Budget
from budget_app.currency_converter import convert_currency


# Create a GUI application
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        # Create a MongoClient to the running mongod instance
        self.client = MongoClient('mongodb://localhost:27017/')

        # Get a reference to a particular database
        self.db = self.client['Budget']

        # Access a collection in the database
        self.collection = self.db['MyDATA']

        # Initialize the budget attribute
        self.budget = Budget(0)  # assuming Budget is a class you have defined elsewhere



# Create the widgets
    def create_widgets(self):
        self.income_label = tk.Label(self, text="Income")
        self.income_label.pack()
        self.income_entry = tk.Entry(self)
        self.income_entry.pack()
        self.income_button = tk.Button(self, text="Add Income", command=self.add_income)
        self.income_button.pack()

        self.expense_label = tk.Label(self, text="Expense")
        self.expense_label.pack()
        self.expense_entry = tk.Entry(self)
        self.expense_entry.pack()

        self.expense_category_label = tk.Label(self, text="Expense Category")
        self.expense_category_label.pack()
        self.expense_category_combobox = ttk.Combobox(self, values=["Rent", "Groceries", "Transportation", "Entertainment","Taxes", "Other"])
        self.expense_category_combobox.pack()

        self.expense_button = tk.Button(self, text="Add Expense", command=self.add_expense)
        self.expense_button.pack()

        self.remaining_budget_button = tk.Button(self, text="Show Remaining Budget", command=self.show_remaining_budget)
        self.remaining_budget_button.pack()

        self.show_expenditures_button = tk.Button(self, text="Show Expenditures", command=self.show_expenditures)
        self.show_expenditures_button.pack()

        self.amount_label = tk.Label(self, text="Amount")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        self.from_currency_label = tk.Label(self, text="From Currency")
        self.from_currency_label.pack()
        self.from_currency_combobox = ttk.Combobox(self, values=[ "INR" ,"USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])
        self.from_currency_combobox.pack()

        self.to_currency_label = tk.Label(self, text="To Currency")
        self.to_currency_label.pack()
        self.to_currency_combobox = ttk.Combobox(self, values=[ "INR","USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])
        self.to_currency_combobox.pack()

        self.convert_button = tk.Button(self, text="Convert Currency", command=self.convert_currency)
        self.convert_button.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack()



# Define the methods
    def add_income(self):
        income = self.income_entry.get()
        self.collection.insert_one({"Income": income})
        if income:  # check if the field is not empty
            amount = float(income)
            self.budget.add_income(amount)
            messagebox.showinfo("Income", f"Added income of {amount}")

    def add_expense(self):
        expense = self.expense_entry.get()
        self.collection.insert_one({"Expense": expense})
        if expense:  # check if the field is not empty
            amount = float(expense)
            category = self.expense_category_combobox.get()
            if self.budget.add_expense(amount, category):
                messagebox.showinfo("Expense", f"Added expense of {amount} for {category}")
            else:
                messagebox.showerror("Error", "Expense exceeds remaining budget")

    def show_remaining_budget(self):
        remaining_budget = self.budget.get_remaining_budget()
        self.collection.insert_one({"Remaining Budget": remaining_budget})
        messagebox.showinfo("Remaining Budget", f"Remaining budget is {remaining_budget}")

    def convert_currency(self):
        amount = float(self.amount_entry.get())
        from_currency = self.from_currency_combobox.get()
        to_currency = self.to_currency_combobox.get()
        converted_amount = convert_currency(amount, from_currency, to_currency)
        messagebox.showinfo("Converted Amount", f"{amount} {from_currency} is equal to {converted_amount} {to_currency}")

    def show_expenditures(self):
        expenditures = self.budget.get_expenditures()
        expenditures_str = "\n".join(f"{amount} for {category}" for amount, category in expenditures)
        messagebox.showinfo("Expenditures", expenditures_str)


# Create the application
root = tk.Tk()
app = Application(master=root)
app.mainloop()