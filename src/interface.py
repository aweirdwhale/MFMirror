import customtkinter as ctk
from tkinter import *

import time
from features import *

from features.behaviour import Behaviour

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
# create a canvas around the watch
watch_canvas = ctk.CTkCanvas(app, width=120, height=120, bg="#000000", highlightthickness=0)
watch_canvas.place(x=950, y=12, anchor="ne")  # place the canvas in the top right corner of the window

# create a circle on the canvas
# watch_canvas.create_oval(0, 0, 117, 117, fill="#000000", outline="#FFFFFF", width=2)  # ==> idk

clk = ctk.CTkLabel(app, text=f"", font=("Montserrat", 42), bg_color="#000000", text_color="#ffffff")
clk.place(x=918, y=20, anchor="ne")
clock = Clock(clk, app)

# Musiqua ! 
# create a circle on the bottom left corner of the window
music_canvas = ctk.CTkCanvas(app, width=180, height=180, bg="#ff0000", highlightthickness=0)
music_canvas.place(x=20, y=700, anchor="sw")

# create a circle on the canvas
music_canvas.create_oval(30, 30, 150, 150, fill="", outline="black", width=20)




"""Wish"""
# Hello babe <3


"""Start the app"""
app.mainloop()
