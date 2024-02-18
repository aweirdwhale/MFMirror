"""
Interface to show when the weather is being updated
"""

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
import os

ctk.FontManager.load_font("fonts/Pilowlava.ttf")
ctk.FontManager.load_font("fonts/Subjectivity.ttf")

# pass this UI inside a thread to update the weather
import tkinter as tk
import threading
import time

from weather_codes import Converter
from weather import Weather
from rounded_rect import drawRect

import dotenv
dotenv.load_dotenv(dotenv_path="config.env")

place = os.getenv("PLACE")
lon = os.getenv("LON")
lat = os.getenv("LAT")

# pass content as a widget
class Content:
    def __init__(self, parent):
        self.w = Weather().refresh()
        self.code = self.w["current"]["code"]

        self.c = Converter(self.code)
        self.description = self.c.convert()
        self.image_path = self.c.get_icon()

        self.parent = parent
        # make a frame that takes the whole window
        self.frame = ctk.CTkFrame(self.parent, bg_color="#000000", fg_color="#000000")
        self.frame.pack(fill="both", expand=True)

        # =============== TITLE =================
        # Create a label top center
        self.label = ctk.CTkLabel(self.frame, text=f"{place}", font=("Pilowlava", 40), bg_color="#000000", fg_color="#000000")
        self.label.pack(pady=20)
        # Another just below it
        self.label2 = ctk.CTkLabel(self.frame, text=f"{lon}°N, {lat}°E", font=("Subjectivity", 16), bg_color="#000000", fg_color="#000000")
        self.label2.pack(pady=0)
        self.label2.place(relx=0.5, rely=0.12, anchor="center")
        
        
        # =============== ICON + DESCRIPTION  =================
        # Create a canvas to show the weather image
        self.canvas = tk.Canvas(self.frame, width=100, height=100, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.place(relx=0.01, rely=0, anchor="nw")
        self.img = Image.open(self.image_path)
        self.img = self.img.resize((72, 72), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(50, 50, image=self.img)

        # Write the weather description on the canvas
        self.canvas.create_text(50, 90, text=self.c.convert(), font=("Subjectivity", 15), fill="white")


        # =============== WEATHER INFORMATIONS =================
        
        rectangle_width = 200
        rectangle_height = 100

        # Create a canvas
        self.canvas = tk.Canvas(self.frame, width=300, height=290, bg="black", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        # INFO BOX
        drawRect(self.canvas, 0, 0, 300, 290, 20, 8, "#FFFFFF")

        # TEMPERATURE
        # temperature circle 20px from bottom and left, 120px width and height
        self.canvas.create_oval(20, 150, 140, 270, fill="black")
        # temperature text at the middle, font : Pilowlava 20
        self.canvas.create_text(80, 200, text=f"{self.w['current']['temp']}°C", font=("Pilowlava", 20), fill="white")
        # High and low temperature text bellow the temperature text, font : Subjectivity 10
        self.canvas.create_text(80, 230, text=f"H: {self.w['daily']['temp_max']}°C, L: {self.w['daily']['temp_min']}", font=("Subjectivity", 10), fill="white")


        #BODY FEELING
        # body feeling circle 20px from bottom and right, 120px width and height
        self.canvas.create_oval(160, 150, 280, 270, fill="black")
        # body feeling temp at the middle, font : Pilowlava 20
        self.canvas.create_text(220, 220, text=f"{self.w['current']['body_feeling']}°C", font=("Pilowlava", 20), fill="white")
        # "body feeling" label over temp, font : Subjectivity 10
        self.canvas.create_text(220, 195, text="Body feeling", font=("Subjectivity", 10), fill="white")

        # TITLE
        # label for weather description at the middle, font : Subjectivity 20
        self.canvas.create_text(150, 25, text="Weather", font=("Subjectivity", 20), fill="black")

        # WEATHER ICON / DESCRIPTION
        # weather icon : mid left mid top, 72x72, reverse colors
        self.img2 = Image.open(self.image_path)
        self.img2 = ImageOps.invert(self.img2.convert("RGB"))
        self.img2 = self.img2.resize((72, 72), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        self.canvas.create_image(150, 85, image=self.img2)

        # weather description : mid right, bellow icon, font : Subjectivity 15
        self.canvas.create_text(150, 125, text=self.c.convert(), font=("Subjectivity", 15), fill="black")

        # ======================================================

        self.frame.update()
    
    def destroy(self):
        self.frame.destroy()
    
    def update(self, text):
        # get meteo infos by weather code
        self.label.config(text=text)
        self.frame.update()

class WeatherUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.app = ctk.CTk()
        self.app.title("Hermione (Mother F* Mirror - Weather)")
        self.app.geometry("960x720")
        self.app.resizable(False, False)
        self.app.config(background="#000000")

        self.content = Content(self.app)

        self.app.mainloop()

if __name__ == "__main__":
    w = WeatherUI()
    w.start()
    