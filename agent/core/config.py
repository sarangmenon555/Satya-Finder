# This Script is responsible for containing all hardcodec values in this project
# It is created to store all of them in 1 place, and change them whenever necessary
# It provides an easy way to change them without manually searching for them
# Importing necessary libraries
from dotenv import load_dotenv
import os

TIMEOUT = 20 # Timeout for Fetching URL's
REDIRECT = True # Whether to allow redirects in fetching
MAX_CHAR = 10000 # Max Number of chars to return when running url fetch
KEY = os.getenv("GROQ_API_KEY") # Groq API Key
MODEL = "qwen/qwen3.6-27b" # The Model used for agent
TEMP = 0.7 # The Agent's Temperature