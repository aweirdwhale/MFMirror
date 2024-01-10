import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../../config.env")

"""
class Weather:
returns lat and lon of city, date and hour of the call, temperature, Body feeling, is_day,
precipitation (rain, snowfall), weather_code, wind_speed & wind_direction
"""


class Weather:
    def __init__(self):
        """Weather API called once on init. You'll have to instantiate a second time to reload or call self.refresh()"""
        self.api = os.getenv("WEATHER_LINK")
        self.lon = os.getenv("LON")
        self.lat = os.getenv("LAT")

        # Set up the Open-Meteo API client with cache and retry on error
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.open_meteo = openmeteo_requests.Client(session=self.retry_session)

        self.params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current": ["temperature_2m", "apparent_temperature", "is_day", "precipitation", "rain", "snowfall",
                        "weather_code", "wind_speed_10m", "wind_direction_10m"],
            "hourly": "temperature_2m",
            "timezone": "Europe/London"
        }

        self.responses = self.open_meteo.weather_api(self.api, params=self.params)
        self.response = self.responses[0]  # process first location

    def current(self):
        # Current values. The order of variables needs to be the same as requested.
        current = self.response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_is_day = current.Variables(2).Value()
        current_precipitation = current.Variables(3).Value()
        current_rain = current.Variables(4).Value()
        current_snowfall = current.Variables(5).Value()
        current_wind_speed_10m = current.Variables(6).Value()
        current_wind_direction_10m = current.Variables(7).Value()

        time = pd.to_datetime(current.Time(), unit='s')

        meteo = {
            "header": [
                f"{self.response.Latitude()}°E {self.response.Longitude()}°N",
                f"{self.response.Elevation()}",
                f"Timezone : {self.response.Timezone()} (GMT+{self.response.UtcOffsetSeconds()})"
            ],
            "time": time,
            "temp": current_temperature_2m,
            "body_feeling": current_apparent_temperature,
            "is_day": True if current_is_day == 1 else False,
            "precipitation": {
                "rain": current_rain,
                "snow": current_snowfall,
                "total": current_precipitation
            },
            "wind": {
                "speed": current_wind_speed_10m,
                "direction": current_wind_direction_10m
            }

        }

        return meteo

    def refresh(self):
        self.responses = self.open_meteo.weather_api(self.api, params=self.params)
        self.response = self.responses[0]  # process first location
        return self.current()


if __name__ == "__main__":
    weather = Weather()
    print(weather.refresh())
