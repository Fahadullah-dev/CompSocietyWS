"""
╔══════════════════════════════════════════════════════════════╗
║  tests/test_fetcher.py  —  Unit Tests for the Fetcher       ║
║                            👥 GROUP 1 RUNS THESE            ║
╚══════════════════════════════════════════════════════════════╝

HOW TO RUN:
  From the news_digest/ folder:
    pytest tests/test_fetcher.py -v

WHAT THESE TESTS CHECK:
  1. The node returns a dict with a "summary" key
  2. The summary is NOT just a copy of the input topic
  3. The summary looks like real content (has length)
  4. The LLM is actually being called (not skipped)

These tests use "mocking" — they replace the real LLM with a
fake one so you don't need an API key to run tests.
The fake LLM always returns "Mocked LLM summary response."
"""

import pytest
from unittest.mock import MagicMock, patch


# ─── HELPER: build a fake LLM response ────────────────────────────────────────
def make_mock_llm(return_text: str):
    """Returns a mock llm object whose .invoke() returns return_text."""
    mock_response = MagicMock()
    mock_response.content = return_text
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = mock_response
    return mock_llm


# ─── TESTS ────────────────────────────────────────────────────────────────────

class TestFetcherNode:

    def test_returns_dict_with_summary_key(self):
        """fetcher_node must return a dict containing 'summary'."""
        with patch("agents.fetcher.llm", make_mock_llm("Mocked LLM summary response.")):
            from agents.fetcher import fetcher_node
            state = {"topic": "AI replaces all programmers", "summary": "", "tags": "", "headline": ""}
            result = fetcher_node(state)

        assert isinstance(result, dict), "Return value must be a dict"
        assert "summary" in result, "Dict must contain the key 'summary'"

    def test_summary_is_not_the_raw_topic(self):
        """
        The summary must NOT be a copy of the input topic.
        This is the core bug: returning state['topic'] instead of response.content.
        """
        topic = "AI replaces all programmers"
        with patch("agents.fetcher.llm", make_mock_llm("Mocked LLM summary response.")):
            from agents.fetcher import fetcher_node
            state = {"topic": topic, "summary": "", "tags": "", "headline": ""}
            result = fetcher_node(state)

        assert result["summary"] != topic, (
            "❌ BUG DETECTED: summary equals the raw topic. "
            "You are returning state['topic'] instead of response.content."
        )

    def test_summary_comes_from_llm_response(self):
        """The summary must equal what the LLM returned."""
        llm_output = "Scientists have found a never-before-seen creature near volcanic vents."
        with patch("agents.fetcher.llm", make_mock_llm(llm_output)):
            from agents.fetcher import fetcher_node
            state = {"topic": "deep sea creature discovery", "summary": "", "tags": "", "headline": ""}
            result = fetcher_node(state)

        assert result["summary"] == llm_output, (
            f"Expected summary to be the LLM's output.\n"
            f"  Expected : {llm_output!r}\n"
            f"  Got      : {result['summary']!r}"
        )

    def test_llm_is_called_once(self):
        """The LLM must be invoked exactly once per call."""
        mock_llm = make_mock_llm("Some summary.")
        with patch("agents.fetcher.llm", mock_llm):
            from agents.fetcher import fetcher_node
            state = {"topic": "test topic", "summary": "", "tags": "", "headline": ""}
            fetcher_node(state)

        mock_llm.invoke.assert_called_once()

    def test_summary_is_non_empty_string(self):
        """The summary must be a non-empty string."""
        with patch("agents.fetcher.llm", make_mock_llm("A real summary with content.")):
            from agents.fetcher import fetcher_node
            state = {"topic": "some topic", "summary": "", "tags": "", "headline": ""}
            result = fetcher_node(state)

        assert isinstance(result["summary"], str), "summary must be a string"
        assert len(result["summary"]) > 0, "summary must not be empty"
