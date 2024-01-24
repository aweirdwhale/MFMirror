import customtkinter as ctk
from tkinter import *
from PIL import ImageTk, Image, ImageDraw
import time
import numpy as np
from features import *

# from features.behaviour import Behaviour

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
# here, we get the thumbnail of the current song and display it as a circle rotating arround itself. We'll use a foo image for now

placeholder_image_path = "placeholder.jpg"

img = Image.open(placeholder_image_path).convert("RGB")

npImage=np.array(img)
h,w=img.size

# Create same size alpha layer with circle
alpha = Image.new('L', img.size,0)
draw = ImageDraw.Draw(alpha)
draw.pieslice([0,0,h,w],0,360,fill=255)

# Convert alpha Image to numpy array
npAlpha=np.array(alpha)

# Add alpha layer to RGB
npImage=np.dstack((npImage,npAlpha))

# Save with alpha
Image.fromarray(npImage).save('thumbnail.png')

# import the image, resize and place it
placeholder_image = Image.open("thumbnail.png")
placeholder_image = placeholder_image.resize((120, 120), Image.ANTIALIAS) 
image_with_circle = placeholder_image.copy()


# Create a canvas for the song thumbnail
thumbnail_canvas = ctk.CTkCanvas(width=120, height=120, bg="#000000", highlightthickness=0)
thumbnail_canvas.place(x=10, y=700, anchor="sw")


# Create an ImageDraw object
draw = ImageDraw.Draw(image_with_circle)

# Calculate the center of the image
center_x = image_with_circle.width // 2
center_y = image_with_circle.height // 2

# Define the radius of the circle (adjust as needed)
circle_radius = 20
hole_radius = 10
border_radius = 40

# Draw a white circle at the center
draw.ellipse((center_x - circle_radius, center_y - circle_radius, center_x + circle_radius, center_y + circle_radius), fill="white")
draw.ellipse((center_x - hole_radius, center_y - hole_radius, center_x + hole_radius, center_y + hole_radius), fill="black")
draw.ellipse((center_x - border_radius, center_y - border_radius, center_x + border_radius, center_y + border_radius), outline="white", width=2)

# Convert the modified image to PhotoImage
placeholder_image_with_circle = ImageTk.PhotoImage(image_with_circle)

# Create a label to display the image with the circle
placeholder_image_label = ctk.CTkLabel(app, text="", image=placeholder_image_with_circle, bg_color="#000000")

# Place it bottom left
placeholder_image_label.place(x=10, y=700, anchor="sw")


"""Wish"""
# Hello babe <3


"""Start the app"""
app.mainloop()
