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

phrases = json.load(open("src/features/phrases.json", "r"))


log = Log()

load_dotenv(dotenv_path=".env.secret")
load_dotenv(dotenv_path="config.env")
language = os.getenv("LANGUAGE")
PiKEY = os.getenv("PORCUPINE_KEY")
github_key = os.getenv("GITHUB")


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
        if "peux-tu" in self.command:
            self.tts.speak(phrases[language]["processing"])

        if "météo" in self.command or "temps" in self.command:
            self.getMeteo()
            # set showWeather to True to display the weather for 8 seconds
            self.showWeather = True
            print("Behaviour : 136 showWeather" + str(self.showWeather))
            self.tts.speak("Il fait " + self.meteo["current"]["temp"] + " degrés Celcius, ressenti" + self.meteo["current"]["body_feeling"] + "." + self.description)
            
            self.showWeather = False
       
        elif "iss" in self.command or "station spatiale" in self.command:
            self.iss.refresh()
            position = self.iss.position
            self.tts.speak("La station spatiale internationale se trouve au dessus de " + position["over"] + " à " + position["time"])
        
        elif "bonne situation" in self.command:
            self.player.pause()
            playsound.playsound("otis.mp3")
            self.player.resume()
        
        elif "musique" in self.command:
            self.count = 0
            self.state = 2
            self.tts.speak(phrases[language]["music"])
            self.get_args()
            print("Music : " + self.arg)
            if "stop" in self.arg:
                self.pause()
                self.state = 0
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
        
        elif "reprends" in self.command or "remets la musique" in self.command and not self.isPlaying:
            self.player.resume()
            self.audio_position = self.player.audio_position
            self.progress_value = self.player.progress_value
            self.audio_position_str = self.player.audio_position_str
            self.isPlaying = True
        
        elif "volume" in self.command:
            self.player.volume()

        elif "wikipédia" in self.command or "recherche" in self.command or "rechercher" in self.command:
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
                self.tts.speak(phrases[language]["wikipedia_success"])
                self.tts.speak(wikipedia_fetcher.recherche[0]) # print the first paragraph
        
        elif "stop" in self.command:
            #shutdown the program
            pass

        elif "bonjour" in self.command:
            self.tts.speak(self.wish.wish())

        elif "qui es-tu" in self.command or "quel est ton nom" in self.command:
            self.tts.speak(phrases[language]["who"])

        elif "comment vas-tu" in self.command:
            self.tts.speak(phrases[language]["how"])

        elif "fonctionnalités" in self.command or "commandes" in self.command:
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

        elif "enregistre moi" in self.command or "enregistre-moi" in self.command or "ajoute-moi" in self.command or "enregistrement" in self.command:
            self.tts.speak(phrases[language]["register"])
            self.get_args()
            name = self.arg
            self.tts.speak(phrases[language]["register_loading"])
            self.face.implement_dataset(name)
            self.tts.speak(phrases[language]["register_success"].replace("{0}", name))
            self.face.extract()
            self.face.train()

        elif "reconnais moi" in self.command or "reconnais-moi" in self.command or "connecte-moi" in self.command or "reconnaît moi" in self.command or "reconnaît-moi" in self.command or "connecte-moi" in self.command:
            user = self.face.recognition()[0]
            self.username = user
            print(user)
            # wish
            self.wish.set_username(user)
            self.tts.speak(self.wish.wish())
        
        elif "éteins-toi" in self.command or "éteins toi" in self.command:
            self.tts.speak(phrases[language]["Farewell"])
            playsound.playsound("DATA/musics/shutdown.mp3")
            # crash the program to force shutdown
            exit()

        else:
            self.tts.speak(phrases[language]["bozo"])
            self.state = 0

        # self.player.resume() #resume the music

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
        #play startup song (DATA/musics/startup.mp3)
        playsound.playsound("DATA/musics/startup.mp3")


    def use(self):
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
            self.wake_word.detected = False
            self.pause()
            self.wake_word.stopmsk = False
            self.state = 0
            


        self.listen()


    def cleanup(self):
        if self.wake_word:
            self.wake_word.cleanup()




if __name__ == "__main__":
    behaviour = Behaviour()
    behaviour.use()
