"""
Interface to show when the weather is being updated
"""

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
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
        self.w = Weather()
        self.code = self.w.refresh()["current"]["code"]

        self.c = Converter(self.code)
        self.description = self.c.convert()
        # self.image_path = self.c.get_images_path()

        self.parent = parent
        # make a frame that takes the whole window
        self.frame = ctk.CTkFrame(self.parent, bg_color="#000000")
        self.frame.pack(fill="both", expand=True)

        # Create a label top center
        self.label = ctk.CTkLabel(self.frame, text=f"{place}", font=("Pilowlava", 40), bg_color="#000000", fg_color="#000000")
        self.label.pack(pady=20)
        # Another just below it
        self.label2 = ctk.CTkLabel(self.frame, text=f"{lon}°N, {lat}°E", font=("Subjectivity", 16), bg_color="#000000", fg_color="#000000")
        self.label2.pack(pady=0)
        self.label2.place(relx=0.5, rely=0.12, anchor="center")
        
        
        # Create a canvas to show the weather image
        # self.canvas = tk.Canvas(self.frame, width=200, height=200, bg="#000000", highlightthickness=0)
        # self.canvas.pack(pady=20)
        # self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        # self.img = Image.open(self.image_path)
        # self.img = self.img.resize((72, 72), Image.ANTIALIAS)
        # self.img = ImageTk.PhotoImage(self.img)
        # self.canvas.create_image(0, 0, anchor="nw", image=self.img)


        
        # Create a label to show the weather
        self.label3 = ctk.CTkLabel(self.frame, text=self.c.convert(), font=("Subjectivity", 10), bg_color="#000000", fg_color="#000000")
        self.label3.pack(pady=20)
        self.label3.place(relx=0.01, rely=0.2, anchor="nw")




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
        self.app.title("Mother F* Mirror - Weather")
        self.app.geometry("960x720")
        self.app.resizable(False, False)
        self.app.config(bg="#000000")

        self.content = Content(self.app)

        self.app.mainloop()

if __name__ == "__main__":
    w = WeatherUI()
    w.start()
    