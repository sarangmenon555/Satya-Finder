from core.config import MONGO_URL, DB_NAME
from pymongo import AsyncMongoClient

if not MONGO_URL:
    raise RuntimeError("MONGO_URL environment variable is not set")

client = AsyncMongoClient(MONGO_URL)
db = client[DB_NAME]

claims = db['claims']
search_results = db['search_results']