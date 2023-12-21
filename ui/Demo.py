#!/usr/bin/env python3

from tkinter import Canvas, Frame, Label

import customtkinter as tk
import threading
import time

from scripts.face_recon.facerecognition import FaceRecognition


class Clock:
    def __init__(self, label):
        self.label = label
        self.change_label()

    def change_label(self):
        current_time = time.strftime('%H\r%M')
        self.label.configure(text=current_time)
        app.after(60 * 1000, self.change_label)  # Met à jour toutes les secondes


class Username:
    def __init__(self, label):
        self.label = label
        self.username = ''
        self.initialize_username()

    def initialize_username(self):
        recon = FaceRecognition(2)
        self.username = recon.recognition()[0]
        self.label.configure(text=f"Bonjour,\r   {self.username}")


def start_app():
    global app
    app = tk.CTk()
    app.title("MFMirror Demo")
    app.geometry("960x720")
    app.resizable(False, False)
    # Black bg
    app.config(bg="#000000")

    wish_label = tk.CTkLabel(app, text="Bonjour,\r   ", font=("Playfair Display", 48), bg_color="#000000")
    wish_label.place(x=20, y=0, anchor="nw")  # Place the label in the top left corner of the window

    username_label = Username(wish_label)

    watch_label = tk.CTkLabel(app, text=f"", font=("Montserrat", 42), bg_color="#000000")
    watch_label.place(x=920, y=22, anchor="ne")  # place the label in the top right corner of the window
    clock = Clock(watch_label)

    music_title_label = tk.CTkLabel(app, text="Music title", font=('Montserrat', 32), bg_color="#000000")
    music_title_label.place(x=200, y=650, anchor="sw")  # place the label bottom left

    music_artist_label = tk.CTkLabel(app, text="artist", font=('Montserrat', 24), bg_color="#000000",
                                     text_color="#d3d3d3")
    music_artist_label.place(x=200, y=680, anchor="sw")  # place the label bottom left

    app.mainloop()


if __name__ == "__main__":
    start_app()
