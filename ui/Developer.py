#!/usr/bin/env python3

# GUI related
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from io import BytesIO

# OS related
import time

# distant classes
from scripts.face_recon.facerecognition import FaceRecognition
from scripts.music.musicbehaviour import MusicBehaviour

# APIs
import requests

recognized = "No recognized faces yet"
"""Creds"""
key = "AIzaSyA3mZLqwIAFmIast90AD3LYc0kxHFMh4qs"

"""Defines Actions for the window"""


class Actions():
    def __init__(self, window, cameraIndex, key):
        self.mbehaviour = MusicBehaviour(window, key)  # musicBehaviour class
        self.fbehaviour = FaceRecognition(cameraIndex)  # Behaviour class

    # Music related actions
    def search(self, entry, label, imageLabel):
        if entry.get() == "":
            return

        result = self.mbehaviour.search_video(str(entry.get()))
        title = result[0]["title"]
        author = result[0]["artist"]
        thumbnail = result[0]["thumbnail"]

        thumbnail = Image.open(BytesIO(requests.get(thumbnail).content))
        thumbnail.resize((100, 75), Image.ANTIALIAS)
        thumbnail = ImageTk.PhotoImage(thumbnail)

        label.config(text=f"{title} by {author}")
        imageLabel.config(image=thumbnail)
        imageLabel.image = thumbnail

    def play(self):
        self.mbehaviour.play()

    def pause(self):
        self.mbehaviour.pause_resume()

    # face recon related actions
    def test(self):
        recognized = self.fbehaviour.recognition()  # calls the start method from Behaviour class and store returned values

        if recognized == False:
            t3 = Label(window, text=f"No recognized faces yet", font=('Montserrat'), bg='#222222', fg='#f00', padx=20)
            t3.place(x=150, y=150, anchor=NW)

        else:
            t3 = Label(window, text=f"Detected : {recognized[0]}, at {recognized[1]}%", font=('Montserrat'),
                       bg='#222222', fg='#0F0', padx=20)
            t3.place(x=150, y=150, anchor=NW)

    def implement(self, username):
        if username != "":
            self.fbehaviour.implement_dataset(str(username))
        else:
            print('You must give your username in order to implement the dataset.')

    def extract(self):
        self.fbehaviour.extract()

    def train(self):
        self.fbehaviour.train()


"""define window properties"""

window = Tk()  # creates a new window
window.geometry("1480x720")  # defines width x height
window.title("Developer Window For MFM")  # sets window title
window.configure(background="#222222")  # sets background color

"""Make an Instance for action class"""
action = Actions(window, 0, key)

"""Define window widgets"""


class Clock:
    def __init__(self):
        self.time1 = ''
        self.time2 = time.strftime('%H:%M:%S')
        self.mFrame = Frame(bg='#f00')
        self.mFrame.config(width=100)
        self.mFrame.pack(side=TOP, expand=False, anchor=NW, padx=20)

        self.watch = Label(self.mFrame, text=self.time2, font=('Montserrat', 12, 'bold'))
        self.watch.pack()

        self.changeLabel()  # first call it manually

    def changeLabel(self):
        self.time2 = time.strftime('%H:%M:%S')
        self.watch.configure(text=self.time2, bg='#222222', fg='#fff')
        self.mFrame.after(200, self.changeLabel)  # it'll call itself continuously


class ISS:
    def __init__(self):
        self.response = requests.get("http://api.open-notify.org/iss-now.json")
        self.lat = self.response.json()["iss_position"]["latitude"]
        self.lon = self.response.json()["iss_position"]["longitude"]

        self.pays = requests.get(
            f"http://api.geonames.org/countryCodeJSON?lat={self.lat}&lng={self.lon}&username=Aweirdwhale")
        if "countryName" in self.pays.json():
            self.pays = self.pays.json()["countryName"]
            print(self.pays)
        else:
            self.pays = "ocean"

        self.iFrame = Frame(bg='#222')
        self.iFrame.config(width=100)
        self.iFrame.pack(side=TOP, expand=False, anchor=NW, padx=20)

        self.pos = Label(self.iFrame, text=f"Current ISS position : {self.lat}, {self.lon} (Over {self.pays})", font=('Montserrat', 12),
                         bg='#222222', fg='#fff')
        self.pos.pack()

        self.btn = ttk.Button(window, text=f"Update ISS", command=self.changeLabel)
        self.btn.place(x=500, y=260, anchor=NW)

    def changeLabel(self):
        self.response = requests.get("http://api.open-notify.org/iss-now.json")
        self.lat = self.response.json()["iss_position"]["latitude"]
        self.lon = self.response.json()["iss_position"]["longitude"]

        self.pays = requests.get(
            f"http://api.geonames.org/countryCodeJSON?lat={self.lat}&lng={self.lon}&username=Aweirdwhale")
        if "countryName" in self.pays.json():
            self.pays = self.pays.json()["countryName"]
            self.pos.configure(text=f"Current ISS position : {self.lon}, {self.lat}. (Over {self.pays})", bg='#222222',
                               fg='#fff')
        else:
            self.pos.configure(text=f"Current ISS position : {self.lon}, {self.lat}. (Over ocean)", bg='#222222',
                               fg='#fff')


class Implementing:
    def __init__(self):
        # 'implement faces'
        self.t = Label(window, text="Implement faces : \r", font=('Montserrat'), bg='#222222', fg='#f00', padx=20,
                       pady=20)
        self.t.pack(side=TOP, anchor=NW)

        # Username input :
        self.i = Entry(window, width=42, bg='#222', fg='#fff')
        self.i.pack(side=TOP, anchor=NW, padx=20)

        # Implement button :
        self.btn = ttk.Button(window, text=f"Start implementing", command=lambda: action.implement(self.i.get()))
        self.btn.place(x=380, y=60, anchor=NW)
        # Manual extraction
        self.btn2 = ttk.Button(window, text=f"Manual extract", command=action.extract)
        self.btn2.place(x=520, y=60, anchor=NW)
        # Manual training.
        self.btn3 = ttk.Button(window, text=f"Manual training", command=action.train)
        self.btn3.place(x=632, y=60, anchor=NW)



class Music:
    def __init__(self):
        self.mFrame = Frame(bg='#222')
        self.mFrame.config(width=100)
        self.mFrame.pack(side=TOP, expand=False, anchor=NW, padx=20, pady=20)

        self.sb = Entry(self.mFrame, width=42, bg='#222', fg='#fff')
        self.sb.pack()

        # # Infos sur la recherche
        self.fnd = Label(self.mFrame, text=f"", font=('Montserrat', 12), bg='#222222', fg='#fff')
        self.fnd.pack()

        self.fnd_img = Label(self.mFrame, bg="#222")
        self.fnd_img.pack()

        # Ajoutez des éléments d'interface utilisateur
        self.play_button = Button(self.mFrame, text="Lire la musique", command=action.play)
        self.play_button.pack()

        self.pause_button = Button(self.mFrame, text="Pause/Reprendre la musique", command=action.pause)
        self.pause_button.pack()

        self.btn = ttk.Button(window, text=f"Search", command=lambda: action.search(self.sb, self.fnd, self.fnd_img))
        self.btn.place(x=500, y=305, anchor=NW)

        # activer la modification de volume
        self.vbtn = ttk.Button(window, text=f"Volume", command=lambda: action.vol())
        self.vbtn.place(x=500, y=335)

    def changeLabel(self):
        pass


"""define window content"""
implementing = Implementing()

# 'Test'
t2 = Label(window, text="Test : \r", font=('Montserrat'), bg='#222222', fg='#f00', padx=20, pady=20)
t2.pack(side=TOP, anchor=NW)

# Test Button
btn2 = ttk.Button(window, text="Start recognition", command=lambda: action.test())
btn2.pack(side=TOP, anchor=NW, padx=20)

# Test Output
t3 = Label(window, text=f"Output", font=('Montserrat'), bg='#222222', fg='#fff', padx=20)
t3.place(x=150, y=150, anchor=NW)

# 'Fonctionnalités'
t2 = Label(window, text="Fonctionnalités : \r", font=('Montserrat'), bg='#222222', fg='#f00', padx=20, pady=20)
t2.pack(side=TOP, anchor=NW)

clock_widget = Clock()
iss_widget = ISS()
music_widget = Music()

"""Starts the window"""
window.mainloop()


