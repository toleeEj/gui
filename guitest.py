import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize database connection
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table if it doesn’t exist
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT,
                   amount REAL,
                   category TEXT,
                   description TEXT)''')
conn.commit()

# Initialize main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x400")

# Function to add expense
def add_expense():
    date = date_entry.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a numeric amount.")
        return
    category = category_entry.get()
    description = description_entry.get()

    # Insert into database
    cursor.execute("INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
                   (date, amount, category, description))
    conn.commit()

    messagebox.showinfo("Success", "Expense added successfully!")

    # Clear input fields
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# Function to view expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    # Create a new window to display expenses
    view_window = tk.Toplevel(root)
    view_window.title("View Expenses")

    for expense in expenses:
        expense_str = f"ID: {expense[0]}, Date: {expense[1]}, Amount: ${expense[2]}, Category: {expense[3]}, Description: {expense[4]}"
        tk.Label(view_window, text=expense_str).pack()

# Input fields and labels
tk.Label(root, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Description").pack()
description_entry = tk.Entry(root)
description_entry.pack()

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).pack(pady=10)
tk.Button(root, text="View Expenses", command=view_expenses).pack(pady=10)

# Run main loop
root.mainloop()

# Close the database connection
conn.close()
