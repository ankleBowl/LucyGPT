# from data_generation.music import main as music
import sys
import os
import random

import csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from music import main as music
# from weather import main as weather

os.chdir(os.path.dirname(os.path.abspath(__file__)))

features = [
    music,
    # weather,
]

def generate_tool_prompt(feature):
    feature.get_commands()
    prompt = "You are Lucy, a virtual assistant developed by Lye Software. You have the following tools available to you:\n"
    for feature in features:
        prompt += f"- {feature.get_name()}\n"
    prompt += "\n"
    prompt += "Decide the most relevant tool to answer the following input:\n"
    query, code = feature.get_utterence()
    prompt += "- " + query

    answer = feature.get_name()
    return prompt, answer

def generate_request_prompt(feature):
    prompt = 'You are Lucy, a virtual assistant developed by Lye Software\n\n'
    prompt += 'You have the following methods available to you:\n'
    prompt += 'say("message")\n'
    prompt += feature.get_commands().strip() + "\n\n"

    prompt += "Write the code necessary to achieve the following:\n"
    query, code = feature.get_utterence()
    prompt += "- " + query

    answer = code
    return prompt, answer

def format_request_prompt_and_answer(feature):
    prompt, answer = generate_request_prompt(feature)
    final_output = ""
    final_output += prompt
    final_output += "\n\n"

    i = 0
    for x in answer:
        i += 1
        if i % 2 == 1:
            final_output += ">>> " + x + "\n"
        else:
            final_output += x + "\n"
    return final_output

def format_tool_prompt_and_answer(feature):
    prompt, answer = generate_tool_prompt(feature)
    output = ""
    output += prompt
    output += "\n\n"
    output += ">>> " + answer + "\n"
    return output

if __name__ == "__main__":
    with open("data.txt", "w") as f:
        index = 0
        for x in range(4000):
            feature = features[index]
            index = (index + 1) % len(features)
            f.write(format_request_prompt_and_answer(feature))
            f.write("---\n")
        for x in range(2000):
            feature = features[index]
            index = (index + 1) % len(features)
            f.write(format_tool_prompt_and_answer(feature))
            f.write("---\n")