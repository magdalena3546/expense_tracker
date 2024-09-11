import tkinter as Tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db import get_expenses_by_category, get_expenses_by_time

# create pie chart 
def create_pie_chart(frame, total_expenses, total_income, title="", row=0, column=0, figsize=(1.2, 1.2)):

    if total_income == 0 and total_expenses == 0:
        return
    sizes = [total_income, total_expenses]
    colors = ["#4CAF50", "#FF5733"]
    explode = (0, 0.1)
    
    fig, ax = plt.subplots(figsize=figsize, facecolor="#2c3e50" )
    
    wedges, texts, autotexts = ax.pie(sizes, colors=colors, explode=explode, autopct = "%1.1f%%", startangle = 140, pctdistance = .85, textprops={'fontsize': 8})
    ax.set_title(title, color="white")
    for text in autotexts:
        text.set_color("white")

    ax.axis("equal")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=column, sticky="nsew")

#create bar chart for grouping expenses by category
def create_bar_chart_categories(frame):
    categories, values = get_expenses_by_category()
    fig, ax = plt.subplots(figsize=(4, 2), facecolor="#2c3e50" )
    ax.bar(categories, values, color=["#3498db", "#9b59b6", "#e74c3c", "#f1c40f", "#1abc9c"])
    ax.tick_params(axis="x", color="white", labelcolor="white")
    ax.tick_params(axis="y", color="white", labelcolor="white")
    ax.set_title("Wydatki według kategorii", color="white")
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('none')
    ax.set_facecolor("#2c3e50")
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

#create line chart for 
def create_line_chart_by_time(frame):
    dates, amounts = get_expenses_by_time()
    fig, ax = plt.subplots(figsize=(4, 2), facecolor="#2c3e50")
    ax.plot(dates, amounts, marker="o", color="#8e44ad")
    ax.set_facecolor("#2c3e50")
    ax.tick_params(axis="x", color="white", labelcolor="white")
    ax.tick_params(axis="y", color="white", labelcolor="white")
    ax.set_title("Wydatki w czasie", color="white")
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('none')
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
#create window with dashboard
def create_visualizations(root, total_expenses, total_income, total_monthly_expenses, total_monthly_income):
    dashboard_window = Tk.Toplevel(root)
    dashboard_window.title("Wizualizacje")
    # dashboard_window.geometry("1400x2000")
    dashboard_window.resizable(False, False)
    dashboard_window.columnconfigure((0, 1), weight=1)
    dashboard_window.rowconfigure((0, 1), weight=1)
    dashboard_window.iconbitmap("images/icon.ico")
    dashboard_frame = ttk.Frame(dashboard_window)
    dashboard_frame.grid(row=0, column=0, sticky="nsew", columnspan=2, padx=20, pady=20)

    create_pie_chart(dashboard_frame, total_expenses, total_income, title="Całkowity bilans", column=0, figsize=(2, 2))
    create_pie_chart(dashboard_frame, total_monthly_expenses, total_monthly_income, title="Bilans miesięczny",row=1, column=1, figsize=(2, 2))
    create_bar_chart_categories(dashboard_frame)
    create_line_chart_by_time(dashboard_frame)