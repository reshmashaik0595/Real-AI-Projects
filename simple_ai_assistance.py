#!/usr/bin/env python3
"""Simple AI assistant that can call local Python tools during chat."""

#Standart libraries
import os

#Third party libraries
from dotenv import load_dotenv
from openai import OpenAI

#local modules
from tools import TOOLS, run_tool
from utilities.utilities import log

# Load local configuration from .env so connection details stay out of source code.
load_dotenv()

# Limit how many model/tool-call cycles are allowed for each user message.
MAX_RUN_STEPS = 3

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
    user_input = input("\n🙋🏻RESHMA_SHAIK: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    # Add the user's turn before sending the conversation to the model.
    messages.append({"role": "user", "content": user_input})

    for step in range(MAX_RUN_STEPS):

        # Request a response using conversation history and available tools.
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            # The assistant has a final response, so no more tool cycles are needed.
            break

        log(f"Step {step+1}: model requested {len(msg.tool_calls)} tool call(s)")
        # When the model asks for a tool call, run it and send the result back.
        messages.append(msg)

        for tool_call in msg.tool_calls:
            result = run_tool(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_id": tool_call.id,
                    "content": str(result),
                }
            )
    else:
        # The loop ended without a final response because the cycle limit was reached.
        fallback = "I couldn't complete your request within the allowed steps. Please try again."
        messages.append({
            "role": "assistant",
            "content": fallback,
        })
        print("ASSISTANT: " + fallback)
        continue

    # Save the assistant response so it becomes part of the next turn's context.
    messages.append({
        "role": msg.role,
        "content": msg.content,
    })

    # Display the assistant's reply and role to the user.
    print("🤖ASSISTANT: " + msg.content)
    print(msg.role)
