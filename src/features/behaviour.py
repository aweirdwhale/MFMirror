import os
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
from features.Logs.log import Log
from features.iss_position.iss import ISS
from features.music.player import Player
from features.weather.weather import Weather
from features.textToSpeech.speech import TTS
from features.wish.wish import Wish
from features.speechToText.stt import SpeechToText
from features.face_recon.facerecognition import FaceRecognition
from features.wakeword.Wakey import PorcupineListener

import json
import playsound
import pygame
import threading

phrases = json.load(open("src/features/phrases.json", "r"))


log = Log()

load_dotenv(dotenv_path=".env.secret")
load_dotenv(dotenv_path="config.env")
language = os.getenv("LANGUAGE")
PiKEY = os.getenv("PORCUPINE_KEY")

class Behaviour():
    def __init__(self):
        self.wake_word = PorcupineListener(
            accessKey=PiKEY,
            keywordPath="src/features/wakeword/wake_fr.ppn",
            modelPath="src/features/wakeword/porcupine_fr.pv",
            outputPath="src/features/wakeword/output.wav"
        )
        self.stt = SpeechToText()
        self.tts = TTS(lang=language)
        self.wish = Wish(language, "Janick")
        self.weather = Weather()
        self.iss = ISS()
        self.player = Player()
        self.face = FaceRecognition(0)
        self.last_detection_time = None
        self.command = ""
        self.arg = ""
        self.isPlaying = False
        self.count = 0
        
        # UI
        self.audio_length = 0
        self.audio_position = 0
        self.audio_position_str = ""
        self.progress_value = 0
        self.audio_length_str = ""
        self.music_title = ""
        self.music_thumbnail = ""

        # Test
        self.test_command = "musique"
        self.test_arg = "Knockin' on heavens door"

    def listen(self):
        try:
            self.wake_word.initialize()
            self.wake_word.start_detection()
            self.use()
        except KeyboardInterrupt:
            print("Ctrl+C detected. Stopping...")
        finally:
            self.cleanup()

    def get_thumbnail(self):
        if self.isPlaying:
            self.player.get_thumbnail()

    def listen_for_commands(self):
        self.stt.run() #running the speach to text
        # print the text detected :
        
        self.command = self.stt.text
        self.command = self.command.lower()

        if "error :" in self.command:
            self.count += 1
            if self.count < 2:
                self.tts.speak(phrases[language]["error"])
                self.listen_for_commands()
            else:
                return
        else:
            self.process_command()
        
        #self.player.pause()

    def get_args(self):
        self.stt.run() #running the speach to text
        
        self.arg = self.stt.text
        self.arg = self.arg.lower()

        return self.arg

    def process_command(self):
        if "peux-tu" in self.command:
            self.tts.speak(phrases[language]["processing"])

        if "météo" in self.command or "temps" in self.command:
            self.weather.refresh()
            meteo = self.weather.meteo
            self.tts.speak("Il fait " + meteo["current"]["temp"] + " degrés Celcius, ressentit" + meteo["current"]["body_feeling"])
        
        elif "iss" in self.command or "station spatiale" in self.command:
            self.iss.refresh()
            position = self.iss.position
            self.tts.speak("La station spatiale internationale se trouve au dessus de " + position["over"] + " à " + position["time"])
        
        elif "bonne situation" in self.command:
            playsound.playsound("otis.mp3")
        
        elif "musique" in self.command:
            self.tts.speak(phrases[language]["music"])
            self.get_args()
            print("Music : " + self.arg)
            self.player.use_youtube(self.arg, os.getenv("GOOGLE_KEY"))
            self.player.play()
            self.player.get_duration()

            self.song_duration = self.player.audio_length
            self.audio_position = round(self.player.audio_position / 60000, 2)
            self.progress_value = round(self.player.progress_value, 2)
            self.audio_length_str = self.player.audio_length_str
            print(f"Durée de la musique : {str(self.player.audio_length)}, position dans la musique : {str(self.player.audio_position)}, valeur de la pbar {str(self.player.progress_value)}, Taille de l'audio en str: {self.player.audio_length_str}")
            self.isPlaying = True
        
        elif "pause" in self.command and self.isPlaying:
            self.player.pause()
            self.isPlaying = False
        
        elif "reprends" in self.command and not self.isPlaying:
            self.player.resume()
            self.isPlaying = True
        
        elif "volume" in self.command:
            self.player.volume()

        elif "wikipédia" in self.command or "recherche" in self.command or "rechercher" in self.command:
            self.tts.speak(phrases[language]["wikipedia"])
            self.get_args()
            print("Wikipedia : " + self.arg)
            self.tts.speak(phrases[language]["processing"])
            self.wiki = Wikipedia(self.arg)
            self.wiki.print_page_info()
            try:
                if self.wiki.recherche[0] == "404":
                    self.tts.speak(phrases[language]["wikipedia_error"])
                elif self.wiki.recherche[0] == "503":
                    self.tts.speak(phrases[language]["wikipedia_error"])
                else:
                    self.tts.speak(phrases[language]["wikipedia_success"])
            except:
                self.tts.speak(phrases[language]["wikipedia_error"])
        
        else:
            self.tts.speak(phrases[language]["bozo"])

        # self.player.resume() #resume the music

    def bypass_voice(self):
        self.tts.speak(phrases[language]["music"])
        print("Music : " + "self.arg")
        self.player.use_youtube("Knockin' on heavens door", os.getenv("GOOGLE_KEY"))
        self.player.play()
        self.player.get_duration()

        # UI
        self.audio_length = self.player.audio_length
        self.audio_position = self.player.audio_position
        self.audio_position_str = self.player.audio_position_str
        self.progress_value = self.player.progress_value
        self.audio_length_str = self.player.audio_length_str
        self.music_title = self.player.music_title
        self.music_thumbnail = self.player.music_thumbnail

        #print(f"Durée de la musique : {str(self.player.audio_length)}, position dans la musique : {str(self.player.audio_position)}, valeur de la pbar {str(self.player.progress_value)}, Taille de l'audio en str: {self.player.audio_length_str}")
        self.isPlaying = True

        update_thread = threading.Thread(target=self.update_music_info_continuously)
        update_thread.start()

    def update_music_info_continuously(self):
        while True:
            self.player.get_duration()
            # Mise à jour des attributs de l'interface utilisateur
            self.audio_length = self.player.audio_length
            self.audio_position = self.player.audio_position
            self.audio_position_str = self.player.audio_position_str
            self.progress_value = self.player.progress_value
            self.audio_length_str = self.player.audio_length_str
            self.music_title = self.player.music_title
            self.music_thumbnail = self.player.music_thumbnail
            time.sleep(1)  # Attendre 1 seconde avant la prochaine mise à jour

    def use(self):
        if self.wake_word.detected:
            #self.player.pause() #pause the music
            # first thing first, say Hello :)
            # Check if the wake word was detected in the last 20 minutes
            if self.last_detection_time is None or datetime.now() - self.last_detection_time > timedelta(minutes=20):
                # Perform actions when wake word is detected after 20 minutes or for the first time
                self.tts.speak(self.wish.wish())
                self.last_detection_time = datetime.now()

                self.tts.speak(phrases[language]["listening"])
                # listen for commands
                self.listen_for_commands()
            else:
                # Don't say hello again, it'll be boring else
                # but still listen for commands
                # Say yes I listen to you
                self.last_detection_time = datetime.now()
                self.tts.speak(phrases[language]["listening"])
                # listen for commands
                self.listen_for_commands()

            self.audio_position = round(self.player.audio_position / 60000, 2)
            self.progress_value = round(self.player.progress_value, 2)
            

        self.listen()

    


    def cleanup(self):
        if self.wake_word:
            self.wake_word.cleanup()




if __name__ == "__main__":
    behaviour = Behaviour()
    behaviour.bypass_voice()
