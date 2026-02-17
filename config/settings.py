"""
╔══════════════════════════════════════════════════════════════╗
║  config/settings.py  —  Shared config for all agents        ║
║                                                              ║
║  ✏️  The ONLY file where you set your API key.               ║
║  Every agent imports llm and DigestState from here.         ║
╚══════════════════════════════════════════════════════════════╝
"""

from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI

# ─── 🔑 PUT YOUR KEY HERE ────────────────────────────────────────────────────
# Get a free key at: https://aistudio.google.com
GOOGLE_API_KEY = "AIzaSyChq4GAKp0zDdLdUc29enWSC3MNW2suw9k"

# ─── LLM ─────────────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)

# ─── SHARED STATE ─────────────────────────────────────────────────────────────
# This is the "memory" that flows between all agents in the pipeline.
# Each agent reads from this dict and writes back to it.
class DigestState(TypedDict):
    topic: str       # INPUT:  The raw news topic to process
    summary: str     # Agent 1 (Fetcher)  → writes here
    tags: str        # Agent 2 (Tagger)   → writes here
    headline: str    # Agent 3 (Editor)   → writes here
