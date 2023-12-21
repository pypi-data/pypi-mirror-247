# TheFunPackage - Init

''' This is the __init__.py file. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import os
import sys
import json
import pickle
import random
import pyjokes
import requests
import randfacts
import webbrowser
from colorama import Fore, Style
from datetime import datetime, timedelta
from PySyst.Packages import package_versions

# Variables - Package Information
__name__ = "TheFunPackage"
__version__ = "1.0.6"
__description__ = "This package is only meant for fun and to entertain you!"
__license__ = "Apache License 2.0"
__author__ = "Aniketh Chavare"
__author_email__ = "anikethchavare@outlook.com"
__github_url__ = "https://github.com/anikethchavare/TheFunPackage"
__pypi_url__ = "https://pypi.org/project/TheFunPackage"
__docs_url__ = "https://anikethchavare.gitbook.io/thefunpackage"

# Function 1 - Version Check
def version_check():
    # Variables
    directory = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/")

    # Nested Function 1 - Version Check 2
    def version_check_2(make_directory):
        # Try/Except - Checking the Version
        try:
            # Variables
            versions = package_versions("python", "TheFunPackage")

            # Checking the Version
            if (versions["Upgrade Needed"]):
                # Checking the Environment
                if ("idlelib.run" in sys.modules):
                    print("You are using TheFunPackage version " + versions["Installed"] + ", however version " + versions["Latest"] + " is available.")
                    print("Upgrade to the latest version for new features and improvements using this command: pip install --upgrade TheFunPackage" + "\n")
                else:
                    print(Fore.YELLOW + "You are using TheFunPackage version " + versions["Installed"] + ", however version " + versions["Latest"] + " is available.")
                    print(Fore.YELLOW + "Upgrade to the latest version for new features and improvements using this command: " + Fore.CYAN + "pip install --upgrade TheFunPackage" + Style.RESET_ALL + "\n")

            # Making the Cache Directory
            if (make_directory):
                # Try/Except - Making the Cache Directory
                try:
                    os.mkdir(directory + "/cache")
                except FileExistsError:
                    pass

            # Opening and Writing to the Cache File
            with open(directory + "/cache/version.cache", "wb") as cache_file:
                pickle.dump({"Future Time": datetime.now() + timedelta(hours=24)}, cache_file)
        except:
            pass

    # Checking if Cache File Exists
    if (os.path.exists(directory + "/cache/version.cache")):
        # Opening and Reading the Cache File
        with open(directory + "/cache/version.cache", "rb") as cache_file:
            # Comparing the Time
            if (pickle.load(cache_file)["Future Time"] < datetime.now()):
                # Running the "version_check_2()" Function
                version_check_2(False)
    else:
        # Running the "version_check_2()" Function
        version_check_2(True)

# Function 1 - GitHub
def github():
    # Opening TheFunPackage's GitHub Repository
    try:
        webbrowser.open(__github_url__)
    except:
        raise Exception("An error occurred while opening the GitHub repository. Please try again.")

# Function 2 - PyPI
def pypi():
    # Opening TheFunPackage's PyPI Page
    try:
        webbrowser.open(__pypi_url__)
    except:
        raise Exception("An error occurred while opening the PyPI page. Please try again.")

# Function 3 - Docs
def docs():
    # Opening TheFunPackage's Docs
    try:
        webbrowser.open(__docs_url__)
    except:
        raise Exception("An error occurred while opening the docs. Please try again.")

# Running the "version_check()" Function
version_check()

# Function 4 - Game
def game(name):
    # Variables
    games_list = ["ant", "avoid", "bagels", "bounce", "cannon", "connect", "crypto", "fidget", "flappy", "guess", "illusion", "life", "madlibs", "maze", "memory", "minesweeper", "pacman", "paint", "pong", "rps", "simonsays", "snake", "tictactoe", "tiles", "tron", "typing", "tennis-game", "rock-paper-scissors"]

    # Checking the Data Type of "name"
    if (isinstance(name, str)):
        # Checking if "name" is Valid
        if (name in games_list):
            # Checking the Value of "name"
            if (name == "tennis-game"):
                # Opening the Tennis Game
                webbrowser.open("https://anikethchavare.vercel.app/projects/tennis-game")
            elif (name == "rock-paper-scissors"):
                # Opening the Rock-Paper-Scissors Game
                webbrowser.open("https://anikethchavare.vercel.app/projects/rock-paper-scissors")
            else:
                # Playing the "freegames" Game
                os.system("python -m freegames." + name)
        else:
            raise Exception("The 'name' argument must be a valid game's name. The available games are:\n\n" + str(games_list))
    else:
        raise TypeError("The 'name' argument must be a string.")

# Function 5 - Joke
def joke(topic="random"):
    # Variables
    joke_topics = ["random", "general", "programming", "knock-knock"]
    programming_joke_random = random.choice([1, 2])
    api_endpoint = "https://official-joke-api.appspot.com/jokes/{0}"

    # Checking the Data Type of "topic"
    if (isinstance(topic, str)):
        # Checking if "topic" is Valid
        if (topic in joke_topics):
            # Checking the Value of "topic"
            if (topic == "random"):
                # Try/Except - Fetching the Joke
                try:
                    # Variables
                    response = json.loads(requests.get(api_endpoint.format("random")).text)
                except requests.ConnectionError:
                    raise ConnectionError("A connection error occurred. Please try again.")
                except:
                    raise Exception("An error occurred while fetching the joke. Please try again.")

                # Returning the Joke
                return response["setup"] + " " + response["punchline"]
            elif (topic in ["general", "knock-knock"]):
                # Try/Except - Fetching the Joke
                try:
                    # Variables
                    response = json.loads(requests.get(api_endpoint.format(topic + "/random")).text)[0]
                except requests.ConnectionError:
                    raise ConnectionError("A connection error occurred. Please try again.")
                except:
                    raise Exception("An error occurred while fetching the joke. Please try again.")

                # Returning the Joke
                return response["setup"] + " " + response["punchline"]
            elif (topic == "programming"):
                # Checking the Value of "programming_joke_random"
                if (programming_joke_random == 1):
                    # Try/Except - Fetching the Joke
                    try:
                        # Variables
                        response = json.loads(requests.get(api_endpoint.format(topic + "/random")).text)[0]
                    except requests.ConnectionError:
                        raise ConnectionError("A connection error occurred. Please try again.")
                    except:
                        raise Exception("An error occurred while fetching the joke. Please try again.")

                    # Returning the Joke
                    return response["setup"] + " " + response["punchline"]
                elif (programming_joke_random == 2):
                    # Returning the Joke
                    return pyjokes.get_joke()
        else:
            raise Exception("The 'topic' argument must be either 'random', 'general', 'programming', or 'knock-knock'.")
    else:
        raise TypeError("The 'topic' argument must be a string.")

# Function 6 - Fact
def fact(topic="general"):
    # Variables
    fact_topics = ["general", "cats"]

    # Checking the Data Type of "topic"
    if (isinstance(topic, str)):
        # Checking if "topic" is Valid
        if (topic in fact_topics):
            # Checking the Value of "topic"
            if (topic == "general"):
                # Returning the Fact
                return randfacts.get_fact(filter_enabled=True, only_unsafe=False)
            elif (topic == "cats"):
                # Try/Except - Fetching the Fact
                try:
                    # Returning the Fact
                    return json.loads(requests.get("https://catfact.ninja/fact").text)["fact"]
                except requests.ConnectionError:
                    raise ConnectionError("A connection error occurred. Please try again.")
                except:
                    raise Exception("An error occurred while fetching the fact. Please try again.")
        else:
            raise Exception("The 'topic' argument must be either 'general' or 'cats'.")
    else:
        raise TypeError("The 'topic' argument must be a string.")

# Function 7 - Bored
def bored():
    # Try/Except - Fetching the Activity
    try:
        # Variables
        response = json.loads(requests.get("https://boredapi.com/api/activity").text)
    except requests.ConnectionError:
        raise ConnectionError("A connection error occurred. Please try again.")
    except:
        raise Exception("An error occurred while fetching the activity. Please try again.")

    # Deleting Unwanted Keys
    del response["price"]
    del response["key"]

    # Returning the Activity
    return response