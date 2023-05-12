import os
import sys
import random
import openai
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import bs4

search_term_prompt = """Convert the question into a search query

Question 1: What's the latest news on OpenAI
Query 1: openai latest news

Question 2: When is WWDC?
Query 2: WWDC date

Question 3: When was the iPhone 4 made
Query 3: iPhone 4 creation date

Question 4: """

get_answer_prompt = """Use the following data:
(DATA)

Answer the question:
(QUESTION)

Use only the data above for your answer. Your answer should be short (1 to 2 sentences)"""

def search_ddg(search_term):
    waiting_time = 1
    try:
        while (True):
            url = 'https://html.duckduckgo.com/html?q=' + search_term.replace(' ', '%20')
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
            }
            response = requests.get(url, headers=headers)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            links = soup.find(id='links')
            links = links.find_all(class_='links_main')
            formatted_links = []
            for link in links:
                page_title = link.find('h2').text.strip()
                page_url = link.find(class_='result__snippet')['href']
                page_description = link.find(class_='result__snippet').text.strip()

                if len(page_url) > 150:
                    page_url = page_url[:140]

                formatted_links.append({"title": page_title, "url": page_url, "description": page_description})
                if (len(formatted_links) == 4):
                    break

            output = ""
            for flink in formatted_links:
                output += flink["title"] + "\n" + flink["description"] + "\n\n"

            return output.strip()
    except:
        waiting_time = waiting_time * 2
        print("Request Errored, waiting for " + str(waiting_time) + " seconds")
        time.sleep(waiting_time)


def get_openai_completion(question):
    waiting_time = 1
    has_repsonse = False
    while (not has_repsonse):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": question},
                ],
                temperature=0.0,
            )
            has_repsonse = True
        except:
            waiting_time = waiting_time * 2
            print("Request Errored, waiting for " + str(waiting_time) + " seconds")
            time.sleep(waiting_time)
    return response["choices"][0]["message"]["content"]

def create_data_point(question):
    query = get_openai_completion(search_term_prompt + question).split(":")[1].strip()
    search_results = search_ddg(query)
    
    extract_result_prompt = get_answer_prompt.replace("(DATA)", search_results)
    extract_result_prompt = extract_result_prompt.replace("(QUESTION)", question)
    answer = get_openai_completion(extract_result_prompt)

    print("Question: " + question)
    print("Query: " + query)
    print("Results:\n" + search_results + "\n")
    print("Answer: " + answer)

    return [question, query, search_results, answer]

questions = []

with open("questions.txt") as f:
    for line in f:
        questions.append(line.strip())

import json

START_ON = 0
with open("data.json", "w") as f:
    i = 0
    for question in questions:
        i += 1
        if (i < START_ON):
            continue
        data_point = create_data_point(question)
        f.write(json.dumps(data_point) + "\n")
        f.flush()