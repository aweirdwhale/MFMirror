"""
Interface to show when the weather is being updated
"""

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

ctk.FontManager.load_font("fonts/Pilowlava.ttf")
ctk.FontManager.load_font("fonts/Subjectivity.ttf")

# pass this UI inside a thread to update the weather
import tkinter as tk
import threading
import time

from weather_codes import Converter
from weather import Weather

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

        # Create a label top center
        self.label = ctk.CTkLabel(self.frame, text=f"{place}", font=("Pilowlava", 40), bg_color="#000000", fg_color="#000000")
        self.label.pack(pady=20)
        # Another just below it
        self.label2 = ctk.CTkLabel(self.frame, text=f"{lon}°N, {lat}°E", font=("Subjectivity", 16), bg_color="#000000", fg_color="#000000")
        self.label2.pack(pady=0)
        self.label2.place(relx=0.5, rely=0.12, anchor="center")
        
        
        # Create a canvas to show the weather image
        self.canvas = tk.Canvas(self.frame, width=100, height=100, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.place(relx=0.01, rely=0, anchor="nw")
        self.img = Image.open(self.image_path)
        self.img = self.img.resize((72, 72), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(50, 50, image=self.img)


        
        # Create a label to show the weather
        self.label3 = ctk.CTkLabel(self.frame, text=self.c.convert(), font=("Subjectivity", 15), bg_color="#000000", fg_color="#000000")
        self.label3.pack(pady=20)
        self.label3.place(relx=0.015, rely=0.15, anchor="nw")


        # CONTENT AT THE MIDDLE OF THE SCREEN
        # temperature (+L & H)
        self.temperature = self.w["current"]["temp"]
        self.tempH = self.w["daily"]["temp_max"]
        self.tempL = self.w["daily"]["temp_min"]

        # make a white circle-shaped canvas to show the temperature
        self.tempCanvas = tk.Canvas(self.frame, width=120, height=120, bg="#000000", highlightthickness=0)
        self.tempCanvas.pack(pady=20)
        self.tempCanvas.place(relx=0.42, rely=0.35, anchor="center")
        self.tempCanvas.create_oval(0, 0, 120, 120, fill="#FFFFFF")


        # write the temperature in the middle of the circle
        self.tempCanvas.create_text(60, 53, text=f"{self.temperature}°C", font=("Subjectivity", 35), fill="#000000")
        self.tempCanvas.create_text(60, 83, text=f"H:{self.tempH}°C L:{self.tempL}°C", font=("Subjectivity", 12), fill="#000000")

        #body feeling
        self.bfeeling = self.w["current"]["body_feeling"]

        # make a white circle-shaped canvas to show the temperature
        self.bodyfeelingCanvas = tk.Canvas(self.frame, width=120, height=120, bg="#000000", highlightthickness=0)
        self.bodyfeelingCanvas.pack(pady=20)
        self.bodyfeelingCanvas.place(relx=0.58, rely=0.35, anchor="center")
        self.bodyfeelingCanvas.create_oval(0, 0, 120, 120, fill="#FFFFFF")


        # write the temperature in the middle of the circle
        self.bodyfeelingCanvas.create_text(60, 45, text=f"Body Feeling", font=("Subjectivity", 10), fill="#000000")
        self.bodyfeelingCanvas.create_text(60, 75, text=f"{self.bfeeling}°C", font=("Subjectivity", 35), fill="#000000")








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
    