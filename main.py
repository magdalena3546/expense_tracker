import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import StringVar
from db import create_connection, create_tables, insert_categories

# set connection with database
con = create_connection("expense_tracked.db")

if con:
    create_tables(con)
    # categories = [("Żywność",), ("Dom",), ("Transport",), ("Rozrywka",), ("Zdrowie",), ("Edukacja",), ("Zwierzęta",), ("Inne",)]
    # insert_categories(con, categories)
    con.close()

root = tk.Tk()

# Set title
root.title("Expense Trucker")

# Set styles
root.geometry("600x400")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("vista")

# Define grid
root.columnconfigure((0, 1), weight=1)
root.rowconfigure(0, weight=1)
# Set the window icon
root.iconbitmap("images/icon.ico")

# Functions for buttons
def add_button_function():
    if(expense_button.winfo_viewable() and income_button.winfo_viewable()):
        expense_button.place_forget()
        income_button.place_forget()
    else:
        x = add_button.winfo_x()
        y = add_button.winfo_y()
        expense_button.place(x= x, y=y-30)
        income_button.place(x=x, y=y-60)

def add_income():
    main_frame.grid_forget()
    income_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")

def add_expense():
    main_frame.grid_forget()
    expense_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
    
def submit_income():
    pass

def submit_expense():
    pass

# Function for create close button

def create_close_button(parent, command, **parameters):
    return ttk.Button(parent, text="X", command=command, **parameters).place(x=200, y=0)

# Function to close forms
def close():
    if(income_frame.winfo_viewable()):
        income_frame.grid_forget()
    else: 
        expense_frame.grid_forget()
    main_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")

#Set main
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")

ttk.Label(main_frame, text="Wydatki: 0 zł").grid(row=0, column=0)
ttk.Label(main_frame, text="Przychody: 0 zł").grid(row=1, column=0)
ttk.Label(main_frame, text="Dochód: 0 zł").grid(row=2, column=0)

# Create buttons
add_button= ttk.Button(root,
                text="+", 
                command=add_button_function
                )
add_button.place(x=500, y=350)

income_button = ttk.Button(root,
                        text="Przychód",
                        command=add_income)

expense_button = ttk.Button(root,
                        text="Wydatek",
                        command=add_expense)

# Set form for Income
income_frame = ttk.Frame(root)
close_button_income = create_close_button(income_frame, close)
ttk.Label(income_frame, text="Dodaj przychód").grid(row=0, column=0, columnspan=2, pady=10)
ttk.Label(income_frame, text="Nazwa").grid(row=1, column=0, pady=5)
entry_income_name = ttk.Entry(income_frame)
entry_income_name.grid(row = 1, column = 1, pady=5)
ttk.Label(income_frame, text="Wartość").grid(row=2, column=0, pady=5)
entry_income_amount = ttk.Entry(income_frame)
entry_income_amount.grid(row = 2, column = 1, pady=5)
ttk.Label(income_frame, text="Data").grid(row=3, column=0, pady=5)
entry_income_date = DateEntry(income_frame, width=12, background = "darkblue", foreground="white", borderwith=2)
entry_income_date.grid(row = 3, column = 1, pady=5, sticky="w")
ttk.Button(income_frame, text="Submit", command=submit_income).grid(row=4, column = 0, columnspan=2, pady=10)

# Set form for Expense
expense_frame = ttk.Frame(root)
close_button_expense = create_close_button(expense_frame, close)
ttk.Label(expense_frame, text="Dodaj wydatek").grid(row=0, column=0, columnspan=2, pady=10)
ttk.Label(expense_frame, text="Nazwa").grid(row=1, column=0, pady=5)
entry_expense_name = ttk.Entry(expense_frame)
entry_expense_name.grid(row=1, column=1)
ttk.Label(expense_frame, text="Wartość").grid(row=2, column=0, pady=5)
entry_expense_amount = ttk.Entry(expense_frame)
entry_expense_amount.grid(row=2, column=1)
ttk.Label(expense_frame, text="Data").grid(row=3, column=0, pady=5)
entry_expense_date = DateEntry(expense_frame, width=12, background="darkblue", foreground="white", borderwith=2)
entry_expense_date.grid(row=3, column=1, pady=5, sticky="w")
ttk.Label(expense_frame, text="Kategoria").grid(row=4, column=0, pady=5)
category_var = StringVar()
categories = ttk.Combobox(expense_frame, textvariable=category_var, width= 15,state="readonly")
categories["values"] = ["Żywność", "Dom", "Transport", "Rozrywka", "Zdrowie", "Edukacja", "Zwierzęta", "Inne"]
categories.grid(row=4, column=1, pady=5)

ttk.Button(expense_frame, text="Submit", command=submit_expense).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()