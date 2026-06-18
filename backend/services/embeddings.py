# This File is responsible for Loadibg the Sentence Transformer Model
# It also is responsible for convertiong the given strings into Embeddings
# These Embeddings are used for Vector Search with Mongo Atlas Vector Search in the Database
# Importing Necessary Libraries
from sentence_transformers import SentenceTransformer
from core.config import EMBED_MODEL

# Load the Model
model = SentenceTransformer(EMBED_MODEL)

# The Function used to generate embeddings
def gen_embeddings(text: str, model=model) -> list[float]:
    encoded = model.encode(sentences=text, convert_to_numpy=True)
    return encoded.tolist()
    