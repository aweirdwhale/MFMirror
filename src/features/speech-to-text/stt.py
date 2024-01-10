import os

import sounddevice as sd
from pydub import AudioSegment
from scipy.io.wavfile import write
import wavio as wv
import speech_recognition as sr
from features.Logs.log import Log

# import language
from dotenv import load_dotenv
load_dotenv("../../../config.env")

lang = os.getenv("LANG")

# init log
log = Log()


class SpeechToText:
    def __init__(self, freq=44100, duration=5):
        self.freq = freq
        self.duration = duration
        self.inputFile = './output/recording.mp3'
        self.outputFile = './output/rec.wav'

    def record(self):
        recording = sd.rec(int(self.duration * self.freq), samplerate=self.freq, channels=2)
        # Start recorder with the given values of duration and sample frequency
        # Record audio for the given number of seconds
        sd.wait()
        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        write(self.inputFile, self.freq, recording)

    def convert(self):
        audio = AudioSegment.from_file(self.inputFile)
        audio.export(self.outputFile, format="wav")

    def recognize(self):
        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(self.outputFile) as source:
                audio = recognizer.record(source)  # save audio file
                text = recognizer.recognize_google(audio, language=lang)
                log.log(text, "great")
                return text
        except sr.UnknownValueError:
            log.log("Unable to understand the audio.", "error")
            return ""
        except sr.RequestError as e:
            log.log(f"An error occured while fetching the API: {e}", "error")
            return ""

    def run(self):
        self.record()
        self.convert()
        self.recognize()


if __name__ == "__main__":
    stt = SpeechToText()
    stt.run()
