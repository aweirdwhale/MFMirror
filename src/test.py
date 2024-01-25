import customtkinter as ctk
from tkinter import *
from PIL import ImageTk, Image, ImageDraw
import time
import numpy as np
import threading

ctk.FontManager.load_font("fonts/Pilowlava.ttf")
ctk.FontManager.load_font("fonts/Subjectivity.ttf")

from features.behaviour import Behaviour

class Clock:
    def __init__(self, label, window):
        self.label = label
        self.window = window
        self.change_label()

    def change_label(self):
        current_time = time.strftime('%H\n%M')
        self.label.configure(text=current_time)
        self.window.after(1000, self.change_label)

class SpinningImage:
    def __init__(self, canvas, image_path):
        self.canvas = canvas
        self.image = Image.open(image_path).convert("RGBA")
        self.image = self.image.resize((80, 80), Image.ANTIALIAS)
        self.angle = 0
        self.image_with_circle = self.image.copy()
        self.center_x = self.image_with_circle.width // 2
        self.center_y = self.image_with_circle.height // 2
        self.circle_radius = 20
        self.hole_radius = 10
        self.border_radius = 40
        self.image_label = None
        self.spin_image()

    def spin_image(self):
        rotated_image = self.image.rotate(self.angle)
        rotated_image_with_circle = self.draw_circle(rotated_image)
        self.display_image(rotated_image_with_circle)
        self.angle -= 5
        self.canvas.after(50, self.spin_image)

    def draw_circle(self, image):
        draw = ImageDraw.Draw(image)
        draw.ellipse((self.center_x - self.circle_radius, self.center_y - self.circle_radius, self.center_x + self.circle_radius, self.center_y + self.circle_radius), fill="white")
        draw.ellipse((self.center_x - self.hole_radius, self.center_y - self.hole_radius, self.center_x + self.hole_radius, self.center_y + self.hole_radius), fill="black")
        draw.ellipse((self.center_x - self.border_radius, self.center_y - self.border_radius, self.center_x + self.border_radius, self.center_y + self.border_radius), outline="white", width=2)

        return image

    def display_image(self, image):
        image_tk = ImageTk.PhotoImage(image)
        if self.image_label:
            self.canvas.delete(self.image_label)
        self.image_label = self.canvas.create_image(self.center_x, self.center_y, image=image_tk)
        self.canvas.image = image_tk

class UserInterface(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.behaviour = Behaviour()
        self.lock = lock

    def run(self):
        self.app = ctk.CTk()
        self.app.title("Mother F Mirror")
        self.app.geometry("960x720")
        self.app.resizable(False, False)
        self.app.config(bg="#000000")
        # Clock widget
        watch_canvas = ctk.CTkCanvas(self.app, width=120, height=120, bg="#000000", highlightthickness=0)
        watch_canvas.place(x=940, y=12, anchor="ne")

        clk = ctk.CTkLabel(self.app, text="", font=("Subjectivity", 42), bg_color="#000000", text_color="#ffffff")
        clk.place(x=940, y=20, anchor="ne")
        clock = Clock(clk, self.app)

        # Musica !
        """round the image"""
        placeholder_image_path = "placeholder.jpg"

        img = Image.open(placeholder_image_path).convert("RGB")

        npImage = np.array(img)
        h, w = img.size

        # Create same size alpha layer with circle
        alpha = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0, 0, h, w], 0, 360, fill=255)

        # Convert alpha Image to numpy array
        npAlpha = np.array(alpha)

        # Add alpha layer to RGB
        npImage = np.dstack((npImage, npAlpha))

        # Save with alpha
        Image.fromarray(npImage).save('thumbnail.png')

        # place the image
        thumbnail_canvas = ctk.CTkCanvas(self.app, width=80, height=80, bg="#000000", highlightthickness=0)
        thumbnail_canvas.place(x=20, y=700, anchor="sw")

        spinning_image = SpinningImage(thumbnail_canvas, "thumbnail.png")

        # Name of the song
        song_name = ctk.CTkLabel(self.app, text=f"Song name", font=ctk.CTkFont("Subjectivity", 24), bg_color="#000000", text_color="#ffffff")
        song_name.place(x=125, y=655, anchor="sw")

        # Song artist
        # song_artist = ctk.CTkLabel(self.app, text=f"Song artist", font=ctk.CTkFont("Subjectivity", 16), bg_color="#000000", text_color="#ffffff")
        # song_artist.place(x=125, y=685, anchor="sw")

        # Song duration
        song_duration_label = ctk.CTkLabel(self.app, text="00:00", font=ctk.CTkFont("Subjectivity", 16), bg_color="#000000", text_color="#ffffff")
        song_duration_label.place(x=125, y=685, anchor="sw")
        self.update_song_duration_label(song_duration_label)

        # Progress bar
        progress_bar = ctk.CTkProgressBar(self.app, width=250, height=6, bg_color="#000000", border_color="#FFFFFF", border_width=1, progress_color="#ffffff", fg_color="#000000")
        progress_bar.set(0)
        progress_bar.place(x=125, y=700, anchor="sw")
        self.progress_bar_behaviour(progress_bar)

        self.app.mainloop()

    def update_song_duration_label(self, label):
        duration_text = f"{self.behaviour.audio_position}/{self.behaviour.audio_length_str}"
        label.configure(text=duration_text)
        self.app.after(1000, lambda: self.update_song_duration_label(label))

    def progress_bar_behaviour(self, progress_bar):
        self.progress = self.behaviour.progress_value
        progress_bar.set(self.progress)
        self.app.after(1000, lambda: self.progress_bar_behaviour(progress_bar))


    def start_behaviour(self):
        self.behaviour.use()

lock = threading.Lock()
# Lancer l'application en tant que thread
ui = UserInterface(lock)
ui.start()

with lock:
    ui.start_behaviour()

# Attendre que le thread de l'application se termine (optionnel)
ui.join()
