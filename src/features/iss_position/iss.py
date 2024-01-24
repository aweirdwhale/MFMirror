import os
import pandas as pd

# import config.env
from dotenv import load_dotenv

#from Logs import log
import requests
import json

load_dotenv(dotenv_path="config.env")
#log = log.Log()


class ISS:
    def __init__(self):
        self.api = os.getenv("ISS_LINK")
        self.response = requests.get(self.api)
        self.response = json.loads(self.response.text)
        self.position = {}
        self.over = "Ocean"
        self.countryName = ""

    def current(self):
        if self.response["message"] == "success":
            time = pd.to_datetime(self.response["timestamp"], unit='s').time()
            time = time.strftime("%H:%M:%S")

            lat = self.response["iss_position"]["latitude"]
            lon = self.response["iss_position"]["longitude"]

            print(lat, lon)

            self.over = requests.get(f"http://api.geonames.org/countryCodeJSON?lat={str(lat)}&lng={str(lon)}&username=aweirdwhale")
            self.over = json.loads(self.over.text)

        else:
            log.log(f"ISS API call failed. Try again later.", "error")
            time = None
            lat = None
            lon = None

        try:  # maybe I cheated a bit here
            self.countryName = self.over["countryName"]
        except:
            self.countryName = "l'océan"

        self.position = {
            "time": str(time),
            "lat": str(lat),
            "lon": str(lon),
            "over": str(self.countryName)
        }

        return self.position

    def refresh(self):
        self.response = requests.get(self.api)
        self.response = json.loads(self.response.text)
        return self.current()


if __name__ == "__main__":
    iss = ISS()
    print(iss.refresh())
