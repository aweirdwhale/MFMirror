import requests
import json
import os
import dotenv

dotenv.load_dotenv(".env.secret")
github_key = os.getenv("GITHUB")

# Send a request to the GitHub API to make an issue on a repository
suggest = "I think you should add this feature (test from MFM)"

headers = {"Authorization" : "token {}".format(github_key)}
data = {
        "title": "Suggestion by an user",
        "body": f"I think you should add this : {suggest}"
} # suggest is a variable that will be replaced by the suggestion

url = "https://api.github.com/repos/aweirdwhale/MFMirror/issues"

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print("Issue created successfully")
except requests.exceptions.HTTPError as err:
    print(err)
    print("Issue could not be created")