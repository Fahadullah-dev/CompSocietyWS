# 🤖 Agentic AI Workshop — News Digest Pipeline

A broken 3-agent LangGraph pipeline. Your group must find and fix the bug
in your assigned agent file.

---

## 📁 Project Structure

```
news_digest/
│
├── main.py                  ← Runs the full pipeline  (DO NOT EDIT)
├── requirements.txt
│
├── config/
│   └── settings.py          ← API key + shared state  (DO NOT EDIT)
│
├── agents/
│   ├── fetcher.py           ← 👥 GROUP 1 owns this
│   ├── tagger.py            ← 👥 GROUP 2 owns this
│   └── editor.py            ← 👥 GROUP 3 owns this
│
└── tests/
    ├── test_fetcher.py      ← 👥 GROUP 1 runs these
    ├── test_tagger.py       ← 👥 GROUP 2 runs these
    └── test_editor.py       ← 👥 GROUP 3 runs these
```

---

## ⚙️ Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your API key in config/settings.py
#    Get a free key at: https://aistudio.google.com
GOOGLE_API_KEY = "AIzaSyChq4GAKp0zDdLdUc29enWSC3MNW2suw9k"
```

---

## 🚀 Running the Pipeline

```bash
python main.py
```

---

## 🧪 Running Your Tests

Each group runs only their own test file — no API key needed for tests.

```bash
# Group 1
pytest tests/test_fetcher.py -v

# Group 2
pytest tests/test_tagger.py -v

# Group 3
pytest tests/test_editor.py -v
```

**Before your fix:** some tests will FAIL — that's the point.  
**After your fix:** all tests for your agent should PASS. ✅

---

## 🐛 Your Mission

Each agent file (`fetcher.py`, `tagger.py`, `editor.py`) has exactly
**one bug**. The code runs without crashing, but produces wrong results.

Read the docstring at the top of your agent file for clues.

---

## ✅ Expected Output (when all bugs are fixed)

```
🚀 Starting News Digest Pipeline...

📡 [FETCHER] Summarizing topic...
🏷️  [TAGGER] Extracting tags...
✍️  [EDITOR] Writing headline...

═══════════════════════════════════════════════════════
📰  FINAL DIGEST
═══════════════════════════════════════════════════════
📋  Summary  : Scientists have discovered a previously unknown creature...
🏷️   Tags     : Keywords: deep-sea, volcanic vents, marine biology. Category: Science
📰  Headline : New Deep-Sea Species Found Near Volcanic Vents
═══════════════════════════════════════════════════════
```
