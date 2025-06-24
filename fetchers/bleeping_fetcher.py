"""
[+] bleeping_fetcher.py
    - BleepingComputer Fetcher Module
    - Retrieves latest cybersecurity news from BleepingComputer using RSS feed.
    - Designed for integration with the News Summary pipeline.
"""
# bleeping_fetcher.py: Fetches news articles from BleepingComputer and filters by keyword

# Required Modules
import feedparser

# ===============================
# Fetch stories filtered by keywords
# ===============================

def fetch_stories_by_keywords(keywords):
    """
    Parses BleepingComputer's RSS feed and filters articles by provided keywords.
    
    Args:
        keywords (list): List of keywords to search for in title or summary.
    
    Returns:
        list of dict: Filtered list of news stories.
    """
    url = "https://www.bleepingcomputer.com/feed/"
    feed = feedparser.parse(url)
    results = []

    for entry in feed.entries:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")

        # Simple keyword match
        if any(kw.lower() in title.lower() or kw.lower() in summary.lower() for kw in keywords):
            results.append({
                "title": title,
                "summary": summary,
                "url": link
            })

    return results
