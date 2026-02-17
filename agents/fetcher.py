"""
╔══════════════════════════════════════════════════════════════╗
║  agents/fetcher.py  —  AGENT 1: The Fetcher                 ║
║                        👥 GROUP 1 OWNS THIS FILE            ║
╚══════════════════════════════════════════════════════════════╝

ROLE:
  The Fetcher reads the raw topic from state and asks the LLM
  to produce a clean 2-3 sentence news summary.

  Input  → state["topic"]    (the raw topic string)
  Output → state["summary"]  (a proper news summary)

YOUR TASK:
  There is exactly ONE bug in the fetcher_node function below.
  The function runs without crashing, but its output is wrong.

  Clue: Run the full pipeline and look closely at what
        gets printed as the Summary in the final output.
        Ask yourself: does it look like a real news summary,
        or does it look like something else entirely?
"""

from config.settings import llm, DigestState


def fetcher_node(state: DigestState) -> dict:
    print("\n📡 [FETCHER] Summarizing topic...")

    prompt = f"Write a 2-3 sentence news summary about: {state['topic']}"
    response = llm.invoke(prompt)

    # 🐛 BUG IS HERE — something is wrong with what this returns
    return {"summary": state["topic"]}
