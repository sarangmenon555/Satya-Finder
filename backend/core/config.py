# This Script is Responsible for Containing every single Value or File Path in the backend
# It is mainly used to ensure that values are not hardcoded and are instead stored in a single file
# This is Done so that specific values can be located and changes easily
# Importing Necessary Libraaries
from dotenv import load_dotenv
import os
load_dotenv()

EMBED_MODEL = "all-MiniLM-L6-v2" # The Model used to generate Vector Search Embeddings
MONGO_URL = os.getenv("MONGO_URI")
DB_NAME = "rumor_db"
THRESHOLD = 60 # The Confidence threshold to whether flagged or not
LIMIT = 20 # Max number of rows to get
SKIP = 0 # Getting rows while skipping by this amount
