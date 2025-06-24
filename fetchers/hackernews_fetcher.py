"""
[+] hackernews_fetcher.py
    Grabs top HackerNews stories filtered by keyword relevance.
    Designed for weekly ingestion by AI assistant.
"""
# Required Modules
import requests
from datetime import datetime
from time import sleep

# =============================
# HackerNews API Base Endpoint
# =============================
HACKERNEWS_API_BASE = "https://hacker-news.firebaseio.com/v0"

# =============================
# Get Top Story IDs
# =============================
def get_top_story_ids(limit=100):
    """
    Pull top story IDs from HackerNews (default: top 10).
    """
    try:
        response = requests.get(f"{HACKERNEWS_API_BASE}/topstories.json")
        response.raise_for_status()
        return response.json()[:limit]
    except Exception as e:
        print(f"[-] Failed to fetch top stories: {e}")
        return []

# =============================
# Fetch Story Detail
# =============================
def get_story_detail(story_id):
    """
    Retrieves full metadata for a given HackerNews story ID.
    """
    try:
        url = f"{HACKERNEWS_API_BASE}/item/{story_id}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[-] Failed to fetch story {story_id}: {e}")
        return None

# =============================
# Keyword-Based Story Filter
# =============================
def fetch_stories_by_keywords(keywords):
    """
    Filters HackerNews stories based on supplied keyword list.

    Returns:
        List of dicts: matching story metadata for later summarization.
    """
    matches = []
    ids = get_top_story_ids()  # Fetch top N story IDs

    for story_id in ids:
        story = get_story_detail(story_id)  # Pull each story's data

        if story and 'title' in story:
            title = story['title'].lower()

            # Match if any keyword appears in the title
            if any(keyword.lower() in title for keyword in keywords):
                matches.append({
                    'id': story['id'],
                    'title': story['title'],
                    'url': story.get('url', 'No URL'),
                    'score': story.get('score', 0),
                    'by': story.get('by', 'unknown'),
                    'time': datetime.fromtimestamp(story['time']).strftime('%Y-%m-%d %H:%M:%S')
                })

        sleep(0.25)  # Avoid API rate limiting

    return matches
