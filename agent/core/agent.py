from langchain_groq import ChatGroq
from tools.url_fetch import fetch_url
from tools.web_search import web_search
from core.config import KEY, MODEL, TEMP

TOOLS = [fetch_url, web_search]

def create_agent() -> ChatGroq:
    llm = ChatGroq(model=MODEL, api_key=KEY, temperature=TEMP)
    return llm.bind_tools(TOOLS)
