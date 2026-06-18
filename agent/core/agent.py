# This Script defines the GroqChat Instance, it uses the Chat Instancwe Langchain
# It also Attatches the tools defined in the tools directory, such as web_search and url_fetch
# It finally returns the final agent
# Imporitng Necessary Libraries
from langchain_groq import ChatGroq
from tools.url_fetch import fetch_url
from tools.web_search import web_search
from core.config import KEY, MODEL, TEMP

# Create the Function that returns the Agent
def create_agent() -> ChatGroq:
    agent = ChatGroq(model=MODEL, api_key=KEY, temperature=TEMP)
    agent.bind_tools([fetch_url, web_search])
    return agent