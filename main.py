import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import StringVar, messagebox
from db import create_connection, create_tables, insert_categories, get_summary, get_monthly_summary
from datetime import datetime
# set connection with database
con = create_connection("expenses_tracker.db")

if con:
    create_tables(con)
    categories = [("Żywność",), ("Dom",), ("Transport",), ("Rozrywka",), ("Zdrowie",), ("Edukacja",), ("Zwierzęta",), ("Inne",)]
    insert_categories(con, categories)
    con.close()

root = tk.Tk()

# Set title
root.title("Expense tracker")

# Set styles
root.geometry("600x400")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("vista")

# Define grid
root.columnconfigure((0, 1), weight=1)
# root.rowconfigure(2, weight=1)
# Set the window icon
root.iconbitmap("images/icon.ico")

#Main frame
main_frame = ttk.Frame(root)
#Function for main view
def show_main():
    today = datetime.today()
    total_expenses, total_income, total = get_summary()
    total_monthly_expenses, total_monthly_income, total_monthly = get_monthly_summary(today.month, today.year)
    #Remove all widgets from main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    #Add content to maim_frame
    ttk.Label(main_frame, text="Konto").grid(row=0, column=0, padx=(10,30), pady=10)
    ttk.Label(main_frame, text=f"Przychody: {total_income:.2f} zł").grid(row=1, column=0, padx=(10,30), pady=10)
    ttk.Label(main_frame, text=f"Wydatki: {total_expenses:.2f} zł").grid(row=2, column=0, padx=(10,30), pady=10)
    ttk.Label(main_frame, text=f"Dochód: {total:.2f} zł").grid(row=3, column=0, padx=(10,30), pady=10)

    ttk.Label(main_frame, text="Podsumowanie miesięczne").grid(row=0, column=1, padx=10, pady=10)
    ttk.Label(main_frame, text=f"Przychody: {total_monthly_income:.2f} zł").grid(row=1, column=1, padx=10, pady=10)
    ttk.Label(main_frame, text=f"Wydatki: {total_monthly_expenses:.2f} zł").grid(row=2, column=1, padx=10, pady=10)
    ttk.Label(main_frame, text=f"Dochód: {total_monthly:.2f} zł").grid(row=3, column=1, padx=10, pady=10)

    main_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
# functions to create treeview
def create_treeview(frame):
    columns = ("id", "name", "amount", "category", "date", "type")
    tree = ttk.Treeview(frame, columns = columns, show="headings")
    tree.heading("id", text="id")
    tree.heading("name", text="nazwa")
    tree.heading("amount", text="wartość")
    tree.heading("category", text="kategoria")
    tree.heading("date", text="data")
    tree.heading("type", text="typ")
    tree.column("id", width=0, stretch=False)
    tree.column("name", width=150)
    tree.column("amount", width=100)
    tree.column("category", width=100)
    tree.column("date", width=100)
    tree.column("type", width=100)
    tree.grid(row=0, column=0, pady=20, sticky="nsew")
    return tree
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
    add_button.place_forget()
    income_button.place_forget()
    expense_button.place_forget()
    main_frame.grid_forget()
    income_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")

def add_expense():
    add_button.place_forget()
    income_button.place_forget()
    expense_button.place_forget()
    main_frame.grid_forget()
    expense_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
    
def submit_income():
    name = entry_income_name.get()
    amount = entry_income_amount.get()
    date = entry_income_date.get_date()
    date_str = date.strftime('%Y-%m-%d')
    if not name or not amount or not date_str:
        messagebox.showerror("Błąd", "Wypełnij wszytskie pola!")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Błąd", "Podaj kwotę w liczbie!")
        return
    
    con = create_connection("expenses_tracker.db")
    cursor = con.cursor()
    try:
        if hasattr(income_frame, "trans_id"):
            cursor.execute(""" 
                UPDATE income
                SET name = ?, amount = ?, date = ?
                WHERE id = ?
            """, (name, amount, date, income_frame.trans_id))
            del income_frame.trans_id
            messagebox.showinfo("Sukces", "Przychód został zaktualizowany.")
        else:
            cursor.execute(
                "INSERT INTO income (name, amount, date) VALUES (?, ?, ?)",
                (name, amount, date_str)
            )
            messagebox.showinfo("Sukces", "Dodano nowy przychód.")
        con.commit()
    except Exception as e:
        messagebox.showerror("Błąd", "Przychód nie został zapisany.")
    finally:
        con.close()
        entry_income_name.delete(0, tk.END)
        entry_income_amount.delete(0, tk.END)
        entry_income_date.set_date(datetime.today())
        income_frame.grid_forget()
        show_main()
        add_button.place(x=500, y=350)

def submit_expense():
    name = entry_expense_name.get()
    amount = entry_expense_amount.get()
    date = entry_expense_date.get_date()
    date_str = date.strftime('%Y-%m-%d')
    category = categories.get()

    if not name or not amount or not date_str or category == "Wybierz":
        messagebox.showerror("Błąd", "Wypełnij wszytskie pola!")
        return
    try:
        amount = float(amount) 
    except ValueError:
        messagebox.showerror("Błąd", "Podaj kwotę w liczbie!")
        return
    
    con = create_connection("expenses_tracker.db")
    cursor = con.cursor()

    cursor.execute("SELECT id FROM categories WHERE name = ?", (category,))
    category_id = cursor.fetchone()
    if category_id is None:
        messagebox.showerror("Błąd", "Nie znaleziono kategorii.")
        return
    try:
        if hasattr(expense_frame, "trans_id"):
            cursor.execute(""" 
                UPDATE expenses
                SET name = ?, amount = ?, date = ?, category_id = ?
                WHERE id = ?
            """, (name, amount, date, category_id[0], expense_frame.trans_id))
            del expense_frame.trans_id
            messagebox.showinfo("Sukces", "Zaktualizowano wydatek.")
        else:
            cursor.execute(
                "INSERT INTO expenses (name, amount, date, category_id) VALUES (?, ?, ?, ?)",
                (name, amount, date_str, category_id[0])
            )
            messagebox.showinfo("Sukces", "Dodano wydatek.")
        con.commit()
    except Exception as e:
        print(e)
        messagebox.showerror("Błąd", "Wydatek nie został zapisany")
    finally: 
        con.close()
        entry_expense_name.delete(0, tk.END)
        entry_expense_amount.delete(0, tk.END)
        entry_expense_date.set_date(datetime.today())
        categories.set("Wybierz")
        expense_frame.grid_forget()
        show_main()
        add_button.place(x=500, y=350)
# Function for create close button

def create_close_button(parent, command, **parameters):
    return ttk.Button(parent, text="X", command=command, **parameters).place(x=200, y=0)

# Function to close forms
def close():
    if(income_frame.winfo_viewable()):
        income_frame.grid_forget()
    else: 
        expense_frame.grid_forget()
    show_main()
    add_button.place(x=500, y=350)

# Function to show transactions
def show_transactions():
    for widget in main_frame.winfo_children():
        widget.destroy()
    ttk.Label(main_frame, text="Lista transakcji").grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    tree = create_treeview(main_frame)
    try:
        con = create_connection("expenses_tracker.db")
        cursor = con.cursor()
        cursor.execute("""
            SELECT id, name, amount, '' as category, date, 'przychód' as type FROM income
        """)
        income_rows = cursor.fetchall()

        cursor.execute("""
            SELECT e.id, e.name, e.amount, c.name as category, e.date, 'wydatek' as type FROM expenses e
            JOIN categories c ON e.category_id = c.id
        """)
        expenses_rows = cursor.fetchall()

        rows =income_rows + expenses_rows
        for row in rows:
            tree.insert('', tk.END, values=row)
        con.close()

        # Add button for delete and edit transaction
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        edit_btn = ttk.Button(button_frame, text= "Edytuj zaznaczoną transakcję", command=lambda: edit_transaction(tree))
        edit_btn.pack(side="left", padx=(0, 10), ipadx=10, ipady=5)
        delete_btn = ttk.Button(button_frame, text="Usuń zaznaczoną transakcję", command=lambda: delete_transaction(tree))
        delete_btn.pack(side="left", ipadx=10, ipady=5)
    except Exception as e:
        print(e)
        print("Błąd podczas pobierania danych")
# Function to delete transaction
def delete_transaction(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Błąd", "Nie zaznaczono transakcji do usunięcia.")
        return
    
    values = tree.item(selected_item[0], "values")
    id_trans, name, amount, category, date, type_trans = values
    confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę transakcję?")
    if not confirm:
        return
    try:
        con = create_connection("expenses_tracker.db")
        cursor = con.cursor()

        if type_trans == "przychód":
            cursor.execute("DELETE FROM income WHERE id=?", (id_trans))
        else:
            cursor.execute("DELETE FROM expenses WHERE id=?", (id_trans))
        con.commit()
        con.close()

        tree.delete(selected_item[0])
        messagebox.showinfo("Sukces", "Usunięto transakcję.")
    except Exception as e:
        print(e)
        messagebox("Błąd", "Wystąpił błąd podczas usuwania transakcji.")
# Function to edit transaction:
def edit_transaction(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Błąd", "Nie zaznaczono transakcji do usunięcia.")
        return
    main_frame.grid_forget()
    values = tree.item(selected_item[0], "values")
    id_trans, name, amount, category, date, type_trans = values

    if type_trans == "przychód":
        entry_income_name.delete(0, tk.END)
        entry_income_name.insert(0, name)
        entry_income_amount.delete(0, tk.END)
        entry_income_amount.insert(0, amount)
        entry_income_date.set_date(date)
        income_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
        income_frame.trans_id = id_trans
        
    else:
        entry_expense_name.delete(0, tk.END)
        entry_expense_name.insert(0, name)
        entry_expense_amount.delete(0, tk.END)
        entry_expense_amount.insert(0, amount)
        entry_expense_date.set_date(date)
        categories.set(category)
        expense_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
        expense_frame.trans_id = id_trans

    
# Function to show visualizations
def show_visualizations():
    for widget in main_frame.winfo_children():
        widget.destroy()
        ttk.Label(main_frame, text="Wizualizacje").grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
#Set menu
menu_bar = tk.Menu(root)
menu_bar.add_command(label="Podsumowanie",command=show_main)
menu_bar.add_command(label="Transakcje",command=show_transactions)
menu_bar.add_command(label="Wizualizacje", command=show_visualizations)
root.config(menu=menu_bar)

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
entry_income_date = DateEntry(income_frame, width=12, background = "darkblue", foreground="white", borderwith=2, date_pattern = "yyyy-mm-dd")
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
entry_expense_date = DateEntry(expense_frame, width=12, background="darkblue", foreground="white", borderwith=2, date_pattern = "yyyy-mm-dd")
entry_expense_date.grid(row=3, column=1, pady=5, sticky="w")
ttk.Label(expense_frame, text="Kategoria").grid(row=4, column=0, pady=5)
category_var = StringVar()
categories = ttk.Combobox(expense_frame, textvariable=category_var, width= 15,state="readonly")
categories["values"] = ["Żywność", "Dom", "Transport", "Rozrywka", "Zdrowie", "Edukacja", "Zwierzęta", "Inne"]
categories.set("Wybierz")
categories.grid(row=4, column=1, pady=5)

ttk.Button(expense_frame, text="Submit", command=submit_expense).grid(row=5, column=0, columnspan=2, pady=10)

show_main()
root.mainloop()