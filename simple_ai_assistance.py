#!/usr/bin/env python3

from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import json
import os

# Read local configuration from .env so connection details stay out of the code.
load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("MODEL")
)

# Keep the full conversation so each request includes earlier turns.
messages = []

# Set behavior instructions once at the start of the conversation.
messages.append(
    {
        "role" : "system",
        "content" : "Act like a very humble agent and respond always under 20 words"
    }
)

# Continue chatting until the user enters an exit word.
while True:
    user_input = input("\nRESHMA_SHAIK:")

    if user_input.lower() in ['exit','quit','bye','goodbye']:
        break

    # Add the user's turn before sending the conversation to the model.
    messages.append(
        {
            'role' : 'user',
            'content' : user_input
        }
    )

    # Request a response using the conversation history and configured model.
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools=TOOLS
    )

    msg = response.choices[0].message
    if msg.tool_calls:
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")

            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_args)

            messages.append(
                {
                    "role":"tool",
                    "tool_id":tool_call.id,
                    "content":str(result)
                }
            )

        # 2nd call to LLM Model
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )

        msg = response.choices[0].message

    # Save the reply so it becomes part of the context for the next turn.
    messages.append(
        {
            'role' : response.choices[0].message.role,
            'content' : response.choices[0].message.content
        }
    )

    # Display the assistant's reply and its message role.
    print("ASSISTANT: " + response.choices[0].message.content)
    print(response.choices[0].message.role)
