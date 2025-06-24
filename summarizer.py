"""
[+] summarize.py
    LLM-based summarization module for news articles.
    Defaults to fake stub if API key is missing.
"""
# Required Modules
import os
import time
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =============================
# Fallback LLM Stub (Dev Mode)
# =============================
def fake_llm_response(prompt: str) -> str:
    """
    Returns placeholder output for dev/test if OpenAI key not set.
    """
    return f"[FAKE SUMMARY] {prompt[:100]}..."

# =============================
# Core OpenAI LLM Call with Retry
# =============================
def query_openai(prompt: str, retries: int = 2) -> str:
    """
    Sends prompt to OpenAI ChatCompletion endpoint and returns summary.
    Retries if timeout occurs.
    Requires OPENAI_API_KEY to be set in environment.
    """
    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7,
                timeout=60  # Set timeout in seconds
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[-] OpenAI summarization failed (attempt {attempt}): {e}")
            if attempt < retries:
                print(f"    Retrying in {2 * attempt} seconds...")
                time.sleep(2 * attempt)
            else:
                return fake_llm_response(prompt)

# =============================
# Summarization Dispatcher
# =============================
def summarize_text(text: str, source: str = "generic") -> str:
    """
    Handles prompt formatting and dispatch for summarization.

    Args:
        text (str): Full content of the story.
        source (str): Tag for formatting prompt type.

    Returns:
        str: Clean summary string.
    """
    if source == "hackernews":
        prompt = f"Summarize this HackerNews story with a cybersecurity focus:\n\n{text}"
    elif source == "bleepingcomputer":
        prompt = f"Summarize this BleepingComputer story with a focus on the key threats and takeaways:\n\n{text}"
    else:
        prompt = f"Summarize the following content:\n\n{text}"

    return query_openai(prompt)

