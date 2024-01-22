import subprocess
from gtts import gTTS

#import config
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="config.env")
language = os.getenv("LANG")


class TTS:
    def __init__(self, lang=language):
        self.lang = lang

    def speak(self, text):
        tts = gTTS(text=text, lang=self.lang)
        tts.save("src/features/textToSpeech/output/speech.mp3")
        subprocess.run(["mpg321", "src/features/textToSpeech/output/speech.mp3"])


if __name__ == "__main__":
    tts = TTS(lang="fr")
    tts.speak("Bonjour.")
