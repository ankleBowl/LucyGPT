import os
import sys
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cities import towns_and_cities

feature_name = "Weather"
feature_commands = []

def get_name():
    return "Weather"

def get_commands():
    global feature_commands
    global feature_name

    app_name_options = [
        "Weather",
        "Climate",
        "Forecast",
    ]

    feature_name = random.choice(app_name_options)

    get_weather_verb_options = [
        "get",
        "retrieve",
        "obtain",
        "fetch",
        "find",
    ]

    get_weather = feature_name.lower() + "." + random.choice(get_weather_verb_options) + "_" + random.choice(app_name_options).lower()

    feature_commands = {
        "get_weather": [ get_weather, get_weather + "(city_name, time, date)" ]
    }

    keys = list(feature_commands.keys())
    random.shuffle(keys)

    string_representation = ""
    for key in keys:
        string_representation += feature_commands[key][1] + "\n"
    return string_representation

def get_utterence():
    request_count = random.randint(1, 3)
    commands = []
    responses = []
    for _ in range(request_count):
        command, response = get_weather_utterence()
        commands += command
        responses += response
    return commands, responses
    

def assemble_begin_and_detail(isPresentParticiple):
    output = ""
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
        return output, detail
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
        return output, detail
    
def generate_extras():
    output = ""
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
                date_str = " today"
                date = "today"
            elif option == 1:
                output += " tomorrow"
                date_str = " tomorrow"
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
    return output, place, time, date, date_str

def gen_final_response(detail, temp, humidity, wind, current_state, time, place, date, date_str):
    final_response = ""
    if detail[1] == "general":
        final_response += current_state
    elif detail[1] == "temperature":
        final_response += str(temp) + " degrees"
    elif detail[1] == "humidity":
        final_response += str(humidity) + " percent humid"
    elif detail[1] == "wind":
        final_response += str(wind) + " mph winds"

    if time != "N/A" or date != "N/A":
        if not detail[1] == "wind":
            final_response = "It will be " + final_response
        else:
            final_response = "There will be " + final_response
    else:
        if not detail[1] == "wind":
            final_response = "It's " + final_response
        else:
            final_response = "There are " + final_response

    if time != "N/A":
        final_response += " at " + time
    if place != "N/A":
        final_response += " in " + place
    if date != "N/A":
        final_response += date_str
    return final_response

def get_weather_utterence():
    # BEGIN         DETAIL      OPTIONAL (PLACE)    OPTIONAL (TIME)    OPTIONAL (DATE)
    # "What's the"  "weather"   "in New York City"  "at 5:00 PM"       "on Monday"

    # VERSUS

    # Begin         DETAIL      OPTIONAL (PLACE)    OPTIONAL (TIME)    OPTIONAL (DATE)
    # "Is it"       "raining"   "in New York City"  "at 5:00 PM"       "on Monday"
    output = ""
    detail = []

    isPresentParticiple = random.choice([True, False])
    output, detail = assemble_begin_and_detail(isPresentParticiple)

    extras, place, time, date, date_str = generate_extras()
    output += extras

    code = []

    code.append("INCOMING: " + output)
    code.append(">>> " + feature_commands["get_weather"][0] + "(\"" + place + "\", \"" + time + "\", \"" + date + "\")")

    temp = random.randint(0, 150)
    humidity = random.randint(0, 100)
    wind = random.randint(0, 100)
    current_state = random.choice(["raining", "snowing", "sunny", "cloudy", "clear", "foggy", "hailing", "thundering", "lightning", "windy"])
    
    fake_json_response = "{\"temp\": " + str(temp) + ", \"humidity\": " + str(humidity) + ", \"wind\": " + str(wind) + ", \"current_state\": \"" + current_state + "\"}"
    code.append(fake_json_response)

    final_response = gen_final_response(detail, temp, humidity, wind, current_state, time, place, date, date_str)

    code.append(">>> self.say(\"" + final_response + "\")")

    output_array = [output]

    shouldFollowup = random.choice([True, False])
    if shouldFollowup:
        choice = random.randint(0, 1)
        if choice == 0:
            start = [
                "",
                "what about ",
                "how about ",
            ]
            cmd_two = random.choice(["and ", ""]) + random.choice(start)
            extras, new_place, new_time, new_date, new_date_str = generate_extras()
            extras = extras.strip()
            if extras == "":
                return output_array, code
            cmd_two += extras.strip()
            code.append("INCOMING: " + cmd_two)
            output_array.append(cmd_two)

            if new_place != place and new_place != "N/A":
                place = new_place
            if new_time != time and new_time != "N/A":
                time = new_time
            if new_date != date and new_date != "N/A":
                date = new_date
                date_str = new_date_str

            code.append(">>> " + feature_commands["get_weather"][0] + "(\"" + place + "\", \"" + time + "\", \"" + date + "\")")

            temp = random.randint(0, 150)
            humidity = random.randint(0, 100)
            wind = random.randint(0, 100)
            current_state = random.choice(["raining", "snowing", "sunny", "cloudy", "clear", "foggy", "hailing", "thundering", "lightning", "windy"])
            
            fake_json_response = "{\"temp\": " + str(temp) + ", \"humidity\": " + str(humidity) + ", \"wind\": " + str(wind) + ", \"current_state\": \"" + current_state + "\"}"
            code.append(fake_json_response)
        
            final_cmdtwo_response = gen_final_response(detail, temp, humidity, wind, current_state, time, place, date, date_str)
            code.append(">>> self.say(\"" + final_cmdtwo_response + "\")")
        if choice == 1:
            isPresentParticiple = random.choice([True, False])
            cmd_two, new_detail = assemble_begin_and_detail(isPresentParticiple)
            if new_detail[1] == detail[1]:
                return output_array, code
            code.append("INCOMING: " + cmd_two)
            output_array.append(cmd_two)
            final_cmdtwo_response = gen_final_response(new_detail, temp, humidity, wind, current_state, time, place, date, date_str)
            code.append(">>> self.say(\"" + final_cmdtwo_response + "\")")
    return output_array, code

if __name__ == "__main__":
    print(get_commands())
    output, code = get_weather_utterence()
    print(output)
    print("----")
    for x in code:
        print(x)