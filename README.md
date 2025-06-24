# 📰 News Summary — Automated Cybersecurity Digest

**News Summary** is a modular Python tool that fetches and summarizes top cybersecurity news each week from **Hacker News** and **BleepingComputer**, delivering it as well-formatted Markdown logs for AI ingestion, research, or review.

Designed for red teamers, security analysts, and AI developers who want to automate threat intelligence and stay on top of trends—without the noise.

---

## 🚀 Features

- **Fetches news** from Hacker News API and BleepingComputer’s RSS feed
- **Keyword-driven filtering**: Only stories matching your interests are summarized
- **Automated OpenAI summarization** with retry/throttling for reliability
- **Markdown report** is generated and logged in `/logs` — ready for ingestion by your AI assistant or personal workflow
- **Highly modular and extendable**: Easily add new news sources or summarizers

---

## 🛠️ Project Structure

```
news-summary/
├── app.py                  # Main launcher script (start here)
├── summarizer.py           # Handles LLM-powered summarization
├── fetchers/
│   ├── hackernews_fetcher.py      # Hacker News keyword-based fetcher
│   └── bleeping_fetcher.py        # BleepingComputer keyword-based fetcher
├── logs/                   # Output markdown summaries
├── keywords.txt            # Your filter list (one keyword per line)
├── requirements.txt        # All required Python packages
├── __init__.py
├── __main__.py
```

---

## ⚡ Quick Start

1. **Clone the repo**  
   `git clone https://github.com/YOURUSERNAME/news-summary.git`

2. **Install dependencies**  
   `pip install -r requirements.txt`

3. **Set your OpenAI API key**  
   Export your key as an environment variable:  
   `export OPENAI_API_KEY=sk-...`

4. **Edit `keywords.txt`**  
   Add your desired topics/keywords (one per line), e.g.:
   ```
   ransomware
   exploit
   CVE
   malware
   breach
   ```

5. **Run the app**  
   ```
   python3 app.py
   ```

   The report will appear in `/logs/` as a timestamped `.md` file!

---

## 🧩 How it Works

- **Keyword Filtering:**  
  The tool pulls the latest stories from both news sources and only keeps those matching your `keywords.txt`.

- **Summarization:**  
  Each story is sent to the OpenAI API (via `summarizer.py`) and summarized for cybersecurity professionals. If the OpenAI key is missing, a stub/fake summary is inserted.

- **Markdown Logging:**  
  The output is a human-readable and AI-ingestable Markdown file—ideal for automated trend monitoring, SOC workflows, or ingestion into a knowledge base.

---

## ⚙️ Scheduling (Optional)

To run automatically every Monday at 9 AM (Linux example):
```bash
crontab -e
```
Add:
```
0 9 * * 1 cd /path/to/news-summary && /usr/bin/python3 app.py
```

---

## 👨‍💻 Developer Notes

- **Add new fetchers:**  
  Just drop a new file in `fetchers/` with a `fetch_stories_by_keywords(keywords)` interface.

- **Add new summarizers:**  
  Extend `summarizer.py` for alternate LLMs or prompt styles.

- **Logs:**  
  All output is in `/logs/` — nothing is sent to a remote server except OpenAI API calls.

- **Community:**  
  Contributions, PRs, and issue reports are welcome—especially if you want to add sources like Ars Technica, The Hacker News, CyberScoop, or automate reporting!

---

## 📜 License

MIT — do whatever you want, just don’t blame us if you miss a zero-day.

---

## ✊ Why News Summary?

*Because even red teamers and analysts deserve automation for their morning news.*
