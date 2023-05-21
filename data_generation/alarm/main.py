# THIS ONE IS LIKE, ALL GPT-4

import random

feature_name = "Alarm"
feature_commands = {}

def get_commands():
    global feature_name
    global feature_commands
    
    feature_name = "Alarm"

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
        "dismiss",
    ]
    
    get_options = [
        "get",
        "retrieve",
        "obtain",
        "fetch",
        "find",
    ]

    start_command = feature_name.lower() + "." + random.choice(start_options) + "_" + feature_name.lower()
    stop_command = feature_name.lower() + "." + random.choice(stop_options) + "_" + feature_name.lower()
    get_current_command = feature_name.lower() + "." + random.choice(get_options) + "_" + feature_name.lower() + "s"

    feature_commands = {
        "start_alarm": [ start_command, start_command + "(hour, ampm)" ],
        "stop_alarm": [ stop_command, stop_command + "(hour, ampm)" ],
        "get_current_alarms": [ get_current_command, get_current_command + "()" ],
    }

    keys = list(feature_commands.keys())
    random.shuffle(keys)

    string_representation = ""
    for key in keys:
        string_representation += feature_commands[key][1] + "\n"
    return string_representation

def generate_random_hour():
    # THIS IS BAD CODE BUT WHO ASKED (THANKS GPT-4)
    hour_24 = random.randint(1, 24)
    if hour_24 == 24:
        hour_24 = 0
    if hour_24 > 12:
        hour_12 = hour_24 - 12
        am_pm = "PM"
    elif hour_24 == 12:
        hour_12 = hour_24
        am_pm = "PM"
    elif hour_24 == 0:
        hour_12 = 12
        am_pm = "AM"
    else:
        hour_12 = hour_24
        am_pm = "AM"
    return hour_12, am_pm, f"{hour_12} {am_pm}"

# Generate a random question
def get_create_alarm_utterence(is_cancel=False):
    greetings = ["Can you", "Could you", "Would you mind", "Please", "I need you to", "I'd like you to", ""]
    if (not is_cancel):
        actions = ["set", "create", "schedule", "make", "put", "start"]
        actions_ing = ["setting", "creating", "scheduling", "making", "putting", "starting"]
    else:
        actions = ["stop", "end", "cancel", "dismiss"]
        actions_ing = ["stopping", "ending", "cancelling", "dismissing"]
    prepositions = ["for", "at", "around", "near"]
    politeness = ["please", "if you could", "if you don't mind", "", "kindly"]

    greeting = random.choice(greetings)
    if greeting == "Would you mind":
        action = random.choice(actions_ing)
    else:
        action = random.choice(actions)
    preposition = random.choice(prepositions)
    integer_hour, am_pm, time_period = generate_random_hour()
    polite = random.choice(politeness)

    # Assemble the question
    question = f"{greeting} {action} an alarm {preposition} {time_period} {polite}"

    # Remove any extra spaces
    question = " ".join(question.split())
    
    utterence = [question]
    output = ["INCOMING: " + question]
    
    # Generate the command
    if (not is_cancel):
        output.append(">>> " + feature_commands["start_alarm"][0] + "(" + str(integer_hour) + ", \"" + am_pm + "\")")
        output.append(">>> self.say(\"I set an alarm for " + time_period + "\")")
    else:
        output.append(">>> " + feature_commands["stop_alarm"][0] + "(" + str(integer_hour) + ", \"" + am_pm + "\")")
        output.append(">>> self.say(\"I cancelled the alarm for " + time_period + "\")")

    return utterence, output

def get_list_alarm_utterence():
    # Define the question components
    greetings = ["Can you", "Could you", "Would you mind", "Please", "I need you to", "I'd like you to", ""]
    actions = ["tell me about", "list", "inform me about", "show", "display"]
    actions_ing = ["telling me about", "listing", "informing me about", "showing", "displaying"]
    politeness = ["please", "if you could", "if you don't mind", "", "kindly"]

    greeting = random.choice(greetings)
    if greeting == "Would you mind":
        action = random.choice(actions_ing)
    else:
        action = random.choice(actions)
    polite = random.choice(politeness)

    # Assemble the question
    question = f"{greeting} {action} my alarms {polite}"

    # Remove any extra spaces
    question = " ".join(question.split())

    # Get the get_alarms command
    get_alarms_command = feature_commands["get_current_alarms"][1]

    # Generate the assistant's vocal response
    num_alarms = random.randint(0,5)  # now can generate 0 alarms
    if num_alarms > 0:
        alarms = [generate_random_hour() for _ in range(num_alarms)]
        if num_alarms == 1:
            alarms_str = f"{alarms[0][0]} {alarms[0][1]}"  # single alarm
            response = f"You have an alarm at {alarms_str}."
        else:
            alarms_str = ', '.join([f"{alarm[0]} {alarm[1]}" for alarm in alarms[:-1]])  # all but last
            alarms_str += f" and {alarms[-1][0]} {alarms[-1][1]}"  # last alarm
            response = f"You have alarms at {alarms_str}."
    else:
        alarms = []
        response = "You do not have any alarms set."

    # JSON representation of the alarms
    json_alarms = [{"hour": alarm[0], "ampm": alarm[1]} for alarm in alarms]

    output = []
    output.append("INCOMING: " + question)
    output.append(">>> " + get_alarms_command)
    output.append(json_alarms)
    output.append(">>> self.say(\"" + response + "\")")
    
    return [question], output

def get_utterence():
    option = random.randint(0, 2)
    if option == 0:
        return get_create_alarm_utterence()
    if option == 1:
        return get_create_alarm_utterence(is_cancel=True)
    if option == 2:
        return get_list_alarm_utterence()
    return None, []

# Generate a large number of questions
if __name__ == "__main__":
    get_commands()
    
    utterence, output = get_utterence()
    for x in output:
        print(x)
