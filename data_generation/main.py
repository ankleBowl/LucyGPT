# from data_generation.music import main as music
import sys
import os
import random

random.seed(0)

import csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from music import main as music
from weather import main as weather
from conversation import main as conversation
from search import main as search

os.chdir(os.path.dirname(os.path.abspath(__file__)))

features = [
    music,
    weather,
    search,
]

feature_weights = [
    2,
    2,
    1,
]

conversation_frequency = 5 # 0 FOR ALWAYS, HIGHER NUMBERS ARE LESS FREQUENT

weighted_features = []
for i in range(len(features)):
    for _ in range(feature_weights[i]):
        weighted_features.append(features[i])

# def generate_tool_prompt(feature):
#     queries, _ = feature.get_utterence()
#     prompt = ""
#     answer = ""
#     for query in queries:
#         prompt += "You are Lucy, a virtual assistant developed by Lye Software. You have the following tools available to you:\n"
#         for f in features:
#             f.get_commands()
#             prompt += f"- {f.get_name()}\n"
#         prompt += "\n"
#         prompt += "Decide the most relevant tool to answer the following input:\n"
#         prompt += "- " + query
#         prompt += "\n\n>>> " + feature.get_name()
#         prompt += "\n---\n"
#     return prompt

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
    with open("train.json", "w") as f:
        out = []
        for x in range(4088):
            out.append({"text": generate_request_prompt()})
        f.write(json.dumps(out))
            
    # with open("val.txt", "w") as f:
    #     index = 0
    #     for x in range(1000):
    #         feature = features[index]
    #         index = (index + 1) % len(features)
    #         f.write(generate_request_prompt(feature))
    #         f.write("---\n")
        # for x in range(100):
        #     feature = features[index]
        #     index = (index + 1) % len(features)
        #     f.write(generate_tool_prompt(feature))