import requests
import json
import os
import dotenv

dotenv.load_dotenv(".env.secret")
github_key = os.getenv("GITHUB")

class GhIssue:
    def __init__(self):
        self.headers = {
            "Authorization" : "token {}".format(github_key)
        }
        self.url = "https://api.github.com/repos/aweirdwhale/MFMirror/issues"

    def suggestion(self, content, user):
        self.data = {
            "title": "Suggestion by an user",
            "body": f"### User : {user} thinks we should add this : \n{content}"
        }
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
            response.raise_for_status()
            print("Issue created successfully")
        except requests.exceptions.HTTPError as err:
            print(err)
            print("Issue could not be created")

    def bug(self, content, user):
        self.data = {
            "title": "Bug report",
            "body": f"### User: {user} thinks he found a bug : \n{content}"
        }
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
            response.raise_for_status()
            print("Issue created successfully")
        except requests.exceptions.HTTPError as err:
            print(err)
            print("Issue could not be created")


if __name__ == '__main__':
    suggest = "I think you should add this feature (test from MFM)"
    gh_issue = GhIssue(suggest)
    gh_issue.suggestion()
    gh_issue.bug()