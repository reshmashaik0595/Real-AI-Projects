#!/usr/bin/env python3

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() #by default looks for .env file

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("MODEL")
)

messages = []

while True:
    user_input = input("\nRESHMA_SHAIK:")

    if user_input.lower() in ['exit','quit','bye','goodbye']:
        break

    messages.append(
        {
            'role':'user', #helps to identify the speaker ['user'(human),'assistant'(model's own replires),'system'(Hidden instructions)]
            'content':user_input
        }
    )

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    messages.append(
        {
            'role':response.choices[0].message.role, #helps to identify the speaker ['user'(human),'assistant'(model's own replires),'system'(Hidden instructions)]
            'content':response.choices[0].message.content
        }
    )

    print("ASSISTANT: " + response.choices[0].message.content) # ollama -> JSON -> OpenAI -> PythonObject
    # print(response.choices[0].message.role)


