from langchain_core.tools import tool
import httpx
from bs4 import BeautifulSoup
from core.config import MAX_CHAR, REDIRECT, TIMEOUT


@tool
def fetch_url(url: str) -> str:
    """Fetch the full main text content of a specific webpage, with navigation,
    footers, scripts, and styling stripped out so only the readable article or
    page content remains.

    Use this after duckduckgo_search, on the 2 to 3 results that look most
    relevant or authoritative, before relying on them in your verdict. Search
    snippets are short fragments and can be misleading on their own - they may
    omit context, refer to an outdated version of a page, or describe a story
    that has since been corrected or retracted. Fetching the full page lets you
    confirm what a source actually says rather than guessing from a snippet.

    Pass the exact URL as returned by duckduckgo_search. If the page cannot be
    reached (timeout, broken link, site blocking automated requests), this will
    return a short error message instead of raising - treat that as a signal to
    try a different source rather than retrying the same URL repeatedly.

    The returned text is capped at a fixed character limit to avoid overwhelming
    your context window, so for very long pages you may only see the beginning
    of the article content.
    """
    try:
        response = httpx.get(url=url, timeout=TIMEOUT, follow_redirects=REDIRECT)
        scraper = BeautifulSoup(response.text, "html.parser")
        for tag in scraper(["nav", "footer", "script", "style"]):
            tag.decompose()
        text = scraper.get_text(separator=" ", strip=True)
        return text[:MAX_CHAR]
    except Exception as e:
        return f"Could not fetch url: {url}, raised error, {e}"