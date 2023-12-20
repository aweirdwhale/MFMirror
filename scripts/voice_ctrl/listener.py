import speech_recognition as sr


def voice_ctrl():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Écoute...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Analyse...")
        texte = recognizer.recognize_google(audio, language="fr-FR")
        print(texte)
    except sr.UnknownValueError:
        print("Impossible de comprendre l'audio.")
    except sr.RequestError as e:
        print(f"Erreur lors de la requête vers l'API Google : {e}")


if __name__ == "__main__":
    voice_ctrl()
