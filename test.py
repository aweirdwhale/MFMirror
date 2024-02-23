import requests
import json
import os
import dotenv
import sys

dotenv.load_dotenv("config.env")

def update():
        # check if update (api link in config.env)
        update = os.getenv("UPDATE_LINK")
        version = os.getenv("VERSION")
        latest = requests.get(update).json()["versions"][0]["version"]
        print(latest)
        if latest != version:
            print("Update available")
            # download update
            url = requests.get(update).json()["versions"][0]["url"]
            print(url)

            r = requests.get(url)
            with open("update.zip", "wb") as code:
                code.write(r.content)
            
            # update version in config.env
            with open("config.env", "r") as f:
                lines = f.readlines()
            with open("config.env", "w") as f:
                for line in lines:
                    if "VERSION" in line:
                        f.write(f"VERSION={latest}\n")
                    else:
                        f.write(line)
                        
            # unzip update
            os.system("unzip update.zip")
            os.system("rm update.zip")

            

            print("Update complete, restarting...")
            os.execv(sys.executable, ['python'] + sys.argv)

        else:
            print("No update available")

update()