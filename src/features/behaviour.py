"""Behaviour is the merging point of the different features."""

from features.Logs.log import Log
from features.iss_position.iss import ISS
from features.music.player import Player
from features.weather.weather import Weather
from features.textToSpeech.speech import TTS
from features.wish.wish import Wish
from features.speechToText.stt import SpeechToText
from features.face_recon.facerecognition import FaceRecognition

# initializations
wish = Wish()
stt = SpeechToText()
tts = TTS()
meteo = Weather()
music = Player()
iss = ISS()
log = Log()
recon = FaceRecognition(2)


