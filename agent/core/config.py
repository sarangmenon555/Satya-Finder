from dotenv import load_dotenv
import os

load_dotenv()

TIMEOUT = 20
REDIRECT = True
MAX_CHAR = 10000
KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"
TEMP = 0.7
MAX_ROUNDS = 12

if not KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is not set")