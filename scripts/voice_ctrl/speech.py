from gtts import gTTS
import subprocess


class Speaker:
    def __init__(self, text, lang='en'):
        self.text = text
        self.lang = lang

    def speak(self):
        tts = gTTS(text=self.text, lang=self.lang)
        tts.save("./output/speech.mp3")
        subprocess.run(["mpg321", "./output/speech.mp3"])


if __name__ == "__main__":
    sp = Speaker("Hello, I'm Gideon, your personal assistant.")
    sp.speak()
