![banner](./Explainations/assets/readmebanner.png)

# **MFMirror**

_**By Les Biquettes**_

_"Les Biquettes" is the name of two french computer science students' band._

## Table of Contents

<details>
<summary>Expend in order to see</summary>

* **[Description](#description)**
* **[Installation](#installation)**
* **[Documentation](#docs)**

</details>

### Description

Don't have any friends? Better than a curly: MFMirror!

MFMirror is an artificial intelligence based on Llama, created by the Biquettes. It powers the world's best mirror. You might ask: If I had to sum up MFMirror with you today, I'd start by saying that it's a meeting between two brilliant minds who reached out to each other, perhaps at a time when we couldn't take it anymore, when we were alone at home. And it's quite curious to think that this chance meeting forged a most perfect mirror, because when you have this taste for things well done, the beautiful gesture, well I'd say that you don't find the interest in spying on your customers as our competitors Amazon, Google or even Apple do.

So, as you may have gathered, Les Biquettes today present a project born out of a meeting between the most eminent minds in science fiction and those of the Brothers Grimm.

A seemingly simple object of fascination, the mirror is in fact a marvellous instrument that has captivated people's imaginations for centuries, possessing a mystical aura that is both practical and magical, making it unique among everyday objects. Here's to artificial intelligence, which we've been talking about far too much lately.

MFMirror is a mirror prototype based on the AI concept of the famous fictional character Tony Stark, a.k.a. Iron Man, or Gideon, the AI of Barry Allen, a.k.a. Flash. A generative AI based on Llama, coupled with voice synthesis, will provide a companion, and control home automation without fear of data leakage. Facial recognition will give the user a feeling of proximity. With no keyboard, mouse or other peripherals, the mirror could be controlled by voice or hand gestures. It would display what you ask it to, thanks to a retrieval screen; it would be battery-powered and in standby it would display the time, the weather and could manage your music from the Internet or stored locally. Finally, using proprietary software, it could manage your schedule, timer and much more without using third-party services. The camera would not be connected to the Internet at all, to avoid spyware.

Les Biquettes make it a point of honour to keep your personal information secure (really!), and 99% of the information needed for the device to function properly would be stored locally, safe from rogue advertisers and pirates.

## Installation

1. Debian based os

   - Install update and upgrade os :

     ```shell
     sudo apt update && apt upgrade
     ```
   - install Python3 and git :

     ```shell
     sudo apt install python3 python3-pip git
     ```
   - Fork and clone this repo

     ```shell
     git clone https://github.com/aweirdwhale/MFMirror
     cd MFMirror
     ```
   - At the root of the project, run `pip install -r requirements.txt`

     - **You will need pyaudio for this project. It's a bit complicated so you may have to search on the web to install it properly :**

     ```shell
       sudo apt-get install python-pyaudio
     ```
   - Still at the root of the project, edit config.env file with your infos.
   - Create your secrets:

     - Make a file `.env.key` at the root.
     - Go to the [Google API](https://console.cloud.google.com/apis/credentials/key "Get a key") and create a key for Youtube Data API v3.
     - Make a [Github Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens "Get a key")
     - Make a free Picovoice:porcupine account and get your [Access Key](https://picovoice.ai/docs/quick-start/porcupine-python/)
     - Fill the .env.key file like so :
       - ```.env.secret
         GOOGLE_KEY = <Your google key>
         PORCUPINE_KEY = <Your porcupine key>
         EMAIL = <Your email>
         GITHUB = <Your GitHub token>
         ```
   - And you are **done** ! You can use this project **as you want**, edit it **as you want !** (Please, **star** and **fork** the repository if you want to **help us** :) )

## Documentation

Folder Structure :

```
  .
  |
  ├── src                     # Source files (alternatively `app`)
  |     └── features          # Here are the face detection, hand gesture, music scripts and so on...
  |     └── components        # Components used in the UI
  |     └── behaviour.py      # This manages the whole behaviour of the app
  |
  ├── interface.py  	      # User interface
  |
  ├── Explainations           # Here you'll find explanations on features and READMEs assets.
  |     └── Assets
  |     └── Face-recognition.md
  |     └── Hand-gesture.md
  |     └── Music.md
  |
  ├── DATA                    # This folder stores datasets as faces and musics
  |
  ├── LICENSE
  └── README.md               # You are here !
```

#### [How face recognition works ?](./Explainations/Face-recognition.md)

#### [How hand gesture detection works ?](./Explainations/Hand-gesture.md)

## **Command list**

Here's a list of everything you can ask to Hermione :

| Command Name                   | Use                                                              |
| ------------------------------ | ---------------------------------------------------------------- |
| weather                        | Tells the current weather (place and coordinates in config.env)) |
| ISS                            | Tells the current position of ISS                                |
| music (play/pause/volume/stop) | Music                                                            |
| Search                         | Search for People in wikipedia's database                        |
| suggestion/bug                 | Opens an issue on github                                         |
| register me                    | Adds you to the (local) user database                            |
| log me                         | Logs you if you are registered                                   |
| shutdown/sleep                 | Shuts down the assistant                                         |
| update                         | Checks if there is a new update and install it if so             |

## Authors

- [@A.weirdwhale](https://www.github.com/aweirdwhale)
- [@Baziog](https://www.github.com/Baziog)

## Appendix

This project is under MIT licence, free for everyone and forever !

[![Licence](https://img.shields.io/badge/Licence-MIT-green?labelColor=gray&style=for-the-badge)](https://choosealicense.com/licenses/mit/)

Fonts used in the UI : [Pilowlava](https://www.freefaces.gallery/typefaces/pilowlava) & [Subjectivity](https://www.freefaces.gallery/typefaces/subjectivity)

## Software :

![PYTHON](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)  ![](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)  ![](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

## Hardware :

![img](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)  ![img](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)


## Changelog : V1.18:02:23

* First stable version
* Minimal for presentation
