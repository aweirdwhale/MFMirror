import wikipediaapi
import dotenv
import os

dotenv.load_dotenv(".env.secret")
dotenv.load_dotenv(".env")
EMAIL = os.getenv("EMAIL")
LANGUAGE = os.getenv("LANGUAGE")


wiki_wiki = wikipediaapi.Wikipedia(f'MFMirror {EMAIL}', f'{LANGUAGE}')

page_py = wiki_wiki.page('Python_(programming_language)')