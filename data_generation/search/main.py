import os
import sys
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json

examples = []

def read_search_json():
    with open("data.json", "r") as f:
        for line in f:
            examples.append(json.loads(line))

read_search_json()

feature_name = "Search"
feature_commands = {}

def get_name():
    return feature_name

def get_commands():

    names = [
        "Search",
        "Google",
        "Bing",
        "Internet",
        "Web",
    ]

    feature_name = random.choice(names)

    search_options = [
        "search",
        "use",
        "look_up",
        "get",
    ]

    search_command = feature_name.lower() + "." + random.choice(search_options) + "_" + random.choice(names).lower()

    feature_commands = {
        "search_google": [ search_command, search_command + "(search_query)" ]
    }

    keys = list(feature_commands.keys())
    random.shuffle(keys)

    string_representation = ""
    for key in keys:
        string_representation += feature_commands[key][1] + "\n"
    return string_representation

i = -1
def get_utterence():
    global i
    i += 1
    example = examples[i]
    output = []
    output.append("INCOMING: " + example[0])
    output.append(">>> self.search_google(\"" + example[1] + "\")")
    output.append("{\"results\": \"" + example[2] + "\"}")
    output.append(">>> self.say(\"" + example[3] + "\"")
    return example[0], output

if __name__ == "__main__":
    command, output = get_utterence()
    # print(command)
    for line in output:
        print(line)
