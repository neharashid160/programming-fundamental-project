# ✨ CapGenius — AI-Powered Instagram Caption Generator

CapGenius is a multi-page Streamlit web app that generates polished Instagram captions, hashtag sets, and engagement scores in seconds — powered by the **Groq Cloud API** (LLaMA 3.3 70B).

---

## Features

- **Caption Generation** — produce 1–5 unique caption variations per request
- **Tone Control** — choose from Casual, Professional, Humorous, Inspirational, or Bold
- **Engagement Scoring** — every caption is rated 1–10 with a one-line reason
- **Hashtag Suggestions** — 15 targeted hashtags per generation (mix of popular, niche, and micro)
- **Caption History** — save, browse, and delete captions with tone and timestamp metadata
- **Copy-friendly** — captions displayed in code blocks for easy one-click copying

---

## Project Structure

```
├── p1_streamlit.py        # Home page — caption generator UI
├── pages/
│   └── 1_History.py       # History page — browse & manage saved captions
├── caption_engine.py      # Backend — Groq API calls, scoring, history I/O
├── requirements.txt       # Python dependencies
├── data/
│   └── history.json       # Auto-created; stores saved captions locally
└── .gitignore
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/capgenius.git
cd capgenius
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a Groq API key

Sign up for free at [console.groq.com](https://console.groq.com) and copy your key (`gsk_...`).

### 4. Run the app

```bash
streamlit run p1_streamlit.py
```

The app opens at `http://localhost:8501`. Paste your Groq API key into the field, hit **Verify Key**, and start generating.

---

## Usage

### Home page
1. Enter your Groq API key and verify it.
2. Describe your post — mood, location, vibe. The more detail the better.
3. Pick a tone and choose how many variations you want (1–5).
4. Click **✨ Generate Captions**.
5. Review captions with their engagement scores and hit **💾 Save** to keep any you like.

### History page
- Navigate to **History** in the sidebar to see all saved captions.
- Delete individual entries with 🗑️ or clear everything at once.

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI and multipage routing |
| `openai` | Groq API client (OpenAI-compatible) |
| `requests` | HTTP utilities |
| `pyperclip` | Clipboard support |
| `pillow` | Image utilities |

---

## Notes

- The Groq API is **free** with generous rate limits — no credit card required.
- Caption history is stored locally in `data/history.json` and persists between sessions.
- Your API key is never stored to disk — it lives only in the current session's state.

---

## License

MIT
