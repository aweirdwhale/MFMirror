import time
from datetime import datetime
import pandas as pd
import json

from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="../../../config.env")
language = os.getenv("LANG")

wishlist = json.load(open("wishlist.json", "r"))
print(wishlist)


class Wish:
    def __init__(self, lang=language):
        self.lang = lang

    # call when the user is recognized
    def welcome(self, username):
        pass


if __name__ == "__main__":
    wish = Wish(lang="en")
    wish.welcome("ttt")
