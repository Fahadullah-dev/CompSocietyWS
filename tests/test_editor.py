"""
╔══════════════════════════════════════════════════════════════╗
║  tests/test_editor.py  —  Unit Tests for the Editor         ║
║                            👥 GROUP 3 RUNS THESE            ║
╚══════════════════════════════════════════════════════════════╝

HOW TO RUN:
  From the news_digest/ folder:
    pytest tests/test_editor.py -v

WHAT THESE TESTS CHECK:
  1. The node returns a dict with a "headline" key
  2. The LLM prompt contains BOTH summary AND tags
  3. The headline comes from the LLM response
  4. The LLM is called exactly once

The critical bug here is that the Editor has both summary and
tags available in state, but only passes summary into the prompt.
Tags are silently ignored — making the Editor partially blind.
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

class TestEditorNode:

    def test_returns_dict_with_headline_key(self):
        """editor_node must return a dict containing 'headline'."""
        with patch("agents.editor.llm", make_mock_llm("New Species Found in Ocean Depths")):
            from agents.editor import editor_node
            state = {
                "topic": "deep sea discovery",
                "summary": "Scientists found a creature near volcanic vents.",
                "tags": "Keywords: ocean, discovery. Category: Science",
                "headline": ""
            }
            result = editor_node(state)

        assert isinstance(result, dict), "Return value must be a dict"
        assert "headline" in result, "Dict must contain the key 'headline'"

    def test_prompt_contains_summary(self):
        """The LLM prompt must include the summary text."""
        mock_llm = make_mock_llm("Creature Found Near Volcanic Vents")
        summary = "SUMMARY_SENTINEL — scientists found something new."
        tags = "Keywords: ocean. Category: Science"

        with patch("agents.editor.llm", mock_llm):
            from agents.editor import editor_node
            state = {"topic": "t", "summary": summary, "tags": tags, "headline": ""}
            editor_node(state)

        call_args = str(mock_llm.invoke.call_args)
        assert summary in call_args, (
            f"❌ The prompt must include the summary.\n"
            f"  Expected in prompt : {summary!r}\n"
            f"  Full call args     : {call_args}"
        )

    def test_prompt_contains_tags(self):
        """
        The LLM prompt must include the tags text.
        This is the core bug: tags is fetched but not passed into the prompt.
        """
        mock_llm = make_mock_llm("Creature Found Near Volcanic Vents")
        summary = "Scientists found a new creature."
        tags = "TAGS_SENTINEL — Keywords: ocean, vents. Category: Science"

        with patch("agents.editor.llm", mock_llm):
            from agents.editor import editor_node
            state = {"topic": "t", "summary": summary, "tags": tags, "headline": ""}
            editor_node(state)

        call_args = str(mock_llm.invoke.call_args)
        assert tags in call_args, (
            "❌ BUG DETECTED: The prompt does not include state['tags'].\n"
            "The Editor must use BOTH summary and tags to write the headline.\n"
            f"  Expected in prompt : {tags!r}\n"
            f"  Full call args     : {call_args}"
        )

    def test_headline_comes_from_llm_response(self):
        """The headline must equal what the LLM returned."""
        llm_output = "New Deep-Sea Species Thrives Near Volcanic Vents"
        with patch("agents.editor.llm", make_mock_llm(llm_output)):
            from agents.editor import editor_node
            state = {
                "topic": "t",
                "summary": "A summary.",
                "tags": "Keywords: a, b. Category: Science",
                "headline": ""
            }
            result = editor_node(state)

        assert result["headline"] == llm_output, (
            f"Expected headline to be the LLM's output.\n"
            f"  Expected : {llm_output!r}\n"
            f"  Got      : {result['headline']!r}"
        )

    def test_llm_is_called_once(self):
        """The LLM must be invoked exactly once per call."""
        mock_llm = make_mock_llm("Some headline.")
        with patch("agents.editor.llm", mock_llm):
            from agents.editor import editor_node
            state = {"topic": "t", "summary": "A summary.", "tags": "some tags", "headline": ""}
            editor_node(state)

        mock_llm.invoke.assert_called_once()

    def test_headline_is_non_empty_string(self):
        """The headline must be a non-empty string."""
        with patch("agents.editor.llm", make_mock_llm("Ocean Discovery Shocks Scientists")):
            from agents.editor import editor_node
            state = {"topic": "t", "summary": "summary", "tags": "tags", "headline": ""}
            result = editor_node(state)

        assert isinstance(result["headline"], str), "headline must be a string"
        assert len(result["headline"]) > 0, "headline must not be empty"
