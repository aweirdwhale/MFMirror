import os
import threading
import tkinter as tk
from io import BytesIO
from tkinter import ttk

import mediapipe as mp
import pygame
import requests
from PIL import ImageTk, Image
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from moviepy.editor import AudioFileClip
from pytube import YouTube

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

pygame_instance = None
music_file = None
paused = False
current_position = 0


class MusicBehaviour:
    def __init__(self, window, key):
        self.volume_thread_stop_event = threading.Event()
        self.key = key
        self.youtube = build("youtube", "v3", developerKey=self.key)
        self.video = []
        self.window = window
        self.save_path = './musics'

    def info(self, info, state):
        print(info, state)
        self.window.update_idletasks()

    def search_video(self, query):
        try:
            self.info('Searching...', 'info')
            search = self.youtube.search().list(
                q=query,
                type="video",
                part="id, snippet",
                maxResults=1
            ).execute()

            for search_result in search.get("items", []):
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
                self.video = []
                self.video.append(self.video_info)

            return self.video

        except HttpError as e:
            self.info(f"Une erreur s'est produite lors de la recherche : {e}", "warn")
            return None

    def download(self):
        self.info("[INFO] Téléchargement . . .", "info")

        if len(self.video) > 0:
            yt_url = self.video[0]["url"]
            file_name = self.video[0]["id"]

            if os.path.isfile(f"{self.save_path}/{file_name}.mp3"):
                self.info("[INFO] Le fichier existe déjà et est prêt à être lu", "success")
            else:
                yt = YouTube(yt_url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                generic_filename = f"{file_name}.mp4"
                audio_stream.download(self.save_path, filename=generic_filename)

                self.info("[INFO] Conversion...", "info")

                video_clip = AudioFileClip(f"{self.save_path}/{file_name}.mp4")
                video_clip.write_audiofile(f"{self.save_path}/{file_name}.mp3")
                video_clip.close()
                os.remove(f"{self.save_path}/{file_name}.mp4")
        else:
            self.info("Aucune musique n'a été trouvée, merci de faire une recherche au préalable.", "warn")
            return False

    def play(self):
        file_name = self.video[0]["id"]
        self.download()

        global pygame_instance, music_file, paused
        if pygame_instance is None:
            pygame_instance = pygame.init()

        music_file = f"{self.save_path}/{file_name}.mp3"
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        self.info("[INFO] Lecture...", "success")
        paused = False
        self.window.after(100, self.check_music_status)

    def pause_resume(self):
        global paused, current_position
        if pygame.mixer.music.get_busy() and not paused:
            current_position = pygame.mixer.music.get_pos()
            pygame.mixer.music.pause()
            paused = True
        elif paused:
            pygame.mixer.music.play(start=float(current_position / 1000))
            paused = False

    def check_music_status(self):
        global paused
        if pygame.mixer.music.get_busy():
            self.window.after(100, self.check_music_status)
        elif not paused:
            pygame.quit()




if __name__ == '__main__':
    class Actions:
        def __init__(self):
            self.behaviour = MusicBehaviour(root)

        def search(self):
            result = self.behaviour.search_video(str(sb.get()))
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

    # Start the main GUI loop
    root.mainloop()
