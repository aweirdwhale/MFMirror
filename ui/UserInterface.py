import customtkinter as ctk


from scripts.time.time import Clock
from features.face_recon.facerecognition import FaceRecognition

"""Define the main window"""
win = ctk.CTk()
win.title("My Window")
win.geometry("960x720")
win.resizable(False, False)
win.config(bg="#000000")




class Username:
    def __init__(self, label):
        self.label = label
        self.username = ''
        self.initialize_username()

    def initialize_username(self):
        recon = FaceRecognition(2)
        self.username = recon.recognition()[0]
        self.label.configure(text=f"Bonjour,\r   {self.username}")


"""Define the widgets"""
wish_label = ctk.CTkLabel(win, text=f"Bonjour,\r   ", font=("Playfair Display", 48), bg_color="#000000")
wish_label.place(x=20, y=0, anchor="nw")  # Place the label in the top left corner of the window
wish = Username(wish_label)


# create a canvas around the watch
watch_canvas = ctk.CTkCanvas(win, width=120, height=120, bg="#000000", highlightthickness=0)
watch_canvas.place(x=950, y=12, anchor="ne")  # place the canvas in the top right corner of the window

# create a circle on the canvas
watch_canvas.create_oval(0, 0, 115, 115, fill="#000000", outline="#FFFFFF", width=2)
watch_label = ctk.CTkLabel(win, text=f"18\r12", font=("Montserrat", 40), bg_color="#000000")
watch_label.place(x=913, y=20, anchor="ne")  # place the label in the top right corner of the window
clock = Clock(watch_label)

music_title_label = ctk.CTkLabel(win, text="Music title", font=('Montserrat', 32), bg_color="#000000")
music_title_label.place(x=150, y=650, anchor="sw")  # place the label bottom left

music_artist_label = ctk.CTkLabel(win, text="artist", font=('Montserrat', 24), bg_color="#000000",
                                  text_color="#d3d3d3")
music_artist_label.place(x=150, y=680, anchor="sw")  # place the label bottom left

# create a canva to display the album cover
album_canvas = ctk.CTkCanvas(win, width=105, height=105, bg="#000000", highlightthickness=0)
album_canvas.place(x=20, y=700, anchor="sw")  # place the canvas bottom left

# create a circle on the canvas
album_canvas.create_oval(0, 0, 100, 100, fill="#000000", outline="#FFFFFF", width=2)

# create a smaller circle on the canvas
album_canvas.create_oval(70, 70, 30, 30, fill="#000000", outline="#FFFFFF", width=2)


"""Backend functions"""



"""Start the main loop"""
win.mainloop()
