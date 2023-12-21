# TheFunPackage - Guesser

''' This is the "Guesser" module. '''

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
import json
import requests

# Function 1 - Age
def age(name, country=None):
    # Variables
    parameters = ["name", "country"]

    # Parameters & Data Types
    paramaters_data = {
        "name": [str, "a string"],
        "country": [(str, type(None)), "a string"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Try/Except - Fetching the Age
    try:
        # Variables
        response = json.loads(requests.get("https://api.agify.io?name=" + name).text) if country == None else json.loads(requests.get("https://api.agify.io?name=" + name + "&country_id=" + country).text)
    except requests.ConnectionError:
        raise ConnectionError("A connection error occurred. Please try again.")
    except:
        raise Exception("An error occurred while fetching the age. Please try again.")

    # Deleting Unwanted Keys
    del response["count"]

    # Returning the Age
    return response

# Function 2 - Gender
def gender(name, country=None):
    # Variables
    parameters = ["name", "country"]

    # Parameters & Data Types
    paramaters_data = {
        "name": [str, "a string"],
        "country": [(str, type(None)), "a string"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Try/Except - Fetching the Gender
    try:
        # Variables
        response = json.loads(requests.get("https://api.genderize.io?name=" + name).text) if country == None else json.loads(requests.get("https://api.genderize.io?name=" + name + "&country_id=" + country).text)
    except requests.ConnectionError:
        raise ConnectionError("A connection error occurred. Please try again.")
    except:
        raise Exception("An error occurred while fetching the gender. Please try again.")

    # Deleting Unwanted Keys
    del response["count"]

    # Returning the Gender
    return response

# Function 3 - Nation
def nation(name):
    # Checking the Data Type of "name"
    if (isinstance(name, str)):
        # Try/Except - Fetching the Nation
        try:
            # Variables
            response = json.loads(requests.get("https://api.nationalize.io?name=" + name).text)
        except requests.ConnectionError:
            raise ConnectionError("A connection error occurred. Please try again.")
        except:
            raise Exception("An error occurred while fetching the nation. Please try again.")

        # Deleting Unwanted Keys
        del response["count"]

        # Returning the Nation
        return response
    else:
        raise TypeError("The 'name' argument must be a string.")