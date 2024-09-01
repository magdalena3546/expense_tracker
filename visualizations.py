import tkinter as Tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_donut_chart(frame, total_expenses, total_income):

    if total_income == 0 and total_expenses == 0:
        return
    sizes = [total_income, total_expenses]
    colors = ["#4CAF50", "#FF5733"]
    explode = (0, 0.1)
    
    fig, ax = plt.subplots(figsize=(1.2, 1.2), facecolor="#2c3e50" )

    wedges, texts, autotexts = ax.pie(sizes, colors=colors, explode=explode, autopct = "%1.1f%%", startangle = 140, pctdistance = .85, textprops={'fontsize': 8})

    # centre_circle = plt.Circle((0,0), .70, fc="white")
    # fig.gca().add_artist(centre_circle)

    for text in autotexts:
        text.set_color("white")

    ax.axis("equal")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")