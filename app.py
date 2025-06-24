#! python3

"""
[+] app.py
    Main launcher for News Summary project.
    - Aggregates cybersecurity news from multiple sources.
    - Summarizes stories using OpenAI.
    - Logs markdown summaries for AI-based ingestion.
"""

# ===== Imports =====
import os                       # For filesystem ops
import time                     # For throttling API calls
from datetime import datetime   # For timestamping logs
from fetchers.hackernews_fetcher import fetch_stories_by_keywords as hn_fetch  # HN fetcher
from fetchers.bleeping_fetcher import fetch_stories_by_keywords as bc_fetch    # BC fetcher
from summarizer import summarize_text    # OpenAI LLM summarizer

# ===== Constants =====
LOG_DIR = "logs"                # Output folder for logs
KEYWORDS_FILE = "keywords.txt"  # Path to keyword file

# ===== Load Keywords from File =====
def load_keywords():
    """
    Reads keywords.txt and returns a list of non-empty lines.
    """
    if not os.path.exists(KEYWORDS_FILE):
        print(f"[-] {KEYWORDS_FILE} not found.")
        return []
    # Return stripped non-empty lines as keywords
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# ===== Main App Logic =====
def main():
    # Ensure logs/ directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # Load list of search keywords
    keywords = load_keywords()
    if not keywords:
        print("[-] No keywords loaded. Check your keywords.txt file.")
        return

    # --- Fetch articles from each source (limit 5 each) ---
    print("[+] Fetching stories from Hacker News...")
    hn_stories = hn_fetch(keywords)[:5]

    print("[+] Fetching stories from BleepingComputer...")
    bc_stories = bc_fetch(keywords)[:5]

    # Combine all stories into a single list
    all_stories = hn_stories + bc_stories
    if not all_stories:
        print("[-] No relevant stories found.")
        return
    else:
        print(f"[+] Fetched {len(all_stories)} matching stories.")

    # --- Prepare log filename and open file ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"cyber_news_{timestamp}.md"
    filepath = os.path.join(LOG_DIR, filename)

    # --- Summarize each story (with retry and throttling), then write to file ---
    with open(filepath, "w", encoding="utf-8") as f:
        # Write header
        f.write(f"# Cybersecurity News Summary — {timestamp}\n\n")
        for story in all_stories:
            summary = "[!] Failed to summarize due to timeout or API error."
            # Try up to 3 times per article
            for attempt in range(3):
                try:
                    summary = summarize_text(story["title"], story.get("url", ""))
                    break  # Success, stop retrying
                except Exception as e:
                    print(f"[!] Error summarizing {story['title']}: {e}")
                    if attempt < 2:
                        wait_time = 2 ** attempt
                        print(f"    Retrying in {wait_time}s...")
                        time.sleep(wait_time)
            # Write formatted markdown for this story
            f.write(f"### [{story['title']}]({story.get('url', '')})\n")
            f.write(f"- **Author**: {story.get('by', 'unknown')}\n")
            f.write(f"- **Score**: {story.get('score', 'N/A')}\n")
            f.write(f"- **Time**: {story.get('time', story.get('date', ''))}\n\n")
            f.write(f"**Summary:**\n{summary}\n\n---\n\n")
            # Throttle API calls to avoid rate limits
            time.sleep(2)

    print(f"[✓] Report saved to logs/{filename}")

# ===== Entry Point =====
if __name__ == "__main__":
    main()



