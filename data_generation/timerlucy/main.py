import random

feature_name = "Timer"
feature_commands = {}

def get_name():
    return feature_name

def get_commands():
    global feature_name
    global feature_commands

    names = [
        "Timer",
        "Stopwatch",
        "Countdown",
    ]

    feature_name = random.choice(names)

    start_options = [
        "start",
        "begin",
        "set",
        "create",
        "make",
    ]

    stop_options = [
        "stop",
        "end",
        "cancel",
    ]

    start_command = feature_name.lower() + "." + random.choice(start_options) + "_" + random.choice(names).lower()
    stop_command = feature_name.lower() + "." + random.choice(stop_options) + "_" + random.choice(names).lower()

    feature_commands = {
        "start_timer": [ start_command, start_command + "(timer_amount, timer_unit)" ],
        "stop_timer": [ stop_command, stop_command + "(timer_amount, timer_unit)" ],
    }

    keys = list(feature_commands.keys())
    random.shuffle(keys)

    string_representation = ""
    for key in keys:
        string_representation += feature_commands[key][1] + "\n"
    return string_representation

def get_utterence():
    return get_main_utterence()
    pass

def get_main_utterence():
    is_start = random.randint(0, 1) == 0
    verb = ""
    if is_start:
        verbs = ["start", "begin", "set", "create", "make"]
        verb = random.choice(verbs)
    else:
        verbs = ["stop", "end", "cancel"]
        verb = random.choice(verbs)
    timer_amount = random.randint(1, 60)
    timer_unit = random.choice(["second", "minute", "hour"])
    timer_name = random.choice(["timer", "stopwatch", "countdown"])

    utterence_template = ["VERB"]
    
    name_should_be_first = random.randint(0, 1) == 0
    if name_should_be_first and is_start:
        utterence_template.append("NAME")
        utterence_template.append("TIME")
    else:
        utterence_template.append("TIME")
        utterence_template.append("NAME")

    utterence = ""
    has_said_name = False
    for word in utterence_template:
        if word == "VERB":
            utterence += verb
            if is_start:
                utterence += " a"
            else:
                utterence += " the"
        elif word == "NAME":
            utterence += timer_name
            has_said_name = True
        elif word == "TIME":
            if has_said_name:
                utterence += "for "
                if timer_amount != 1:
                    timer_unit += "s"
            utterence += f"{timer_amount} {timer_unit}"
        utterence += " "

    utterence = utterence.strip()
    
    output = ["INCOMING: " + utterence]
    if is_start:
        output.append(">>> " + feature_commands["start_timer"][0] + "(" + str(timer_amount) + ", \"" + timer_unit + "\")")
    else:
        output.append(">>> " + feature_commands["stop_timer"][0] + "(" + str(timer_amount) + ", \"" + timer_unit + "\")")
    output.append("{\"status\": \"success\"}")

    start_responses = [
        "Starting a timer for " + str(timer_amount) + " " + timer_unit + ".",
        "I started a timer for " + str(timer_amount) + " " + timer_unit + ".",
        "Started the " + str(timer_amount) + " " + timer_unit + " timer.",
        "It's started.",
    ]

    stop_responses = [
        "Stopping the timer for " + str(timer_amount) + " " + timer_unit + ".",
        "I stopped the timer for " + str(timer_amount) + " " + timer_unit + ".",
        "Stopped the " + str(timer_amount) + " " + timer_unit + " timer.",
        "It's stopped.",
    ]

    if is_start:
        output.append(">>> self.say(\"" + random.choice(start_responses) + "\")")
    else:
        output.append(">>> self.say(\"" + random.choice(stop_responses) + "\")")

    return [utterence], output

if __name__ == "__main__":
    print(get_commands())
    print(get_utterence())