import tkinter as tk  
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from visualizations import create_pie_chart, create_visualizations
from tkinter import StringVar, messagebox
from db import create_connection, create_tables, insert_categories, get_summary, get_monthly_summary
from datetime import datetime
# set connection with database
con = create_connection("expenses_tracker.db")

global income_button, expense_button, add_button

if con:
    create_tables(con)
    categories = [("Żywność",), ("Dom",), ("Transport",), ("Rozrywka",), ("Zdrowie",), ("Edukacja",), ("Zwierzęta",), ("Inne",)]
    insert_categories(con, categories)
    con.close()

root = ttk.Window(themename="superhero")
#set size and position of window
window_width = 1400
window_height = 1300
position_right = int(root.winfo_screenwidth()/2  - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
root.option_add("*Font", "Helvetica 10")
# Set title
root.title("Expense tracker")
root.resizable(False, False)
# # Set styles
# Define grid
root.columnconfigure((0, 1), weight=1)
# Set the window icon
root.iconbitmap("images/icon.ico")

#Main frame
main_frame = ttk.Frame(root)
#Function for main view
def show_main():
    global add_button, income_button, expense_button
    today = datetime.today()
    total_expenses, total_income, total = get_summary()
    total_monthly_expenses, total_monthly_income, total_monthly = get_monthly_summary(today.month, today.year)
    #Remove all widgets from main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    #Add content to maim_frame
    summary_frame= ttk.Frame(main_frame, padding=(30, 30), relief="solid", borderwidth=2)
    summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    ttk.Label(summary_frame, text="Podsumowanie", font=("Helvetica, 14")).grid(row=0, column=0, pady=5, sticky="w")
    ttk.Label(summary_frame, text="Przychody: ").grid(row=1, column=0,  pady=5, sticky="w")
    ttk.Label(summary_frame, text=f"{total_income:.2f} zł", bootstyle="success").grid(row=1, column=1, pady=5, sticky="e")
    ttk.Label(summary_frame, text="Wydatki: ").grid(row=2, column=0,  pady=5, sticky="w")
    ttk.Label(summary_frame, text=f"{total_expenses:.2f} zł", bootstyle="danger").grid(row=2, column=1, pady=5, sticky="e")
    ttk.Label(summary_frame, text="Dochód: ").grid(row=3, column=0, pady=5, sticky="w")
    ttk.Label(summary_frame, text=f"{total:.2f} zł", bootstyle="primary").grid(row=3, column=1, pady=5, sticky="e")
    chart_frame = ttk.Frame(summary_frame, padding=(10, 10))
    chart_frame.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nsew")
    create_pie_chart(chart_frame, total_expenses, total_income)

    monthly_summary_frame = ttk.Frame(main_frame, padding=(30, 30), relief="solid", borderwidth=2)
    monthly_summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    ttk.Label(monthly_summary_frame, text="Bieżący miesiąc", font=("Helvetica, 14")).grid(row=0, column=0, pady=5, sticky="w")
    ttk.Label(monthly_summary_frame, text="Przychody: ").grid(row=1, column=0, pady=5, sticky="w")
    ttk.Label(monthly_summary_frame, text=f"{total_monthly_income:.2f} zł", bootstyle="success").grid(row=1, column=1, pady=5, sticky="e")
    ttk.Label(monthly_summary_frame, text="Wydatki: ").grid(row=2, column=0, pady=5, sticky="w")
    ttk.Label(monthly_summary_frame, text=f"{total_monthly_expenses:.2f} zł", bootstyle="danger").grid(row=2, column=1, pady=5, sticky="e")
    ttk.Label(monthly_summary_frame, text="Dochód: ").grid(row=3, column=0, pady=5, sticky="w")
    ttk.Label(monthly_summary_frame, text=f"{total_monthly:.2f} zł", bootstyle="primary").grid(row=3, column=1, pady=5, sticky="e")
    chart_frame_month = ttk.Frame(monthly_summary_frame, padding=(10, 10))
    chart_frame_month.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nsew")
    create_pie_chart(chart_frame_month, total_monthly_expenses, total_monthly_income)
    # Create buttons
    add_button= ttk.Button(main_frame,
                    text="+", 
                    command=add_button_function,
                    padding=(20, 10)
                    )
    add_button.grid(row=3, column=0, sticky="e", padx=10, pady=(80,10))

    income_button = ttk.Button(main_frame,
                            text="Przychód",
                            command=add_income)

    expense_button = ttk.Button(main_frame,
                            text="Wydatek",
                            command=add_expense)
    main_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
# functions to create treeview
def create_treeview(frame):
    columns = ("id", "name", "amount", "category", "date", "type")
    tree = ttk.Treeview(frame, columns = columns, show="headings")
    tree.heading("id", text="id")
    tree.heading("name", text="nazwa", anchor="w")
    tree.heading("amount", text="wartość", anchor="w")
    tree.heading("category", text="kategoria", anchor="w")
    tree.heading("date", text="data", anchor="w")
    tree.heading("type", text="typ", anchor="w")
    tree.column("id", width=0, stretch=False)
    tree.column("name", width=150)
    tree.column("amount", width=100)
    tree.column("category", width=120)
    tree.column("date", width=120)
    tree.column("type", width=100)
    tree.grid(row=0, column=0, pady=20, sticky="nsew")
    return tree
# Functions for buttons
def add_button_function():
    global add_button, income_button, expense_button
    if(expense_button.winfo_viewable() and income_button.winfo_viewable()):
        expense_button.place_forget()
        income_button.place_forget()
    else:
        x = add_button.winfo_x()
        y = add_button.winfo_y()
        expense_button.place(x= x, y=y-80)
        income_button.place(x=x, y=y-160)

def add_income():
    main_frame.grid_forget()
    income_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
    root.config(menu="")

def add_expense():
    main_frame.grid_forget()
    expense_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
    root.config(menu="")
def submit_income():
    name = entry_income_name.get()
    amount = entry_income_amount.get()
    date = entry_income_date.entry.get()

    if not name or not amount or not date:
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
                (name, amount, date)
            )
            messagebox.showinfo("Sukces", "Dodano nowy przychód.")
        con.commit()
    except Exception as e:
        messagebox.showerror("Błąd", "Przychód nie został zapisany.")
    finally:
        con.close()
        entry_income_name.delete(0, tk.END)
        entry_income_amount.delete(0, tk.END)
        today = datetime.today().strftime('%d.%m.%Y')
        entry_income_date.entry.delete(0, tk.END)
        entry_income_date.entry.insert(0, today)
        income_frame.grid_forget()
        root.config(menu=menu_bar)
        show_main()

def submit_expense():
    name = entry_expense_name.get()
    amount = entry_expense_amount.get()
    date = entry_expense_date.entry.get()
    # date_str = date.strftime('%Y-%m-%d')
    category = categories.get()

    if not name or not amount or not date or category == "Wybierz":
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
                (name, amount, date, category_id[0])
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
        today = datetime.today().strftime('%d.%m.%Y')
        entry_expense_date.entry.delete(0, tk.END)
        entry_expense_date.entry.insert(0, today)
        categories.set("Wybierz")
        expense_frame.grid_forget()
        root.config(menu=menu_bar)
        show_main()
# Function for create close button

def create_close_button(parent, command):
    return ttk.Button(parent, text="X", command=command, style="danger.Outline.TButton", padding=(20, 10)).grid(row=0, column=2, padx=20, pady=20)

# Function to close forms
def close():
    if(income_frame.winfo_viewable()):
        income_frame.grid_forget()
    else: 
        expense_frame.grid_forget()
    root.config(menu=menu_bar)
    show_main()

# Function to show transactions
def show_transactions():
    for widget in main_frame.winfo_children():
        widget.destroy()
    ttk.Label(main_frame, text="Lista transakcji", font="Helvetica, 14").grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    tree = create_treeview(main_frame)
    tree.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
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
        button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
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
    root.config(menu="")
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
        entry_income_date.entry.delete(0, tk.END)
        entry_income_date.entry.insert(0, date)
        income_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
        income_frame.trans_id = id_trans
        
    else:
        entry_expense_name.delete(0, tk.END)
        entry_expense_name.insert(0, name)
        entry_expense_amount.delete(0, tk.END)
        entry_expense_amount.insert(0, amount)
        entry_expense_date.entry.delete(0, tk.END)
        entry_expense_date.entry.insert(0, date)
        categories.set(category)
        expense_frame.grid(row=0, column=1, pady=20, padx=20,sticky="nsew")
        expense_frame.trans_id = id_trans

    
# Function to show visualizations
def show_visualizations():
    total_expenses, total_income, total = get_summary()
    today = datetime.today()
    total_monthly_expenses, total_monthly_income, total_monthly = get_monthly_summary(today.month, today.year)
    create_visualizations(root, total_expenses, total_income, total_monthly_expenses, total_monthly_income)
#Set menu
menu_bar = ttk.Menu(root)
menu_bar.add_command(label="Podsumowanie",command=show_main)
menu_bar.add_command(label="Transakcje",command=show_transactions)
menu_bar.add_command(label="Wizualizacje", command=show_visualizations)
root.config(menu=menu_bar)


# Set form for Income
income_frame = ttk.Frame(root, padding=20)
close_button_income = create_close_button(income_frame, close)
ttk.Label(income_frame, text="Dodaj przychód").grid(row=0, column=0, columnspan=2, pady=30)
ttk.Label(income_frame, text="Nazwa").grid(row=1, column=0, pady=30, padx=5, sticky="w")
entry_income_name = ttk.Entry(income_frame)
entry_income_name.grid(row = 1, column = 1, pady=30, padx=5, sticky="e")
ttk.Label(income_frame, text="Wartość").grid(row=2, column=0, pady=30, padx=5, sticky="w")
entry_income_amount = ttk.Entry(income_frame)
entry_income_amount.grid(row = 2, column = 1, pady=30, padx=5, sticky="e")
ttk.Label(income_frame, text="Data").grid(row=3, column=0, pady=30, padx=5, sticky="w")
entry_income_date = ttk.DateEntry(income_frame, width=12)
entry_income_date.grid(row = 3, column = 1, pady=30, padx=5, sticky="w")
ttk.Button(income_frame, text="Submit", command=submit_income, style="info.Outline.TButton", padding=20).grid(row=4, column = 0, columnspan=2, pady=30)

# Set form for Expense
expense_frame = ttk.Frame(root)
close_button_expense = create_close_button(expense_frame, close)
ttk.Label(expense_frame, text="Dodaj wydatek").grid(row=0, column=0, columnspan=2, pady=30)
ttk.Label(expense_frame, text="Nazwa").grid(row=1, column=0, pady=30, padx=5, sticky="w")
entry_expense_name = ttk.Entry(expense_frame)
entry_expense_name.grid(row=1, column=1, pady=30, padx=5, sticky="w")
ttk.Label(expense_frame, text="Wartość").grid(row=2, column=0, pady=30, padx=5, sticky="w")
entry_expense_amount = ttk.Entry(expense_frame)
entry_expense_amount.grid(row=2, column=1, pady=30, padx=5, sticky="e")
ttk.Label(expense_frame, text="Data").grid(row=4, column=0, pady=30, padx=5, sticky="w")
entry_expense_date = ttk.DateEntry(expense_frame, width=15)
entry_expense_date.grid(row=4, column=1, pady=30, padx=5, sticky="e")
ttk.Label(expense_frame, text="Kategoria").grid(row=3, column=0, pady=30, padx=5, sticky="w")
category_var = StringVar()
categories = ttk.Combobox(expense_frame, textvariable=category_var, width= 17,state="readonly")
categories["values"] = ["Żywność", "Dom", "Transport", "Rozrywka", "Zdrowie", "Edukacja", "Zwierzęta", "Inne"]
categories.set("Wybierz")
categories.grid(row=3, column=1, pady=30, padx=5, sticky="e")

ttk.Button(expense_frame, text="Submit", command=submit_expense, style="info.Outline.TButton", padding=20).grid(row=5, column=0, columnspan=2, pady=30)

show_main()
root.mainloop()