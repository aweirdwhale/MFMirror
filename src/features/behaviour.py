import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Logs.log import Log
from iss_position.iss import ISS
from music.player import Player
from weather.weather import Weather
from textToSpeech.speech import TTS
from wish.wish import Wish
from speechToText.stt import SpeechToText
from face_recon.facerecognition import FaceRecognition
from wakeword.Wakey import PorcupineListener

import json
import playsound
import pygame

phrases = json.load(open("src/features/phrases.json", "r"))


log = Log()

load_dotenv(dotenv_path=".env.secret")
load_dotenv(dotenv_path="config.env")
language = os.getenv("LANGUAGE")
PiKEY = os.getenv("PORCUPINE_KEY")

class Behaviour:
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

    def listen(self):
        try:
            self.wake_word.initialize()
            self.wake_word.start_detection()
            self.use()
        except KeyboardInterrupt:
            print("Ctrl+C detected. Stopping...")
        finally:
            self.cleanup()

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
        
        elif "iss" in self.commandn or "station spatiale" in self.command:
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
            self.isPlaying = True
        
        elif "pause" in self.command and self.isPlaying:
            self.player.pause()
            self.isPlaying = False
        
        elif "reprends" in self.command and not self.isPlaying:
            self.player.resume()
            self.isPlaying = True
        
        elif "volume" in self.command:
            self.player.volume()

        
        else:
            self.tts.speak(phrases[language]["bozo"])

        # self.player.resume() #resume the music


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


        self.listen()

    def cleanup(self):
        if self.wake_word:
            self.wake_word.cleanup()

if __name__ == "__main__":
    behaviour = Behaviour()
    behaviour.listen()
