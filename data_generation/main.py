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
    queries, _ = feature.get_utterence()
    prompt = ""
    answer = ""
    for query in queries:
        prompt += "You are Lucy, a virtual assistant developed by Lye Software. You have the following tools available to you:\n"
        for feature in features:
            prompt += f"- {feature.get_name()}\n"
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
    query, code = feature.get_utterence()
    answer = code
    return prompt, answer

def format_request_prompt_and_answer(feature):
    prompt, answer = generate_request_prompt(feature)
    final_output = ""
    final_output += prompt
    for x in answer:
        final_output += x + "\n"
    return final_output

if __name__ == "__main__":
    # print(format_request_prompt_and_answer(music))
    with open("data.txt", "w") as f:
        index = 0
        for x in range(4000):
            feature = features[index]
            index = (index + 1) % len(features)
            f.write(format_request_prompt_and_answer(feature))
            f.write("---\n")
        for x in range(1000):
            feature = features[index]
            index = (index + 1) % len(features)
            f.write(generate_tool_prompt(feature))