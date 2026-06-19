from dotenv import load_dotenv
import os

load_dotenv()

TIMEOUT = 20
REDIRECT = True
MAX_CHAR = 10000
KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-groq-70b-8192-tool-use-preview"
TEMP = 0.7
MAX_ROUNDS = 12