from datasets import load_dataset

import random

dataset = load_dataset("allenai/soda")

conversational_examples = []
count = 0
for example in dataset["train"]:
    speakers = example["speakers"]

    speakers_unique = []
    for speaker in speakers:
        if speaker not in speakers_unique:
            speakers_unique.append(speaker)
    if len(speakers_unique) != 2:
        continue
    
    first_person_name = example["PersonX"]
    second_person_name = example["PersonY"]

    conversational_examples.append({"speaker_one": first_person_name, "speaker_two": second_person_name, "conversation": example["dialogue"], "speaker_order": speakers})
    count += 1
    if count > 10000:
        break

def get_conversation():
    index = random.randint(0, len(conversational_examples) - 1)
    user_name = conversational_examples[index]["speaker_one"]
    other_speaker = conversational_examples[index]["speaker_two"]
    output_lines = []
    for x in range(len(conversational_examples[index]['conversation'])):
        line = conversational_examples[index]['conversation'][x].replace(user_name, "User")
        if other_speaker != "":
            line = line.replace(other_speaker, "Lucy")

        if conversational_examples[index]['speaker_order'][x] == user_name:
            line = "INCOMING: " + line
        else:
            line = ">>> self.say(\"" + line + "\")"
        output_lines.append(line)
    return output_lines

message = get_conversation()
for line in message:
    print(line)
