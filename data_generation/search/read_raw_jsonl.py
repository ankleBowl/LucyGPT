# read in nq-dev-00.jsonl
# log just the questions, write them out to a text file

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json

questions = ""
with open("nq-dev-00.jsonl", "r") as f:
    for line in f:
        line = json.loads(line)
        questions += line["question_text"] + "\n"

with open("questions.txt", "w") as f:
    f.write(questions)