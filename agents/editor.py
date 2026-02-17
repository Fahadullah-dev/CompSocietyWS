"""
╔══════════════════════════════════════════════════════════════╗
║  agents/editor.py  —  AGENT 3: The Editor                   ║
║                        👥 GROUP 3 OWNS THIS FILE            ║
╚══════════════════════════════════════════════════════════════╝

ROLE:
  The Editor reads BOTH the summary AND the tags, then crafts
  a single punchy headline (max 12 words).

  Using both inputs makes the headline more specific and
  accurate than using either one alone.

  Input  → state["summary"]   (Fetcher's output)
           state["tags"]      (Tagger's output)
  Output → state["headline"]  (a polished one-liner)

YOUR TASK:
  There is exactly ONE bug in the editor_node function below.
  The agent has access to all the data it needs, but it is
  not making full use of it when building the prompt.

  Clue: Look at what variables are available in the function.
        Now look at what actually gets passed into the prompt.
        Is anything being left out?
"""

from config.settings import llm, DigestState


def editor_node(state: DigestState) -> dict:
    print("\n✍️  [EDITOR] Writing headline...")

    summary = state["summary"]
    tags = state["tags"]   # fetched but... is it used?

    # 🐛 BUG IS HERE — the prompt is missing one of the inputs
    prompt = (
        f"Write ONE punchy headline (max 12 words). "
        f"Use this summary: {summary}"
    )
    response = llm.invoke(prompt)

    return {"headline": response.content}
