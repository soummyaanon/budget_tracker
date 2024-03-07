# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from budget_app.budget import Budget
from budget_app.currency_converter import convert_currency
import pandas as pd


# Create a GUI application
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.config(bg="light steel blue")


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
        self.income_label = tk.Label(self, text="Personal Budget Trackert", width=100, height=2)
        self.income_label.pack()
        self.income_entry = tk.Entry(self, width=30, bg="black", fg="white", font="Arial 20 bold", borderwidth=5, relief="sunken", insertbackground="white")
        self.income_entry.pack()
        self.income_button = tk.Button(self, text="Add Income", command=self.add_income, width=30, height=2, ) 
        self.income_button.pack()

        self.tax_rate_label = tk.Label(self, text="Tax Rate (%)")
        self.tax_rate_label.pack()
        self.tax_rate_entry = tk.Entry(self, width=30, bg="black", fg="white", font="Arial 20 bold", borderwidth=5, relief="sunken", insertbackground="white")
        self.tax_rate_entry.pack()
        self.tax_button = tk.Button(self, text="Calculate Net Income", command=self.calculate_net_income, width=30, height=2,) 
        self.tax_button.pack()

        self.expense_label = tk.Label(self, text="Expense")
        self.expense_label.pack()
        self.expense_entry =tk.Entry(self, width=30, bg="black", fg="white", font="Arial 20 bold", borderwidth=5, relief="sunken", insertbackground="white")
        self.expense_entry.pack()

        self.expense_category_label = tk.Label(self, text="Expense Category")
        self.expense_category_label.pack()
        self.expense_category_combobox = ttk.Combobox(self, values=["Rent","Veichile", "Groceries", "Transportation", "Entertainment","Taxes", "Other"])
        self.expense_category_combobox.pack()

        self.expense_button = tk.Button(self, text="Add Expense", command=self.add_expense, width=30, height=2,)
        self.expense_button.pack()

        self.remaining_budget_button = tk.Button(self, text="Show Remaining Budget", command=self.show_remaining_budget, width=30, height=2,)
        self.remaining_budget_button.pack()

        self.show_expenditures_button = tk.Button(self, text="Show Expenditures", command=self.show_expenditures, width=30, height=2,)
        self.show_expenditures_button.pack()

        self.download_button = tk.Button(self, text="Download Data", command=self.download_data_as_csv, width=30, height=2,)
        self.download_button.pack()

        self.amount_label = tk.Label(self, text="Amount")
        self.amount_label.pack()
        self.amount_entry =tk.Entry(self, width=30, bg="black", fg="white", font="Arial 20 bold", borderwidth=5, relief="sunken", insertbackground="white")
        self.amount_entry.pack()

        self.from_currency_label = tk.Label(self, text="From Currency")
        self.from_currency_label.pack()
        self.from_currency_combobox = ttk.Combobox(self, values=[ "INR" ,"USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])
        self.from_currency_combobox.pack()

        self.to_currency_label = tk.Label(self, text="To Currency")
        self.to_currency_label.pack()
        self.to_currency_combobox = ttk.Combobox(self, values=[ "INR","USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])
        self.to_currency_combobox.pack()

        self.convert_button = tk.Button(self, text="Convert Currency", command=self.convert_currency, width=30, height=2,)
        self.convert_button.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy, width=10, height=2,)
        self.quit.pack()



# Define the methods
    def add_income(self):
        income = self.income_entry.get()
        self.collection.insert_one({"Income": income})
        if income:  # check if the field is not empty
            amount = float(income)
            self.budget.add_income(amount)
            messagebox.showinfo("Income", f"Added income of {amount}")
    
    def calculate_net_income(self):
        tax_rate = self.tax_rate_entry.get()
        if tax_rate:  # check if the field is not empty
            tax_rate = float(tax_rate) / 100
            net_income = self.budget.get_income() * (1 - tax_rate)
            self.collection.insert_one({"Net Income": net_income})
            messagebox.showinfo("Net Income", f"Net income after {tax_rate * 100}% tax is {net_income}")

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
    
    
    def download_data_as_csv(self):
        # Fetch all documents from the collection
        data = self.collection.find()

        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(list(data))

        # Save the DataFrame as a CSV file
        df.to_csv('data.csv', index=False)


    


# Create the application
root = tk.Tk()
app = Application(master=root)
app.mainloop()
