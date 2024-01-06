import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import shutil


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 100)  # Définir la vitesse de la voix (ajustez selon vos préférences)
engine.setProperty('language', 'en')


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Sir!")

    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")

    else:
        speak("Good Evening Sir!")

    assname = "Jarvis 1.0"
    speak("I am your Assistant")
    speak(assname)


def username():
    speak("What should I call you, sir?")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print(f"Welcome Mr. {uname}".center(columns))
    print("#####################".center(columns))

    speak("How can I help you, Sir?")


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query


if __name__ == '__main__':
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

    # This Function will clean any
    # command before execution of this python file
    clear()
    wishMe()
    username()

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("https://www.youtube.com")
