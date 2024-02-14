"""WMO Weather codes converter"""

import json
import os
import dotenv

from svg import svg2png

from os import path
dotenv.load_dotenv(dotenv_path="config.env")
lang = os.getenv("LANGUAGE")

class Converter:
    def __init__(self, code):
        self.code = code # WMO weather code
        self.weather_codes = json.load(open("src/features/weather/descriptions.json", "r"))
        self.lang = lang
        

    def convert(self):
        # Utilisation du dictionnaire pour obtenir la description correspondante
        description = self.weather_codes[self.lang][str(self.code)][0]
        print(description)  # Cela affichera "Rain - Slight intensity"
        
        return description


    def get_icon(self):
       # Utilisation du dictionnaire pour obtenir le chemin de l'image correspondante
       chemin = path.join("DATA/weather_icons/" + self.weather_codes[self.lang][str(self.code)][1])
       self.icon = svg2png(chemin, 4.0).convert()
       return self.icon



if __name__ == "__main__":
    c = Converter(61)
    c.convert()
    print(c.get_icon())

