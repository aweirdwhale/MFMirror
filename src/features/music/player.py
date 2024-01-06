import os

import cv2
import pygame
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube

from src.features.Logs.log import Log

from dotenv import load_dotenv

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from io import BytesIO
import requests

import mediapipe as mp
import threading

from hand_gesture import HandGesture

import math
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

load_dotenv(dotenv_path="../../../.env.secret")
key = os.getenv("GOOGLE_KEY")

# init log
log = Log()


class Player:
    def __init__(self, window=None):
        self.video_info = None
        self.result = []
        self.save_path = '../../../DATA/musics'
        self.window = window

        self.pygame_instance = None
        self.music_file = None
        self.paused = False
        self.current_position = 0

        self.volume_thread_stop_event = threading.Event()

    def use_youtube(self, query, yt_key):
        youtube = build("youtube", "v3", developerKey=yt_key)
        try:
            log.log('Searching...', 'info')
            crawl = youtube.search().list(
                q=query,
                type="video",
                part="id, snippet",
                maxResults=1
            ).execute()

            for search_result in crawl.get("items", []):
                video_id = search_result["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                artist = search_result["snippet"]["channelTitle"]
                title = search_result["snippet"]["title"]
                thumbnail = search_result["snippet"]["thumbnails"]["medium"]["url"]

                self.video_info = {
                    "url": video_url,
                    "artist": artist,
                    "title": title,
                    "thumbnail": thumbnail,
                    "id": str(video_id)
                }

                self.result = []
                self.result.append(self.video_info)

            log.log(f"Found {self.result[0]['title']}.", 'nice')
            return self.result

        except HttpError as e:
            error = f"An error occurred while trying to fetch data from youtube: {e}"
            log.log(error, 'error')
            return error

    def download(self):
        log.log("Downloading . . .", "info")

        if len(self.result) > 0:
            yt_url = self.result[0]["url"]
            file_name = self.result[0]["id"]

            if os.path.isfile(f"{self.save_path}/{file_name}.mp3"):
                log.log("File ready to play.", "great")

            else:
                yt = YouTube(yt_url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                generic_filename = f"{file_name}.mp4"
                audio_stream.download(self.save_path, filename=generic_filename)

                log.log("Converting . . .", "info")

                video_clip = AudioFileClip(f"{self.save_path}/{file_name}.mp4")
                video_clip.write_audiofile(f"{self.save_path}/{file_name}.mp3")
                video_clip.close()
                os.remove(f"{self.save_path}/{file_name}.mp4")

                log.log("File downloaded and ready to play.", "great")
        else:
            log.log("404 Music not found.", "fail")
            return False

    def play(self):
        file_name = self.result[0]["id"]
        self.download()

        if self.pygame_instance is None:
            self.pygame_instance = pygame.init()

        self.music_file = f"{self.save_path}/{file_name}.mp3"
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play()
        log.log("Playing . . .", "success")
        self.paused = False

        if self.window is not None:
            self.window.after(100, self.check_music_status)

    def check_music_status(self):
        if pygame.mixer.music.get_busy():
            self.window.after(100, self.check_music_status)
        elif not self.paused:
            pygame.quit()

    def pause_resume(self):

        if pygame.mixer.music.get_busy() and not self.paused:
            self.current_position = pygame.mixer.music.get_pos()
            pygame.mixer.music.pause()
            self.paused = True
        elif self.paused:
            pygame.mixer.music.play(start=float(self.current_position / 1000))
            self.paused = False

    def volume(self):
        hg = HandGesture()  # instance
        hg.start()  # start thread
        hg.join()  # wait for thread to finish


# Test
if __name__ == '__main__':
    class Actions:
        def __init__(self):
            self.behaviour = Player(root)

        def search(self):
            result = self.behaviour.use_youtube(str(sb.get()), key)
            title = result[0]["title"]
            author = result[0]["artist"]
            thumbnail = result[0]["thumbnail"]
            thumbnail = ImageTk.PhotoImage(Image.open(BytesIO(requests.get(thumbnail).content)))

            fnd.config(text=f"{title} by {author}")
            fnd_img.config(image=thumbnail)
            fnd_img.image = thumbnail

        def play(self):
            self.behaviour.play()

        def pause(self):
            self.behaviour.pause_resume()

        def volume(self):
            self.behaviour.volume()


    # Create the main window
    root = tk.Tk()
    root.title("YouTube Music Player")
    root.geometry("1000x500")

    actions = Actions()

    # SearchBar
    sb = tk.Entry(root, width=42, bg='#222', fg='#fff')
    sb.pack()

    sbtn = tk.Button(root, text="Rechercher", command=actions.search)
    sbtn.pack()

    # Search result info
    fnd = ttk.Label(root, text=f" ", font='Montserrat')
    fnd.pack()

    fnd_img = ttk.Label(root)
    fnd_img.pack()

    # Add GUI elements
    play_button = tk.Button(root, text="Lire la musique", command=actions.play)
    play_button.pack()

    progress = ttk.Label(root)
    progress.pack()

    pause_button = tk.Button(root, text="Pause/Reprendre la musique", command=actions.pause)
    pause_button.pack()

    volume = tk.Button(root, text="volume", command=actions.volume)
    volume.pack()

    # Start the main GUI loop
    root.mainloop()