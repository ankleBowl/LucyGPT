import random

feature_name = "Reminder"
feature_commands = {}

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


def get_reminder_commands():
    global feature_name
    global feature_commands

    names = [
        "reminder",
    ]

    start_options = [
        "create",
        "set",
        "establish",
        "initiate",
    ]

    stop_options = [
        "delete",
        "remove",
        "cancel",
        "end",
    ]
    
    get_options = [
        "list",
        "retrieve",
        "get",
        "display",
        "show",
    ]

    feature_name = random.choice(names)

    start_command = feature_name.lower() + "." + random.choice(start_options) + "_" + feature_name.lower()
    stop_command = feature_name.lower() + "." + random.choice(stop_options) + "_" + feature_name.lower()
    get_current_command = feature_name.lower() + "." + random.choice(get_options) + "_" + feature_name.lower() + "s"

    feature_commands = {
        "create_reminder": [start_command, start_command + "(time, date, title)"],
        "delete_reminder": [stop_command, stop_command + "(title)"],
        "list_reminders": [get_current_command, get_current_command + "()"],
    }

    keys = list(feature_commands.keys())
    random.shuffle(keys)

    string_representation = ""
    for key in keys:
        string_representation += feature_commands[key][1] + "\n"
    return string_representation

def get_create_reminder_utterance():
    greetings_optional = ["", "Could you", "Can you", "Would you mind", "I'd like you to", "Please"]
    actions = ["set", "make", "create", "establish", "craft"]
    actions_ing = ["setting", "making", "creating", "establishing", "crafting"]
    prepositions = ["for", "at"]
    reminders = ["Team meeting", "Doctor's appointment", "Cooking class", "Dentist appointment", "Date night"]
    politeness = ["kindly", "please", "if possible", "if you could", ""]
    days = ["today", "tomorrow", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dates = []
    for i in range(1, 32):
        string = "the " + str(i)
        if string[:-1] == "1":
            dates.append(string + "st")
        elif string[:-1] == "2":
            dates.append(string + "nd")
        elif string[:-1] == "3":
            dates.append(string + "rd")
        else:
            dates.append(string + "th")

    # Choose components randomly
    greeting = random.choice(greetings_optional)
    if greeting == "Would you mind":
        action = random.choice(actions_ing)
    else:
        action = random.choice(actions)
    preposition = random.choice(prepositions)
    reminder = random.choice(reminders)
    polite = random.choice(politeness)
    target_day = random.choice(days + dates)
    target_hour, target_ampm, target_time = generate_random_hour()
    
    if random.randint(0, 1) == 0:
        target_time = None
    if random.randint(0, 1) == 0:
        target_day = None
    
    if random.random() < 0.15:
        sentence_parts = [
            {"type": "ACTION", "content": "remind me"},
        ]
        ending_parts = [
            {"type": "REMINDER", "content": reminder},
            {"type": "TIME", "content": f"at {target_time}" if target_time is not None else None},
            {"type": "POLITE", "content": polite},
            {"type": "DAY", "content": f"on {target_day}" if target_day is not None else None},
        ]
        random.shuffle(ending_parts)
        sentence_parts += ending_parts
    else:
        sentence_parts = [
            {"type": "GREETING", "content": greeting},
            {"type": "ACTION", "content": action},
            {"type": "OBJECT", "content": "a reminder"},

        ]
        ending_parts = [
            {"type": "TIME", "content": f"{preposition} {target_time}" if target_time is not None else None},
            {"type": "REMINDER", "content": f"for {reminder}"},
            {"type": "DAY", "content": f"on {target_day}" if target_day is not None else None},
            {"type": "POLITE", "content": polite},
        ]
        random.shuffle(ending_parts)
        sentence_parts += ending_parts

    # Assemble the question
    question_parts = [part["content"] for part in sentence_parts if part["content"]]
    question = " ".join(question_parts)

    # Remove any extra spaces
    question = " ".join(question.split())

    utterence = question
    output = []
    output.append("INCOMING: " + utterence)

    if target_day is None and target_time is None:
        utterance = "You didn't specify a date or time. When would you like to set the reminder?"
        output.append("OUTGOING: " + utterance)
        
print(get_create_reminder_utterance())