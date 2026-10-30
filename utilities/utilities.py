import os
from dotenv import load_dotenv

# Load local configuration from .env so connection details stay out of source code.
load_dotenv()

START_SEQUENCE = '\033[90m'
END_SEQUENCE = '\033[0m'

def log(text):
    if os.getenv("DEBUG") == "True":
        print(f"    {START_SEQUENCE}{text}{END_SEQUENCE}")
