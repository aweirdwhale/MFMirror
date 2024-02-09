import subprocess
from gtts import gTTS

import pygame

#import config
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="config.env")
language = os.getenv("LANG")


class TTS:
    def __init__(self, lang=language):
        self.lang = lang
        self.pygame_instance = None

    def speak(self, text):
        if self.pygame_instance is None:
            self.pygame_instance = pygame.init()

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(.05)

        tts = gTTS(text=text, lang=self.lang)
        tts.save("src/features/textToSpeech/output/speech.mp3")
        subprocess.run(["mpg321", "src/features/textToSpeech/output/speech.mp3"])

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(1)

if __name__ == "__main__":
    tts = TTS(lang="fr")
    tts.speak("Bonjour.")
