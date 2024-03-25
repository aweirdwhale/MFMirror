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
from features.weather.weather_codes import Converter
from features.github.suggestion import GhIssue
#from features.weather.weatherUI import WeatherUI
from features.wikipedia.wikipedia import Wikipedia
import json
import playsound
import pygame
import threading
import sys
import requests

phrases = json.load(open("src/features/phrases.json", "r"))


log = Log()

load_dotenv(dotenv_path=".env.key")
load_dotenv(dotenv_path="config.env")
language = os.getenv("LANGUAGE")
PiKEY = os.getenv("PORCUPINE_KEY")
github_key = os.getenv("GITHUB")
place = os.getenv("PLACE")


class Behaviour():
    def __init__(self):
        self.wake_word = PorcupineListener(
            accessKey=PiKEY,
            keywordPath=["src/features/wakeword/Hermione.ppn", "src/features/wakeword/stop_musique.ppn"],
            modelPath="src/features/wakeword/porcupine_fr.pv",
            outputPath="src/features/wakeword/output-Hermione.wav"
        )
        self.stt = SpeechToText()
        self.tts = TTS(lang=language)
        self.wish = Wish(language)
        self.weather = Weather()
        self.iss = ISS()
        self.player = Player()
        self.face = FaceRecognition(0)
        self.gh = GhIssue()
        self.last_detection_time = None
        self.command = ""
        self.arg = ""
        self.isPlaying = False
        self.count = 0
        self.last_command_time = None
        
        # UI
        self.audio_length = 0
        self.audio_position = 0
        self.audio_position_str = ""
        self.progress_value = 0
        self.audio_length_str = ""
        self.music_title = ""
        self.music_thumbnail = "https://www.aweirdwhale.xyz/pps/21.jpg"
        self.updateThumbnail = False
        self.state = 0  # State of the listener => 0=wakeword, 1=listening and 2=processing

        # Test
        self.test_command = "musique"
        self.test_arg = "Still standing"

        # weather
        self.meteo = {}
        self.getMeteo()
        self.showWeather = False
        self.code = self.meteo["current"]["code"]
        self.c = Converter(self.code)
        self.description = self.c.convert()
        #self.weatherUI = WeatherUI()

        self.username = "Guest"

    def listen(self):
        self.state = 0
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
        self.state = 1
        self.stt.run() #running the speach to text
        # print the text detected :
        
        self.command = self.stt.text
        self.command = self.command.lower()

        # If a command just got executed, don't ask for wakeword
        # if self.last_command_time is None or datetime.now() - self.last_command_time < timedelta(seconds=5):
        #     self.listen_for_commands()

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
        self.isPlaying = False
        self.state = 1
        self.stt.run() #running the speach to text
        
        self.arg = self.stt.text
        # if Unable to understand the command
        if "error :" in self.arg:
            self.count += 1
            if self.count < 2:
                self.tts.speak(phrases[language]["error"])
                self.get_args()
            else:
                return
        else:
            
            self.arg = self.arg.lower()

    def get_args_upper(self):
        self.isPlaying = False
        self.state = 1
        self.stt.run() #running the speach to text
        
        self.arg = self.stt.text
        # if Unable to understand the command
        if "error : unable to understand the audio." in self.arg:
            self.count += 1
            if self.count < 2:
                self.tts.speak(phrases[language]["error"])
                self.get_args_upper()
            else:
                return
        else:
                
            self.arg = self.arg

    def set_playing_state(self, is_playing):
        self.isPlaying = is_playing
 
    def getMeteo(self):
        self.weather.refresh()
        self.meteo = self.weather.meteo
        return self.meteo

    def pause(self):
        if self.isPlaying:
            self.player.pause()
            self.isPlaying = False

    def process_command(self):
        self.state = 2
        self.last_command_time = datetime.now()

        if self.command.split()[-1] == "quoi":
            self.tts.speak("QUOICOUBEH !!")

        if "peux-tu" in self.command:
            self.tts.speak(phrases[language]["processing"])

        if "météo" in self.command or "temps" in self.command or "weather" in self.command:
            self.getMeteo()
            # set showWeather to True to display the weather for 8 seconds
            self.showWeather = True
            print("Behaviour : 136 showWeather" + str(self.showWeather))
            self.tts.speak(phrases[language]["weather"].replace("{0}", self.meteo["current"]["temp"]).replace("{2}", self.meteo["current"]["body_feeling"]).replace("{3}", self.description).replace("{1}", place))
            
            self.showWeather = False
       
        elif "iss" in self.command or "station spatiale" in self.command or "space station" in self.command:
            self.iss.refresh()
            position = self.iss.position
            spik = phrases[language]["iss"].replace("{0}", position["over"]).replace("{1}", position["time"])
            self.tts.speak("La station spatiale internationale se trouve au dessus de " + position["over"] + " à " + position["time"])
        
        elif "bonne situation" in self.command:
            self.player.pause()
            playsound.playsound("otis.mp3")
            self.player.resume()
        
        elif "musique" in self.command or "music" in self.command:
            self.count = 0
            self.state = 2
            self.tts.speak(phrases[language]["music"])
            self.get_args()
            print("Music : " + self.arg)
            if "stop" in self.arg:
                self.pause()
                self.state = 0
                return
            if "error :" in self.arg:
                self.state = 0
                self.tts.speak(phrases[language]["error"])
                return
            self.player.use_youtube(self.arg, os.getenv("GOOGLE_KEY"))
            self.clean_music()
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
            self.updateThumbnail = True
            self.isPlaying = True
            

            

            update_thread = threading.Thread(target=self.update_music_info_continuously)
            update_thread.start()
        
        elif "pause" in self.command and self.isPlaying:
            self.pause()
        
        elif "reprends" in self.command or "remets la musique" in self.command or "play" in self.command and not self.isPlaying:
            self.player.resume()
            self.audio_position = self.player.audio_position
            self.progress_value = self.player.progress_value
            overself.audio_position_str = self.player.audio_position_str
            self.isPlaying = True
        
        elif "volume" in self.command:
            self.player.volume()

        elif "wikipédia" in self.command or "recherche" in self.command or "rechercher" in self.command or "search" in self.command:
            self.tts.speak(phrases[language]["wikipedia"])
            self.get_args_upper()
            subject = self.arg

            wikipedia_fetcher = Wikipedia(subject)
            wikipedia_fetcher.print_page_info()

            # self.tts.speak(wikipedia_fetcher.recherche[0])
            
            if wikipedia_fetcher.recherche[0] == "404":
                self.tts.speak(phrases[language]["wikipedia_error"])
            elif wikipedia_fetcher.recherche[0] == "503":
                self.tts.speak(phrases[language]["wikipedia_error"])
            else:
                self.tts.speak(phrases[language]["wikipedia_success"].replace("{0}", subject))
                self.tts.speak(wikipedia_fetcher.recherche[0]) # print the first paragraph

        elif "bonjour" in self.command or "hello" in self.command:
            self.tts.speak(self.wish.wish())

        elif "qui es-tu" in self.command or "quel est ton nom" in self.command or "who are you" in self.command or "what's your name" in self.command:
            self.tts.speak(phrases[language]["who"])

        elif "comment vas-tu" in self.command or "ça va" in self.command or "how are you" in self.command:
            self.tts.speak(phrases[language]["how"])

        elif "fonctionnalités" in self.command or "commandes" in self.command or "qu'est-ce que tu sais faire" in self.command or "what can you do" in self.command:
            self.tts.speak(phrases[language]["features"])

        elif "suggestion" in self.command or "proposition" in self.command:
            self.tts.speak(phrases[language]["suggestion1"])
            self.get_args_upper()
            suggestion = self.arg
            user = self.username
            self.tts.speak(phrases[language]["suggestion"])
            self.gh.suggestion(suggestion, user)

        elif "bug" in self.command or "problème" in self.command:
            self.tts.speak(phrases[language]["suggestion1"])
            self.get_args_upper()
            bug = self.arg
            self.tts.speak(phrases[language]["bug"])
            self.gh.bug(bug, self.username)

        elif "enregistre moi" in self.command or "enregistre-moi" in self.command or "ajoute-moi" in self.command or "enregistrement" in self.command or "register" in self.command:
            self.tts.speak(phrases[language]["register"])
            self.get_args()
            name = self.arg
            self.tts.speak(phrases[language]["register_loading"])
            self.face.implement_dataset(name)
            self.tts.speak(phrases[language]["register_success"].replace("{0}", name))
            self.face.extract()
            self.face.train()

        elif "reconnais moi" in self.command or "reconnais-moi" in self.command or "connecte-moi" in self.command or "reconnaît moi" in self.command or "reconnaît-moi" in self.command or "connecte-moi" in self.command or "log me in" in self.command or "log me" in self.command or "log in" in self.command or "log me in" in self.command or "log me" in self.command or "log in" in self.command:
            user = self.face.recognition()[0]
            self.username = user
            print(user)
            # wish
            self.wish.set_username(user)
            self.tts.speak(self.wish.wish())
        
        elif "éteins-toi" in self.command or "éteins toi" in self.command or "va faire dodo" in self.command or "rideaux" in self.command or "extinction" in self.command or "shutdown" in self.command or "shut down" in self.command or "go to sleep" in self.command or "go to bed" in self.command or "goodbye" in self.command or "bye" in self.command or "au revoir" in self.command:
            self.tts.speak(phrases[language]["Farewell"])
            playsound.playsound("sounds/shutdown.mp3")
            # crash the program to force shutdown
            os._exit(0)

        elif "qui est la plus belle" in self.command or "qui est le plus beau" in self.command or "magnifique" in self.command :
            self.tts.speak(phrases[language]["beautiful"])

        elif "mise à jour" in self.command or "mettre à jour" in self.command or "nouvelle version" in self.command or "new version" in self.command or "update" in self.command:
            self.update()

        elif "qui est le plus fort" in self.command or "qui est la plus forte" in self.command or "strongest" in self.command or "strong" in self.command:
            self.tts.speak(phrases[language]["strongest"])
        
        elif "restart" in self.command or "reboot" in self.command or "redémarre" in self.command or "redémarrage" in self.command:
            self.tts.speak(phrases[language]["restarting"])
            os.system("sudo reboot")

        else:
            self.tts.speak(phrases[language]["bozo"])
            self.state = 0


        # self.player.resume() #resume the music

    def check_for_update(self):
        self.tts.speak(phrases[language]["check_update"])
        # check if update (api link in config.env)
        update = os.getenv("UPDATE_LINK")
        version = os.getenv("VERSION")
        latest = requests.get(update).json()["versions"][0]["version"]
        if latest != version:
            self.tts.speak(phrases[language]["update_available"].replace("{0}", latest))
            self.tts.speak(phrases[language]["wanna_update"])
        else:
            self.tts.speak(phrases[language]["update_error"])

    def update(self):
        self.tts.speak(phrases[language]["check_update"])
        # check if update (api link in config.env)
        update = os.getenv("UPDATE_LINK")
        version = os.getenv("VERSION")
        latest = requests.get(update).json()["versions"][0]["version"]
        print(latest)
        if latest != version:
            self.tts.speak(phrases[language]["update_available"].replace("{0}", latest))
            # download update
            url = requests.get(update).json()["versions"][0]["url"]
            print(url)

            r = requests.get(url)
            with open("update.zip", "wb") as code:
                code.write(r.content)
            
            # update version in config.env
            with open("config.env", "r") as f:
                lines = f.readlines()
            with open("config.env", "w") as f:
                for line in lines:
                    if "VERSION" in line:
                        f.write(f"VERSION={latest}\n")
                    else:
                        f.write(line)
                        
            # unzip update
            os.system("unzip update.zip")
            os.system("rm update.zip")

            

            self.tts.speak(phrases[language]["update_success"])
            os.execv(sys.executable, ['python'] + sys.argv)

        else:
            self.tts.speak(phrases[language]["update_error"])

    def clean_music(self):
        # reset title, thumbnail etc to avoid showing the previous music
        self.audio_length = 0
        self.audio_position = 0
        self.audio_position_str = ""
        self.progress_value = 0
        self.audio_length_str = ""
        self.music_title = ""
        self.music_thumbnail = "https://www.aweirdwhale.xyz/pps/21.jpg"
        self.updateThumbnail = False
        self.isPlaying = False

    def bypass_voice(self):
        self.get_args()
        self.tts.speak(phrases[language]["music"])
        print("Music : " + "self.arg")
        self.player.use_youtube(self.arg, os.getenv("GOOGLE_KEY"))
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
        self.updateThumbnail = True

        

        update_thread = threading.Thread(target=self.update_music_info_continuously)
        update_thread.start()

    def update_music_info(self, song_name_label, song_duration_label, progress_bar):
        self.isPlaying = self.behaviour.isPlaying
        self.behaviour.set_playing_state(self.isPlaying)

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
            # Mise à jour de l'état de lecture
            self.set_playing_state(self.isPlaying)
            time.sleep(1)  # Attendre 1 seconde avant la prochaine mise à jour

    def startup_song(self):
        

        return True

    def notify(self, message):
        self.tts.speak(message)
    
    def notify_sound(self, sound):
        if sound == 0:
            playsound.playsound("sounds/notif1.mp3")
        else:
            playsound.playsound("sounds/notif erreur.mp3")

    def use(self):
        print("use")
        self.state = 0
        
        if self.wake_word.detected:
            self.state = 2
            #self.player.pause() #pause the music
            # first thing first, say Hello :)
            # Check if the wake word was detected in the last 20 minutes
            if self.last_detection_time is None or datetime.now() - self.last_detection_time > timedelta(minutes=20):
                # Perform actions when wake word is detected after 20 minutes or for the first time
                self.tts.speak(self.wish.wish())
                self.last_detection_time = datetime.now()

                self.tts.speak(phrases[language]["listening"])
                
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

        elif self.wake_word.stopmsk:
            print("Stop musique")
            


        self.listen()

    def cleanup(self):
        if self.wake_word:
            self.wake_word.cleanup()




if __name__ == "__main__":
    behaviour = Behaviour()
    behaviour.use()
