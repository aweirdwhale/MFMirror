import customtkinter as ctk

import time
from features import *


class Clock:
    def __init__(self, label, window):
        self.label = label
        self.window = window
        self.change_label()

    def change_label(self):
        current_time = time.strftime('%H\r%M')
        self.label.configure(text=current_time)
        self.window.after(1000, self.change_label)  # Met à jour toutes les secondes


app = ctk.CTk()
app.title("Mother F Mirror")
app.geometry("960x720")
app.resizable(False, False)
# Black bg
app.config(bg="#000000")


"""Clock widget"""
clk = ctk.CTkLabel(app, text=f"", font=("Montserrat", 42), bg_color="#000000")
clk.place(x=920, y=22, anchor="ne")
clock = Clock(clk, app)

""""""
app.mainloop()
