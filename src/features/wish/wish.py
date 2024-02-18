from datetime import datetime
import json
from random import randint

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../../config.env")
language = os.getenv("LANGUAGE")

wishlist = json.load(open("src/features/wish/wishlist.json", "r"))


class Wish:
    def __init__(self, lang=language, username="Guest"):
        self.lang = lang
        self.daytime = ""
        self.username = None
    
    def set_username(self, username):
        self.username = username

    def _get_random_message(self, message_list):
        index = randint(0, len(message_list) - 1)
        return message_list[index]

    def _get_time_of_day(self):
        print(type(datetime.now().hour))
        if 12 <= datetime.now().hour < 18:
            return "afternoon"
        elif 18 <= datetime.now().hour <= 21:
            return "evening"
        elif 21 < datetime.now().hour <= 24:
            return "doesntMatter"
        elif 0 <= datetime.now().hour < 6:
            return "doesntMatter"
        else:
            return "morning"

    def wish(self):
        self.daytime = self._get_time_of_day()

        # Greet
        if self.username is None:
            greeting_list = wishlist["welcome"][self.lang]["noUsername"]
            greeting = self._get_random_message(greeting_list)
        else:
            greeting_list = wishlist["welcome"][self.lang][self.daytime]
            greeting = self._get_random_message(greeting_list)
            greeting = greeting.replace("{username}", self.username)

        return greeting

    def farewell(self):
        print("called")
        if self.username is None:
            farewell_list = wishlist["goodbye"][self.lang]
            farewell = self._get_random_message(farewell_list)
            farewell = farewell.replace("{username}", " ")
        else:
            farewell_list = wishlist["goodbye"][self.lang]
            farewell = self._get_random_message(farewell_list)
            farewell = farewell.replace("{username}", self.username)

        return farewell


if __name__ == "__main__":
    wish = Wish("en", "Big Boss")
    print(wish.wish())

    # ... other interactions ...

    print(wish.farewell())
