# from data_generation.music import main as music
import sys
import os
import random

import csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from music import main as music


os.chdir(os.path.dirname(os.path.abspath(__file__)))

features = [
    music,
]

def generate_tool_prompt():
    prompt = "You are Lucy, a virtual assistant developed by Lye Software. You have the following tools available to you:\n"
    for feature in features:
        prompt += f"- {feature.get_name()}\n"
    prompt += "\n"
    prompt += "Decide the most relevant tool to answer the following input:\n"
    query, code = feature.get_utterence()
    prompt += "- " + query

    answer = feature.get_name()
    return prompt, answer

def generate_request_prompt():
    feature = random.choice(features)
    prompt = 'You are Lucy, a virtual assistant developed by Lye Software\n\n'
    prompt += 'You have the following methods available to you:\n'
    prompt += 'say("message")\n'
    prompt += feature.get_commands().strip() + "\n\n"

    prompt += "Write the code necessary to achieve the following:\n"
    query, code = feature.get_utterence()
    prompt += "- " + query

    answer = code
    return prompt, answer

def format_request_prompt_and_answer():
    prompt, answer = generate_request_prompt()
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

def format_tool_prompt_and_answer():
    prompt, answer = generate_tool_prompt()
    output = ""
    output += prompt
    output += "\n\n"
    output += ">>> " + answer + "\n"
    return output

if __name__ == "__main__":
    with open("data.txt", "w") as f:
        for x in range(3000):
            f.write(format_request_prompt_and_answer())
            f.write("---\n")
        for x in range(1000):
            f.write(format_tool_prompt_and_answer())
            f.write("---\n")