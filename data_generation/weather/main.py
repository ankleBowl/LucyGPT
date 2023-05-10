import os
import sys
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cities import towns_and_cities

def get_name():
    return "Weather"

def get_commands():
    return """
get_weather("city", "time", "date")
"""

def get_utterence():
    # BEGIN         DETAIL      OPTIONAL (PLACE)    OPTIONAL (TIME)    OPTIONAL (DATE)
    # "What's the"  "weather"   "in New York City"  "at 5:00 PM"       "on Monday"

    # VERSUS

    # Begin         DETAIL      OPTIONAL (PLACE)    OPTIONAL (TIME)    OPTIONAL (DATE)
    # "Is it"       "raining"   "in New York City"  "at 5:00 PM"       "on Monday"

    parts_to_options = {
        "PPBEGIN": [
            "Is it going to be",
            "Is it",
            "Is it going to",
            "Will it be",
            "Has it been",
            "Could you tell me if its",
            "Do you know if its"
        ],
        "BEGIN": [
            "What's the",
            "What is the",
            "Can you tell me the",
            "How is the",
            "Are they forecasting",
        ]
    }

    details = [
        [["weather"], None],
        [["temperature"], ["hot", "cold", "warm", "cool"]],
        [["humidity"], ["humid", "dry"]],
        [["wind"], ["windy", "calm"]],
        [["precipitation", "rain"], ["raining", "snowing", "sunny", "cloudy", "clear", "foggy", "hailing", "thundering", "lightning", "windy", "calm"]],
    ]

    utterence = []

    isPresentParticiple = random.choice([True, False])
    if isPresentParticiple:
        utterence.append("PPBEGIN")
        utterence.append("PPDETAIL")
    else:
        utterence.append("BEGIN")
        utterence.append("DETAIL")
    extras = []
    shouldAddPlace = random.choice([True, False])
    if shouldAddPlace:
        extras.append("PLACE")
    shouldAddTime = random.choice([True, False])
    if shouldAddTime:
        extras.append("TIME")
    shouldAddDate = random.choice([True, False])
    if shouldAddDate:
        extras.append("DATE")
    random.shuffle(extras)
    utterence += extras

    output = ""
    time = "N/A"
    date = "N/A"
    place = "N/A"
    solving_for = "N/A"

    for x in utterence:
        if x == "TIME":
            pass
        elif x == "DATE":
            pass
        elif x == "PLACE":
            pass
        elif x == "DETAIL" or x == "PPDETAIL":
            pass
        else:
            output += random.choice(parts_to_options[x])
        output += " "

    return output, "N/A"

if __name__ == "__main__":
    print(get_utterence())