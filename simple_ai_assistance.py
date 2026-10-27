#!/usr/bin/env python3
"""Simple AI assistant that can call local Python tools during chat."""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import FUNCTION_NAME_TO_FUNCTION_MAP, TOOLS

# Load local configuration from .env so connection details stay out of source code.
load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("MODEL"),
)

# Keep the full conversation so each request includes earlier turns.
messages = []

# Give the assistant a short personality and response limit for this project.
messages.append(
    {
        "role": "system",
        "content": "Act like a very humble agent and respond always under 20 words.",
    }
)

# Continue chatting until the user chooses to exit.
while True:
    user_input = input("\nRESHMA_SHAIK:")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    # Add the user's turn before sending the conversation to the model.
    messages.append({"role": "user", "content": user_input})

    # Request a response using conversation history and available tools.
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools=TOOLS,
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        # When the model asks for a tool call, run it and send the result back.
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")

            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_id": tool_call.id,
                    "content": str(result),
                }
            )

        # Second model call after tool execution to synthesize the final answer.
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
        )
        msg = response.choices[0].message

    # Save the assistant response so it becomes part of the next turn's context.
    messages.append({
        "role": msg.role,
        "content": msg.content,
    })

    # Display the assistant's reply and role to the user.
    print("ASSISTANT: " + msg.content)
    print(msg.role)
