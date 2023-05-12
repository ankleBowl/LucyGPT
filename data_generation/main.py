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

os.chdir(os.path.dirname(os.path.abspath(__file__)))

features = [
    music,
    weather,
]

def generate_tool_prompt(feature):
    queries, _ = feature.get_utterence()
    prompt = ""
    answer = ""
    for query in queries:
        prompt += "You are Lucy, a virtual assistant developed by Lye Software. You have the following tools available to you:\n"
        for f in features:
            f.get_commands()
            prompt += f"- {f.get_name()}\n"
        prompt += "\n"
        prompt += "Decide the most relevant tool to answer the following input:\n"
        prompt += "- " + query
        prompt += "\n\n>>> " + feature.get_name()
        prompt += "\n---\n"
    return prompt

def generate_request_prompt(feature):
    prompt = 'You are Lucy, a virtual assistant developed by Lye Software\n\n'
    prompt += 'You have the following methods available to you:\n'
    prompt += 'say("message")\n'
    prompt += feature.get_commands().strip() + "\n\n"

    prompt += "Write the code necessary to achieve your goals:\n\n"
    for _ in range(random.randint(1, 3)):
        shouldAddConvo = random.randint(0, 4)
        
        if shouldAddConvo == 0:
            convo = conversation.get_conversation()
            for line in convo:
                prompt += line + "\n"

        query, code = feature.get_utterence()
        for line in code:
            prompt += line + "\n"

        if shouldAddConvo == 1:
            convo = conversation.get_conversation()
            for line in convo:
                prompt += line + "\n"
    return prompt

if __name__ == "__main__":
    # print(generate_request_prompt(music))
    with open("train.txt", "w") as f:
        index = 0
        for x in range(4000):
            feature = features[index]
            index = (index + 1) % len(features)
            f.write(generate_request_prompt(feature))
            f.write("---\n")
        for x in range(1000):
            feature = features[index]
            index = (index + 1) % len(features)
            f.write(generate_tool_prompt(feature))
            
    with open("val.txt", "w") as f:
        index = 0
        for x in range(1000):
            feature = features[index]
            index = (index + 1) % len(features)
            f.write(generate_request_prompt(feature))
            f.write("---\n")
        for x in range(100):
            feature = features[index]
            index = (index + 1) % len(features)
            f.write(generate_tool_prompt(feature))