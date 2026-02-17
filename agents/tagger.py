"""
╔══════════════════════════════════════════════════════════════╗
║  agents/tagger.py  —  AGENT 2: The Tagger                   ║
║                        👥 GROUP 2 OWNS THIS FILE            ║
╚══════════════════════════════════════════════════════════════╝

ROLE:
  The Tagger reads the Fetcher's summary and extracts:
    - 3 keywords from the text
    - 1 category: Technology / Politics / Science /
                  Business / Entertainment

  Input  → state["summary"]  (Fetcher's output)
  Output → state["tags"]     (keywords + category)

YOUR TASK:
  There is exactly ONE bug in the tagger_node function below.
  The function runs and produces output, but it is tagging
  the WRONG piece of data.

  Clue: Think about what data this agent is SUPPOSED to receive
        from the previous agent. Now check what the prompt is
        actually reading from state. Are they the same key?
"""

from config.settings import llm, DigestState


def tagger_node(state: DigestState) -> dict:
    print("\n🏷️  [TAGGER] Extracting tags...")

    # 🐛 BUG IS HERE — this prompt is reading from the wrong state key
    prompt = (
        f"From this text, extract 3 keywords and assign one category "
        f"(Technology/Politics/Science/Business/Entertainment). "
        f"Text: {state['topic']}"
    )
    response = llm.invoke(prompt)

    return {"tags": response.content}
