import sys
import os
import random

working_dir = os.getcwd()

random.seed(0)

import csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from music import main as music
from weather import main as weather
from conversation import main as conversation
from search import main as search
from timerlucy import main as timer

os.chdir(os.path.dirname(os.path.abspath(__file__)))

features = [
    music,
    weather,
    search,
    timer,
]

feature_weights = [
    2,
    2,
    1,
    2,
]

conversation_frequency = 5 # 0 FOR ALWAYS, HIGHER NUMBERS ARE LESS FREQUENT

weighted_features = []
for i in range(len(features)):
    for _ in range(feature_weights[i]):
        weighted_features.append(features[i])

def generate_request_prompt():
    global features

    prompt = 'You are Lucy, a virtual assistant developed by Lye Software\n\n'
    prompt += 'You have the following methods available to you:\n'
    prompt += 'self.say("message")\n'

    random.shuffle(features)
    for f in features:
        prompt += f.get_commands().strip() + "\n"

    prompt += "\n"
    for _ in range(random.randint(1, 3)):
        picked_feature = random.choice(weighted_features)
        shouldAddConvo = random.randint(0, conversation_frequency + 1)
        
        if shouldAddConvo == 0:
            convo = conversation.get_conversation()
            for line in convo:
                prompt += line + "\n"

        query, code = picked_feature.get_utterence()
        for line in code:
            prompt += line + "\n"

        if shouldAddConvo == 1:
            convo = conversation.get_conversation()
            for line in convo:
                prompt += line + "\n"
    return prompt

import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print(generate_request_prompt())
    with open(working_dir + "/train.json", "w") as f:
        out = []
        for x in range(5000):
            out.append({"text": generate_request_prompt()})
        f.write(json.dumps(out))