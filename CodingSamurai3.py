import datetime
import os
import tkinter as tk
from tkinter import messagebox

class ExpenseTracker:
    def __init__(self, filename):
        self.expenses = []
        self.filename = filename
        self.load_data()
        self.root = tk.Tk()
        self.root.title("Expense Tracker")
        self.current_frame = None
        self.main_menu()

    def main_menu(self):
        self.clear_current_frame()

        main_menu_frame = tk.Frame(self.root, padx=10, pady=10)
        main_menu_frame.pack()

        tk.Button(main_menu_frame, text="Add Expense", command=self.show_add_expense).pack(padx=10, pady=10)
        tk.Button(main_menu_frame, text="List Expenses", command=self.show_expense_list).pack(padx=10, pady=10)
        tk.Button(main_menu_frame, text="Calculate Total Expenses", command=self.show_calculate_expenses).pack(padx=10, pady=10)
        tk.Button(main_menu_frame, text="Generate Monthly Report", command=self.show_monthly_report).pack(padx=10, pady=10)
        tk.Button(main_menu_frame, text="Exit", command=self.root.quit).pack(padx=10, pady=10)

        self.current_frame = main_menu_frame

    def show_add_expense(self):
        self.clear_current_frame()

        add_expense_frame = tk.Frame(self.root, padx=10, pady=10)
        add_expense_frame.pack()

        tk.Label(add_expense_frame, text="Amount:").grid(row=0, column=0, padx=10, pady=10)
        amount_entry = tk.Entry(add_expense_frame)
        amount_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_expense_frame, text="Category:").grid(row=1, column=0, padx=10, pady=10)
        category_entry = tk.Entry(add_expense_frame)
        category_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_expense_frame, text="Description:").grid(row=2, column=0, padx=10, pady=10)
        description_entry = tk.Entry(add_expense_frame)
        description_entry.grid(row=2, column=1, padx=10, pady=10)

        add_button = tk.Button(add_expense_frame, text="Add Expense", command=lambda: self.add_expense(amount_entry.get(), category_entry.get(), description_entry.get()))
        add_button.grid(row=3, columnspan=2, padx=10, pady=10)

        back_button = tk.Button(add_expense_frame, text="Back", command=self.main_menu)
        back_button.grid(row=4, columnspan=2, padx=10, pady=10)

        self.current_frame = add_expense_frame

    def add_expense(self, amount, category, description):
        try:
            amount = float(amount)
            date = datetime.date.today()
            self.expenses.append({"date": date, "amount": amount, "category": category, "description": description})
            self.save_data()
            messagebox.showinfo("Success", "Expense added successfully.")
            self.main_menu()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")

    def show_expense_list(self):
        self.clear_current_frame()

        expense_list_frame = tk.Frame(self.root, padx=10, pady=10)
        expense_list_frame.pack()

        expense_list = "\n".join([f"Date: {expense['date']}, Amount: {expense['amount']}, Category: {expense['category']}, Description: {expense['description']}" for expense in self.expenses])
        tk.Label(expense_list_frame, text=expense_list).pack(padx=10, pady=10)

        back_button = tk.Button(expense_list_frame, text="Back", command=self.main_menu)
        back_button.pack(padx=10, pady=10)

        self.current_frame = expense_list_frame

    def show_calculate_expenses(self):
        self.clear_current_frame()

        calculate_frame = tk.Frame(self.root, padx=10, pady=10)
        calculate_frame.pack()

        tk.Label(calculate_frame, text="Calculate total expenses for:").pack(side="left")
        tk.Button(calculate_frame, text="Daily", command=lambda: self.calculate_total_expenses("daily")).pack(side="left", padx=5)
        tk.Button(calculate_frame, text="Weekly", command=lambda: self.calculate_total_expenses("weekly")).pack(side="left", padx=5)
        tk.Button(calculate_frame, text="Monthly", command=lambda: self.calculate_total_expenses("monthly")).pack(side="left", padx=5)

        back_button = tk.Button(calculate_frame, text="Back", command=self.main_menu)
        back_button.pack(padx=10, pady=10)

        self.current_frame = calculate_frame

    def calculate_total_expenses(self, timeframe):
        total = 0
        today = datetime.date.today()
        if timeframe == "daily":
            total = sum(expense["amount"] for expense in self.expenses if expense["date"] == today)
        elif timeframe == "weekly":
            total = sum(expense["amount"] for expense in self.expenses if expense["date"].isocalendar()[1] == today.isocalendar()[1])
        elif timeframe == "monthly":
            total = sum(expense["amount"] for expense in self.expenses if expense["date"].month == today.month)
        messagebox.showinfo("Total Expenses", f"Total expenses for {timeframe} timeframe: {total}")

    def show_monthly_report(self):
        self.clear_current_frame()

        report_frame = tk.Frame(self.root, padx=10, pady=10)
        report_frame.pack()

        today = datetime.date.today()
        categories = {}
        for expense in self.expenses:
            if expense["date"].month == today.month:
                if expense["category"] in categories:
                    categories[expense["category"]] += expense["amount"]
                else:
                    categories[expense["category"]] = expense["amount"]
        report = ""
        for category, amount in categories.items():
            report += f"Category: {category}, Amount: {amount}\n"

        tk.Label(report_frame, text=report).pack(padx=10, pady=10)

        back_button = tk.Button(report_frame, text="Back", command=self.main_menu)
        back_button.pack(padx=10, pady=10)

        self.current_frame = report_frame

    def save_data(self):
        with open(self.filename, "w") as file:
            for expense in self.expenses:
                file.write(f"{expense['date']},{expense['amount']},{expense['category']},{expense['description']}\n")

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                for line in file:
                    date, amount, category, description = line.strip().split(",")
                    self.expenses.append({"date": datetime.datetime.strptime(date, "%Y-%m-%d").date(), "amount": float(amount), "category": category, "description": description})

    def clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    filename = "expenses.txt"
    tracker = ExpenseTracker(filename)
    tracker.run()
