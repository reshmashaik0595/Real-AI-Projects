"""Tool definitions for the local AI assistant project.

This module exposes small Python functions that can be called by an LLM through
OpenAI-compatible tool calling. Each function is registered in a simple schema
that the model can discover and invoke during a conversation.
"""

from datetime import datetime
from utilities.utilities import log
import requests
import json

def get_current_time():
    """Return the current date and time in a human-readable format."""
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


def get_city_weather(city):
    """Fetch the current weather for a given city from the wttr.in API."""
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def get_city():
    return "Hyderabad"

# OpenAI function-calling schema: the model sees these names and arguments.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current date and time as a formatted string.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": "Returns the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City to get the weather for."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_city",
            "description":"",
            "parameters":{
                "type":"object",
                "properties":{}
            }
        }
    }
]

# Map tool names to their Python implementations so the assistant can run them.
FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_city": get_city
}

def run_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}
    
    try:
        func_args = json.loads(tool_call.function.arguments or "{}")
        log(f"🔧  {func_name}({func_args})")
        fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
        result = fn(**func_args)
    except Exception as e:
        result = f"Error while running {func_name} : {e}"
    log(f"↪️ {result}")
    return result