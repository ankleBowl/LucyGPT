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
    
    get_options = [
        "get",
        "retrieve",
        "obtain",
        "fetch",
        "find",
    ]

    start_command = feature_name.lower() + "." + random.choice(start_options) + "_" + random.choice(names).lower()
    stop_command = feature_name.lower() + "." + random.choice(stop_options) + "_" + random.choice(names).lower()
    get_current_command = feature_name.lower() + "." + random.choice(get_options) + "_" + random.choice(names).lower() + "s"

    feature_commands = {
        "start_timer": [ start_command, start_command + "(timer_amount, timer_unit)" ],
        "stop_timer": [ stop_command, stop_command + "(timer_amount, timer_unit)" ],
        "get_current_timers": [ get_current_command, get_current_command + "()" ],
    }

    keys = list(feature_commands.keys())
    random.shuffle(keys)

    string_representation = ""
    for key in keys:
        string_representation += feature_commands[key][1] + "\n"
    return string_representation

def get_utterence():
    option = random.randint(0, 2)
    if option == 0:
        return get_main_utterence()
    if option == 1:
        return get_time_left_utterence()
    if option == 2:
        return get_get_timer_utterence()

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
    utterence += random.choice(["", " please"])
    
    output = ["INCOMING: " + utterence]
    if is_start:
        output.append(">>> " + feature_commands["start_timer"][0] + "(" + str(timer_amount) + ", \"" + timer_unit + "\")")
    else:
        output.append(">>> " + feature_commands["stop_timer"][0] + "(" + str(timer_amount) + ", \"" + timer_unit + "\")")

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
        
        should_add_nevermind = random.randint(0, 1) == 0
        if should_add_nevermind:
            begginigns = [
                "Nevermind",
                "Forget it",
                "",
            ]
            middles = [
                "I don't need a timer",
                "remove the timer",
                "cancel the timer",
                "stop the timer",
                ""
            ]
            cancel_timer_utterence = random.choice(begginigns) + " " + random.choice(middles)
            if cancel_timer_utterence != "":
                output.append("INCOMING: " + cancel_timer_utterence)
                output.append(">>> " + feature_commands["stop_timer"][0] + "(" + str(timer_amount) + ", \"" + timer_unit + "\")")
                output.append(">>> self.say(\"" + random.choice(stop_responses) + "\")")
    else:
        output.append(">>> self.say(\"" + random.choice(stop_responses) + "\")")

    return [utterence], output

def get_time_left_utterence():
    potential_timers = generate_fake_timers()
        
    openings = [
        "how much time",
        "what time",
    ]

    ends = [
        "remains",
        "is left",
    ]
    
    optional = [
        "on the (TIMER)",
        "on the (DURATION) (TIMER)",
    ]
    
    timer_words = [
        "timer",
        "stopwatch",
        "countdown",
    ]
    
    sections = ["OPENING", "END"]
    shouldInsertOptional = random.randint(0, 3)
    if not shouldInsertOptional == 3:
        sections.insert(shouldInsertOptional, "OPTIONAL")
        
    utterences = []
        
    utterence = ""
    for section in sections:
        if section == "OPENING":
            utterence += random.choice(openings)
        elif section == "END":
            utterence += random.choice(ends)
        elif section == "OPTIONAL":
            utterence += random.choice(optional)
        utterence += " "
    utterence = utterence[:-1]
    utterence = utterence.replace("(TIMER)", random.choice(timer_words))
    
    shouldAskForFakeTimer = random.randint(0, 1) == 0
    
    if (len(potential_timers) == 0 or shouldAskForFakeTimer):
        duration = random.randint(1, 60)
        unit = random.choice(["second", "minute", "hour"])
        current_remaining_time = random.randint(0, duration)
        desiredTimer = (duration, unit, current_remaining_time)
    else:
        desiredTimer = random.choice(potential_timers)
    
    utterenceHasSpecificTimer = "(DURATION)" in utterence
    isMoreThanOneTimer = len(potential_timers) > 1
    
    utterence = utterence.replace("(DURATION)", str(desiredTimer[0]) + " " + desiredTimer[1])
    output = []
    output.append("INCOMING: " + utterence)
    utterences.append(utterence)
    output.append(">>> " + feature_commands["get_current_timers"][0] + "()")
    
    output.append(get_json_from_timers(potential_timers))
    
    if len(potential_timers) == 0:
        output.append(">>> self.say(\"You don't have any timers running.\")")
        return [utterence], output
    elif isMoreThanOneTimer and not utterenceHasSpecificTimer:
        output.append(">>> self.say(\"Which timer?\")")
        
        begginings = [
            "Tell me ",
            "",
            "I want to know ",
        ]
        
        shouldAddAbout = random.randint(0, 1) == 0
        
        utterence = random.choice(begginings)
        if shouldAddAbout:
            utterence += "about "
        utterence = utterence + "the "
        utterence += get_timer_description(desiredTimer)
        output.append("INCOMING: " + utterence)
        utterences.append(utterence)
            
    if (shouldAskForFakeTimer):
        output.append(">>> self.say(\"There is no timer that lasts for that long.\")")
        shouldContinue = random.randint(1, 1) == 1
        if shouldContinue:
            option_one = [
                "What",
                "How",
                "And",
            ]
            desiredTimer = random.choice(potential_timers)
            utterence = random.choice(option_one) + " about the " + get_timer_description(desiredTimer)
            output.append("INCOMING: " + utterence)
            utterences.append(utterence)
            
            isPlural = desiredTimer[2] != 1
            response = ""
            if isPlural:
                response = "There are " + str(desiredTimer[2]) + " " + desiredTimer[1] + "s left."
            else:
                response = "There is " + str(desiredTimer[2]) + " " + desiredTimer[1] + " left."
            output.append(">>> self.say(\"" + response + "\")")
    else:
        isPlural = desiredTimer[2] != 1
        response = ""
        if isPlural:
            response = "There are " + str(desiredTimer[2]) + " " + desiredTimer[1] + "s left."
        else:
            response = "There is " + str(desiredTimer[2]) + " " + desiredTimer[1] + " left."
        output.append(">>> self.say(\"" + response + "\")")
        
    return utterences, output

def generate_fake_timers():
    potential_timers = []
    for _ in range(random.randint(0, 5)):
        duration = random.randint(1, 60)
        unit = random.choice(["second", "minute", "hour"])
        current_remaining_time = random.randint(0, duration)
        potential_timers.append((duration, unit, current_remaining_time))
    return potential_timers

def get_timer_description(desiredTimer):
    timer_words = [
        "timer",
        "stopwatch",
        "countdown",
        "one",
    ]
    shouldPlaceDurationAfter = random.randint(0, 1) == 0
    utterence = ""
    if not shouldPlaceDurationAfter:
        utterence += str(desiredTimer[0]) + " " + desiredTimer[1] + " " + random.choice(timer_words)
        return utterence
    else:
        utterence += random.choice(timer_words)
        options_one = [
            "that",
            "which",
        ]
        options_two = [
            "lasts",
            "is",
            "will last",
            "will be",
        ]
        utterence += " " + random.choice(options_one) + " " + random.choice(options_two) + " " + random.choice(["", "for "]) + str(desiredTimer[0]) + " " + desiredTimer[1]    
        if (desiredTimer[0] != 1):
            utterence += "s"
        return utterence
    
def get_get_timer_utterence():
    timers = generate_fake_timers()
    
    output = []
    
    timer_words = [
        "timers",
        "stopwatches",
        "countdowns",
    ]
    openings = [
        ["What (TIMER)", True],
        ["I want to know what (TIMER)", True],
        ["Tell me my (TIMER)", False],
        ["What are my (TIMER)", False],
        ["Let me know my (TIMER)", False],
        ["Let me know what (TIMER)", True],
        ["Get my (TIMER)", False],
        ["Give me my (TIMER)", False],
    ]
    
    endings_for_what = [
        "do I have",
        "are there",
        "are running",
    ]
    
    opening = random.choice(openings)
    utterence = opening[0]
    if opening[1] == True:
        utterence += " " + random.choice(endings_for_what)
    utterence = utterence.replace("(TIMER)", random.choice(timer_words))
    utterence += random.choice(["", " please"])
    
    output.append("INCOMING: " + utterence)
    output.append(">>> " + feature_commands["get_current_timers"][0] + "()")
    output.append(get_json_from_timers(timers))
    
    response = "You have "
    for x in range(len(timers)):
        timer = timers[x]
        should_do_and = len(timers) > 1 and x == len(timers) - 1
        if should_do_and:
            response += "and "
        total_time_plural = timer[0] != 1
        current_time_plural = timer[2] != 1
        if total_time_plural:
            response += "a timer for " + str(timer[0]) + " " + timer[1] + "s"
        else:
            response += "a timer for " + str(timer[0]) + " " + timer[1]
            
        if current_time_plural:
            response += " with " + str(timer[2]) + " " + timer[1] + "s left"
        else:
            response += " with " + str(timer[2]) + " " + timer[1] + " left"
        response += ", "
    if len(timers) == 0:
        response += "no timers, "
    
    output.append(">>> self.say(\"" + response[:-2] + ".\")")
            
    
    return [utterence], output

def get_json_from_timers(timers):
    json_output = ""
    if len(timers) == 0:
        json_output = "[]"
    else:
        for timer in timers:
            json_output += f"{{\"duration\": {timer[0]}, \"unit\": \"{timer[1]}\", \"current_remaining_time\": {timer[2]}}}, "
        json_output = "[" + json_output[:-2] + "]"
    return json_output


if __name__ == "__main__":
    print(get_commands())
    utterence, output = get_get_timer_utterence()
    for out in output:
        print(out)