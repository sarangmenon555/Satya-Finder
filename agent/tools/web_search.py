from langchain_core.tools import tool
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun


_runner = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return a summary of the top results.

    Use this to find news articles, official announcements, and other sources
    relevant to the claim being investigated. Pass a specific, targeted query
    rather than the full claim text. Run 2 to 4 different query angles to
    surface different sources and catch contradictions. After every 2 calls to
    this tool, use fetch_url on at least one promising result before searching
    again - snippets alone are not sufficient to verify a claim.
    """
    return _runner.run(query)