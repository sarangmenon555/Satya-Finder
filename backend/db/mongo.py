# This script is responsible for Loading The Client, Database and Collections into memory
# This is done so that every other file can directly access that connection instead of Creating a Client every single time
# It uses the URL and Database name for the .env file
# Importing Necessary libraries
from core.config import MONGO_URL, DB_NAME
from pymongo import AsyncMongoClient

client = AsyncMongoClient(MONGO_URL)
db = client[DB_NAME]

# Collections
claims = db['claims']
search_results = db['search_results']
