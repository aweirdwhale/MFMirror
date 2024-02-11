import customtkinter as ctk
from tkinter import *
from PIL import ImageTk, Image, ImageDraw
import time
import numpy as np
import threading
import requests
from io import BytesIO
import os

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
        width, height = self.image.size

        # Choisissez la dimension minimale pour le redimensionnement
        min_dimension = min(width, height)

        # Calculez les coordonnées du rectangle de recadrage centré
        left = (width - min_dimension) // 2
        top = (height - min_dimension) // 2
        right = (width + min_dimension) // 2
        bottom = (height + min_dimension) // 2

        # Effectuez le recadrage
        self.image = self.image.crop((left, top, right, bottom))

        # Redimensionnez ensuite l'image à la taille souhaitée
        self.image = self.image.resize((80, 80), Image.ANTIALIAS)
        self.image_with_circle = self.image.copy()
        self.center_x = self.image_with_circle.width // 2
        self.center_y = self.image_with_circle.height // 2
        self.angle = 0
        self.circle_radius = 20
        self.hole_radius = 10
        self.border_radius = 40
        self.image_label = None
        self.image_tk = None  # Ajout de cette ligne
        self.spin_image()

    def spin_image(self):
        rotated_image = self.image.rotate(self.angle)
        rotated_image_with_circle = self.draw_circle(rotated_image)
        self.display_image(rotated_image_with_circle)
        self.angle -= 4
        self.canvas.after(50, self.spin_image)

    def draw_circle(self, image):
        draw = ImageDraw.Draw(image)
        draw.ellipse((self.center_x - self.circle_radius, self.center_y - self.circle_radius, self.center_x + self.circle_radius, self.center_y + self.circle_radius), fill="white")
        draw.ellipse((self.center_x - self.hole_radius, self.center_y - self.hole_radius, self.center_x + self.hole_radius, self.center_y + self.hole_radius), fill="black")
        draw.ellipse((self.center_x - self.border_radius, self.center_y - self.border_radius, self.center_x + self.border_radius, self.center_y + self.border_radius), outline="white", width=2)
        return image

    def display_image(self, image):
        if self.image_tk:
            self.canvas.delete(self.image_tk)
        image_tk = ImageTk.PhotoImage(image)
        self.image_tk = image_tk  # Mettez à jour la même instance
        self.image_label = self.canvas.create_image(self.center_x, self.center_y, image=image_tk)
        self.canvas.image = image_tk

    def clear(self):
        self.canvas.delete(self.image_label)

class IndicatorDot:
    def __init__(self, canvas):
        self.canvas = canvas
        self.dot = None
        self.color = "orange"
        self.draw_dot()

    def draw_dot(self):
        self.clear()
        self.dot = self.canvas.create_oval(0, 0, 10, 10, fill=self.color)
        self.canvas.after(800, self.draw_dot)

    def clear(self):
        self.canvas.delete(self.dot)

    def update_color(self, new_color):
        self.color = new_color
        self.clear()
        self.draw_dot()


class wish:
    def __init__(self, label, meteo):
        self.label = label
        self.meteo = meteo
        self.label.configure(text="Bonjour, \n   Olivier")
        self.toMeteo()
    
    def toMeteo(self):
        self.label.configure(text=f'{self.meteo["current"]["temp"]}°C {self.meteo["current"]["code"]}')
        self.label.configure(font=ctk.CTkFont("Subjectivity", 24))
        self.label.after(10 * 1000, self.toWish)
    
    def toWish(self):
        self.label.configure(text="Bonjour, \n   Olivier")
        self.label.configure(font=ctk.CTkFont("Pilowlava", 24))
        self.label.after(4 * 1000, self.toMeteo)


class UserInterface(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.behaviour = Behaviour()
        self.lock = lock
        self.isPlaying = False
        self.updateThumbnail = False
        self.spinning_image = None
        self.thumbnail_image = None
        self.placeholder = "placeholder_.png"
        self.state = self.behaviour.state
        self.dot_color = "orange"  # Utilisez dot_color au lieu de state
        self.meteo = self.behaviour.meteo
        self.last_modification_time = None

        

    def run(self):
        self.app = ctk.CTk()
        self.app.title("Mother F* Mirror")
        self.app.geometry("960x720")
        self.app.resizable(False, False)
        self.app.config(bg="#000000")

        # Clock widget
        watch_canvas = ctk.CTkCanvas(self.app, width=120, height=120, bg="#000000", highlightthickness=0)
        watch_canvas.place(x=940, y=12, anchor="ne")

        clk = ctk.CTkLabel(self.app, text="", font=("Subjectivity", 42), bg_color="#000000", text_color="#ffffff")
        clk.place(x=940, y=20, anchor="ne")
        clock = Clock(clk, self.app)

        # self.behaviour.get_thumbnail()

        # place the image
        thumbnail_canvas = ctk.CTkCanvas(self.app, width=80, height=80, bg="#000000", highlightthickness=0)
        thumbnail_canvas.place(x=20, y=700, anchor="sw")

        #self.update_thumbnail(thumbnail_canvas=thumbnail_canvas)
        self.last_modification_time = os.path.getmtime("thumbnail.png")
        self.check_image_modification("thumbnail.png", thumbnail_canvas)

        # put a placeholder image
        self.thumbnail_image = ImageTk.PhotoImage(Image.open(self.placeholder).convert("RGBA"))
        thumbnail_canvas.create_image(0, 0, anchor="nw", image=self.thumbnail_image)
    
        # place the listener state indicator dot
        state_canvas = ctk.CTkCanvas(self.app, width=20, height=20, bg="#000000", highlightthickness=0)
        # place the dot at the top center
        state_canvas.place(x=480, y=20, anchor="n")

        # create the dot
        self.indicator_dot = IndicatorDot(state_canvas)
        self.update_state_indicator()

        """Top left corner"""
        # Wish the user
        wish_label = ctk.CTkLabel(self.app, text=f"Bonjour, \n  Olivier", font=ctk.CTkFont("Pilowlava", 24), bg_color="#000000", text_color="#ffffff")
        wish_label.place(x=20, y=20, anchor="nw")
        w = wish(wish_label, self.meteo)
        # Meteo
        # meteo_label = ctk.CTkLabel(self.app, text=f'{self.meteo["current"]["temp"]}°C {self.meteo["current"]["code"]}', font=ctk.CTkFont("Subjectivity", 24), bg_color="#000000", text_color="#ffffff")
        # meteo_label.place(x=20, y=20, anchor="nw")



        # Name of the song
        song_name = ctk.CTkLabel(self.app, text=f"Nothing is playing", font=ctk.CTkFont("Subjectivity", 24), bg_color="#000000", text_color="#ffffff")
        song_name.place(x=125, y=655, anchor="sw")

        # Song duration
        song_duration_label = ctk.CTkLabel(self.app, text="", font=ctk.CTkFont("Subjectivity", 16), bg_color="#000000", text_color="#ffffff")
        song_duration_label.place(x=125, y=685, anchor="sw")

        # Progress bar
        progress_bar = ctk.CTkProgressBar(self.app, width=250, height=6, bg_color="#000000", border_color="#FFFFFF", border_width=1, progress_color="#ffffff", fg_color="#000000")
        progress_bar.set(0)
        progress_bar.place(x=125, y=700, anchor="sw")

        # Mettez à jour les informations de la musique
        self.update_music_info(song_name, song_duration_label, progress_bar, thumbnail_canvas)

        self.app.mainloop()


    def update_state_indicator(self):
        new_state = self.behaviour.state
        if new_state == 0:
            new_color = "#b86721"
        elif new_state == 1:
            new_color = "#67b821"
        elif new_state == 2:
            new_color = "#2179b8"

        if new_color != self.dot_color:
            self.dot_color = new_color
            self.indicator_dot.update_color(new_color)

        # Planifier la prochaine mise à jour après un certain délai (par exemple, toutes les secondes)
        self.app.after(1000, self.update_state_indicator)

    def get_thumbnail(self):
        #delete the previous image
        os.remove("thumbnail.png")

        self.music_thumbnail = self.behaviour.music_thumbnail

        # Musica ! 
        """round the image"""
        # get the image from link
        _ = requests.get(self.music_thumbnail)
        _.raise_for_status()  # Check if request is successful

        img = Image.open(BytesIO(_.content)).convert("RGB")

        npImage = np.array(img)
        h, w = img.size

        # Create same size alpha layer with circle
        alpha = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(alpha)

        radius = w // 2
        center_x = h // 2
        center_y = w // 2

        # make a circle with radius = h/2 at the center of image
        draw.pieslice((center_x - radius, center_y - radius, center_x + radius, center_y + radius), 0, 360, fill=255, width=2)

        # Convert alpha Image to numpy array
        npAlpha = np.array(alpha)

        # Add alpha layer to RGB
        npImage = np.dstack((npImage, npAlpha))

        # Save with alpha
        Image.fromarray(npImage).save('thumbnail.png')



    #def update_thumbnail(self, thumbnail_canvas):
     #   self.updateThumbnail = False
        # delete the placeholder image from the canvas
      #  thumbnail_canvas.delete("all")
        #get new image
       # self.get_thumbnail()
        # place the new image
        #self.spinning_image = SpinningImage(thumbnail_canvas, "thumbnail.png")
        #self.updateThumbnail = False



    def check_image_modification(self, image_path, canvas):
        """
        Vérifie si une image a été modifiée en comparant les horodatages de modification.
        """
        try:
            # Récupérer l'horodatage de modification actuel de l'image
            current_modification_time = os.path.getmtime(image_path)

            # Si l'horodatage a changé depuis la dernière vérification
            if current_modification_time != self.last_modification_time:
                # Mettre à jour l'image
                if self.spinning_image:
                    print("cleared")
                    self.spinning_image.clear()
                    time.sleep(1)

                # Mettre à jour l'image existante
                self.spinning_image = SpinningImage(canvas, image_path)
                
                print("Image modifiée")

                # Mettre à jour l'horodatage de la dernière modification
                self.last_modification_time = current_modification_time
        except FileNotFoundError:
            print("Fichier introuvable :", image_path)

        # Planifier la prochaine vérification après un certain délai (par exemple, toutes les secondes)
        self.app.after(1000, lambda: self.check_image_modification(image_path, canvas=canvas))


    def update_music_info(self, song_name_label, song_duration_label, progress_bar, thumbnail_canvas):
        self.isPlaying = self.behaviour.isPlaying
        if self.isPlaying:
            
            # Mettez à jour les étiquettes et la barre de progression avec les informations de la musique
            song_name_label.configure(text=self.behaviour.music_title)
            self.thumnail_link = self.behaviour.music_thumbnail
            duration_text = f"{self.behaviour.audio_position_str}/{self.behaviour.audio_length_str}"
            song_duration_label.configure(text=duration_text)
            progress_bar.set(self.behaviour.progress_value)
            progress_bar.configure(bg_color="#000000", progress_color="#ffffff", fg_color="#000000", border_color="#ffffff")
        else:
            # Mettez à jour les étiquettes et la barre de progression avec les informations de la musique
            
            song_name_label.configure(text=f"")
            song_duration_label.configure(text="")
            progress_bar.configure(bg_color="#000000", progress_color="#000000", fg_color="#000000", border_color="#000000")

        # Répétez cette méthode toutes les secondes
        self.app.after(1000, lambda: self.update_music_info(song_name_label, song_duration_label, progress_bar, thumbnail_canvas))

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
