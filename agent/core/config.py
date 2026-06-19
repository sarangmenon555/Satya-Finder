from dotenv import load_dotenv
import os

load_dotenv()

TIMEOUT = 20
REDIRECT = True
MAX_CHAR = 10000
KEY = os.getenv("GROQ_API_KEY")
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TEMP = 0.7
MAX_ROUNDS = 12