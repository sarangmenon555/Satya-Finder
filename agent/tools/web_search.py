# This Script contains the Web Search Tool, this is responsible for allowing the model to search the web and recieve relevant information
# It use the DuckDuckGo API thorugh Langchain Community
# Uses the tool decoator to turn the function into a tool
# Importing Necessary Libraries
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

web_search = DuckDuckGoSearchRun() # The Tool that will be used
