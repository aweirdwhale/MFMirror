import speech_recognition as sr
from pydub import AudioSegment


def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")


# Utilisation de la fonction pour convertir le fichier audio en WAV
input_file_path = './output.mp3'  # Remplacez par le chemin de votre fichier audio
output_file_path = './output.wav'  # Remplacez par le chemin de sortie en format WAV

convert_to_wav(input_file_path, output_file_path)


def speech_to_text_from_file(audio_file_path):
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)  # Enregistre tout le fichier audio
            text = recognizer.recognize_google(audio, language='fr-FR')
            return text
    except sr.UnknownValueError:
        print("Impossible de comprendre l'audio.")
        return ""
    except sr.RequestError as e:
        print(f"Erreur lors de la demande à pocketSphinx: {e}")
        return ""


# Utilisation de la fonction avec un fichier audio
audio_file_path = './output.wav'  # Remplacez par le chemin de votre fichier audio
result = speech_to_text_from_file(audio_file_path)

if result:
    print("Texte transcrit:", result)
else:
    print("Aucun texte transcrit.")
