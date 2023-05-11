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
    utterence = []
    output = ""
    detail = []

    isPresentParticiple = random.choice([True, False])
    if isPresentParticiple:
        begins = [
            "What's the",
            "What is the",
            "Can you tell me the",
            "How is the",
            "Are they forecasting",
        ]
        details = [
            [["weather", "precipitation", "rain"], "general"],
            [["temperature"], "temperature"],
            [["humidity"], "humidity"],
            [["wind"], "wind"],
        ]
        output += random.choice(begins)
        detail = random.choice(details)
        output += " " + random.choice(detail[0])
    else:
        begins = [
            "Is it going to be",
            "Is it",
            "Is it going to",
            "Will it be",
            "Has it been",
            "Could you tell me if its",
            "Do you know if its"
        ]
        details = [
            [["raining", "snowing", "sunny", "cloudy", "clear", "foggy", "hailing", "thundering", "lightning", "windy"], "general"],
            [["hot", "cold", "warm", "cool"], "temperature"],
            [["humid", "dry"], "humidity"],
            [["windy", "calm"], "wind"],
        ]
        output += random.choice(begins)
        detail = random.choice(details)
        output += " " + random.choice(detail[0])

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

    time = "N/A"
    date = "N/A"
    date_str = "N/A"
    place = "N/A"

    for x in extras:
        if x == "PLACE":
            place = random.choice(towns_and_cities)
            output += " in " + place
        elif x == "TIME":
            hours = random.randint(1, 12)
            ampm = random.choice(["AM", "PM"])
            time = str(hours) + ":00 " + ampm
            output += " at " + time
        elif x == "DATE":
            option = random.randint(0, 3)
            if option == 0:
                output += " today"
                date_str = "today"
                date = "today"
            elif option == 1:
                output += " tomorrow"
                date_str = "tomorrow"
                date = "tomorrow"
            elif option == 2:
                date_str = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                date_str = " on " + date_str
                output += date_str
            elif option == 3:
                date_num = random.randint(1, 31)
                date = str(date_num)
                date_str = date
                if date_num % 10 == 1:
                    date_str += "st"
                elif date_num % 10 == 2:
                    date_str += "nd"
                elif date_num % 10 == 3:
                    date_str += "rd"
                else:
                    date_str += "th"
                date_str = " on the " + date_str
                output += date_str

    code = ["get_weather(\"" + place + "\", \"" + time + "\", \"" + date + "\")"]

    temp = random.randint(0, 150)
    humidity = random.randint(0, 100)
    wind = random.randint(0, 100)
    current_state = random.choice(["raining", "snowing", "sunny", "cloudy", "clear", "foggy", "hailing", "thundering", "lightning", "windy"])
    
    fake_json_response = "{\"temp\": " + str(temp) + ", \"humidity\": " + str(humidity) + ", \"wind\": " + str(wind) + ", \"current_state\": \"" + current_state + "\"}"
    code.append(fake_json_response)

    final_response = ""
    if detail[1] == "general":
        final_response += current_state
    elif detail[1] == "temperature":
        final_response += str(temp) + " degrees"
    elif detail[1] == "humidity":
        final_response += str(humidity) + " percent humidity"
    elif detail[1] == "wind":
        final_response += str(wind) + " mph winds"

    if time != "N/A" or date != "N/A":
        final_response = "It will be " + final_response
    else:
        final_response = "It's " + final_response

    if time != "N/A":
        final_response += " at " + time
    if place != "N/A":
        final_response += " in " + place
    if date != "N/A":
        final_response += date_str

    code.append("self.say(\"" + final_response + "\")")

    return output, code

if __name__ == "__main__":
    output, code = get_utterence()
    print(output)
    print("----")
    for x in code:
        print(x)