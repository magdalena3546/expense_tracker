import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

# set variables
BG_COLOR = "#f0f4f8"
HEADER_COLOR = "#1f4e79"
ENTRY_COLOR = "#e0e7ef"
TEXT_COLOR = "#333333"
BORDER_COLOR = "#cccccc"

root = tk.Tk()

# Set title
root.title("Expense Trucker")

# Set styles
root.geometry("600x400")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("vista")


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
    main_frame.pack_forget()


def add_expense():
    main_frame.pack_forget()
    income_frame.grid(row=1, column=0, pady=20)

#Set main
main_frame = ttk.Frame(root)
main_frame.pack(pady=20)

ttk.Label(main_frame, text="Wydatki: 0 zł").pack()
ttk.Label(main_frame, text="Przychody: 0 zł").pack()
ttk.Label(main_frame, text="Dochód: 0 zł").pack()

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

ttk.Label(income_frame, text="Dodaj przychód")
ttk.Label(income_frame, text="Nazwa").grid(row=0, column=0)
entry_income_name = ttk.Entry(income_frame).grid(row = 0, column = 1)
ttk.Label(income_frame, text="Wartość w złotych").grid(row=1, column=0)
entry_income_amount = ttk.Entry(income_frame).grid(row = 1, column = 1)
ttk.Label(income_frame, text="Data").grid(row=2, column=0)
entry_income_date = DateEntry(income_frame, width=12, background = "darkblue", foreground="white", borderwith=2).grid(row = 2, column = 1)


root.mainloop()