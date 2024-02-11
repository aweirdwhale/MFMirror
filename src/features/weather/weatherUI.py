"""
Interface to show when the weather is being updated
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import os

ctk.FontManager.load_font("fonts/Pilowlava.ttf")
ctk.FontManager.load_font("fonts/Subjectivity.ttf")

# pass this UI inside a thread to update the weather
import tkinter as tk
import threading
import time

import dotenv
dotenv.load_dotenv(dotenv_path="config.env")

place = os.getenv("PLACE")
lon = os.getenv("LON")
lat = os.getenv("LAT")

# pass content as a widget
class Content:
    def __init__(self, parent):
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
        # Add the weather image top left
        self.weather_image = Image.open("assets/weather.png")
        self.weather_image = self.weather_image.resize((100, 100))
        self.weather_image = ImageTk.PhotoImage(self.weather_image)
        self.weather_label = ctk.CTkLabel(self.frame, image=self.weather_image, bg_color="#000000")
        self.weather_label.pack(pady=20, padx=20, side="left")
        # Add the weather text below the image
        self.weather_text = ctk.CTkLabel(self.frame, text="Light Rain", font=("Pilowlava", 20), bg_color="#000000", fg_color="#000000")
        self.weather_text.pack(pady=20, side="left")
        




        self.frame.update()
    
    def destroy(self):
        self.frame.destroy()
    
    def update(self, text):
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
    