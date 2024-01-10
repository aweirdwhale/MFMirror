import os
import pandas as pd

# import config.env
from dotenv import load_dotenv

from features.Logs import log
import requests
import json

load_dotenv(dotenv_path="../../../config.env")
log = log.Log()


class ISS:
    def __init__(self):
        self.api = os.getenv("ISS_LINK")
        self.response = requests.get(self.api)
        self.response = json.loads(self.response.text)

    def current(self):
        if self.response["message"] == "success":
            log.log("ISS API call successful", "success")
            time = pd.to_datetime(self.response["timestamp"], unit='s').time()
            time = time.strftime("%H:%M:%S")

            lat = self.response["iss_position"]["latitude"]
            lon = self.response["iss_position"]["longitude"]
        else:
            log.log(f"ISS API call failed. Try again later.", "error")
            time = None
            lat = None
            lon = None

        position = {
            "time": time,
            "lat": lat,
            "lon": lon
        }

        return position

    def refresh(self):
        self.response = requests.get(self.api)
        self.response = json.loads(self.response.text)
        return self.current()


if __name__ == "__main__":
    iss = ISS()
    print(iss.refresh())
