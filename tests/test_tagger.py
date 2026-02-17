"""
╔══════════════════════════════════════════════════════════════╗
║  tests/test_tagger.py  —  Unit Tests for the Tagger         ║
║                            👥 GROUP 2 RUNS THESE            ║
╚══════════════════════════════════════════════════════════════╝

HOW TO RUN:
  From the news_digest/ folder:
    pytest tests/test_tagger.py -v

WHAT THESE TESTS CHECK:
  1. The node returns a dict with a "tags" key
  2. The LLM prompt contains the SUMMARY text, not the topic
  3. Tags come from the LLM response, not from state directly
  4. The LLM is called exactly once

The critical bug here is about WHICH state key is passed into
the prompt. The tagger must process state["summary"], not
state["topic"] — otherwise Fetcher's work is completely ignored.
"""

import pytest
from unittest.mock import MagicMock, patch


# ─── HELPER ───────────────────────────────────────────────────────────────────
def make_mock_llm(return_text: str):
    mock_response = MagicMock()
    mock_response.content = return_text
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response
    return mock_llm


# ─── TESTS ────────────────────────────────────────────────────────────────────

class TestTaggerNode:

    def test_returns_dict_with_tags_key(self):
        """tagger_node must return a dict containing 'tags'."""
        with patch("agents.tagger.llm", make_mock_llm("Keywords: ocean, discovery, biology. Category: Science")):
            from agents.tagger import tagger_node
            state = {
                "topic": "raw topic text",
                "summary": "Scientists found a new deep-sea creature near volcanic vents.",
                "tags": "",
                "headline": ""
            }
            result = tagger_node(state)

        assert isinstance(result, dict), "Return value must be a dict"
        assert "tags" in result, "Dict must contain the key 'tags'"

    def test_prompt_uses_summary_not_topic(self):
        """
        The LLM prompt must contain the summary text, NOT the topic.
        This is the core bug: reading state['topic'] instead of state['summary'].
        """
        mock_llm = make_mock_llm("Keywords: test. Category: Science")
        topic = "TOPIC_SENTINEL_VALUE"
        summary = "SUMMARY_SENTINEL_VALUE — this is the fetcher's output."

        with patch("agents.tagger.llm", mock_llm):
            from agents.tagger import tagger_node
            state = {"topic": topic, "summary": summary, "tags": "", "headline": ""}
            tagger_node(state)

        # Grab the actual prompt that was passed to the LLM
        call_args = mock_llm.invoke.call_args
        actual_prompt = str(call_args)

        assert summary in actual_prompt, (
            "❌ BUG DETECTED: The prompt does not contain state['summary'].\n"
            "The tagger must process the Fetcher's summary, not the raw topic.\n"
            f"  Expected in prompt : {summary!r}\n"
            f"  Full call args     : {actual_prompt}"
        )

        assert topic not in actual_prompt, (
            "❌ BUG DETECTED: The prompt contains state['topic'] instead of state['summary'].\n"
            "The pipeline is broken — Fetcher's output is being ignored."
        )

    def test_tags_come_from_llm_response(self):
        """The tags must equal what the LLM returned."""
        llm_output = "Keywords: deep-sea, volcanic vents, marine biology. Category: Science"
        with patch("agents.tagger.llm", make_mock_llm(llm_output)):
            from agents.tagger import tagger_node
            state = {
                "topic": "some topic",
                "summary": "A detailed summary about ocean research.",
                "tags": "",
                "headline": ""
            }
            result = tagger_node(state)

        assert result["tags"] == llm_output, (
            f"Expected tags to be the LLM's output.\n"
            f"  Expected : {llm_output!r}\n"
            f"  Got      : {result['tags']!r}"
        )

    def test_llm_is_called_once(self):
        """The LLM must be invoked exactly once per call."""
        mock_llm = make_mock_llm("Keywords: a, b, c. Category: Science")
        with patch("agents.tagger.llm", mock_llm):
            from agents.tagger import tagger_node
            state = {"topic": "t", "summary": "A summary.", "tags": "", "headline": ""}
            tagger_node(state)

        mock_llm.invoke.assert_called_once()

    def test_tags_is_non_empty_string(self):
        """The tags output must be a non-empty string."""
        with patch("agents.tagger.llm", make_mock_llm("Keywords: x, y, z. Category: Business")):
            from agents.tagger import tagger_node
            state = {"topic": "topic", "summary": "Some summary text.", "tags": "", "headline": ""}
            result = tagger_node(state)

        assert isinstance(result["tags"], str), "tags must be a string"
        assert len(result["tags"]) > 0, "tags must not be empty"
