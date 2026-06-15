"""
Unit tests for the Wikipedia Service module.
Tests search functionality with mocked Wikipedia API responses.
"""

import pytest
from unittest.mock import patch, MagicMock
import wikipedia as wiki_lib
from src.services.wiki_service import WikiService


MOCK_SUMMARY = (
    "Mars is the fourth planet from the Sun and the second-smallest "
    "planet in the Solar System, being larger than only Mercury."
)


class TestWikiServiceBasic:
    """Basic tests for WikiService."""

    def test_empty_topic_returns_prompt(self, wiki_service):
        result = wiki_service.search("")
        assert "please" in result.lower()

    def test_whitespace_topic_returns_prompt(self, wiki_service):
        result = wiki_service.search("   ")
        assert "please" in result.lower()


class TestWikiServiceSearch:
    """Tests for Wikipedia search with mocked API."""

    @patch("src.services.wiki_service.wikipedia.summary")
    def test_valid_topic_returns_summary(self, mock_summary, wiki_service):
        mock_summary.return_value = MOCK_SUMMARY

        result = wiki_service.search("Mars")

        assert "Mars" in result
        assert "planet" in result
        mock_summary.assert_called_once_with("Mars", sentences=3, auto_suggest=False)

    @patch("src.services.wiki_service.wikipedia.summary")
    def test_page_not_found(self, mock_summary, wiki_service):
        mock_summary.side_effect = wiki_lib.exceptions.PageError("xyz")

        result = wiki_service.search("xyznonexistent")
        assert "couldn't find" in result.lower()

    @patch("src.services.wiki_service.wikipedia.summary")
    def test_disambiguation_picks_first(self, mock_summary, wiki_service):
        # First call raises disambiguation, second call succeeds
        error = wiki_lib.exceptions.DisambiguationError(
            "Python", ["Python (programming)", "Python (snake)", "Monty Python"]
        )
        mock_summary.side_effect = [error, "Python is a programming language."]

        result = wiki_service.search("Python")
        assert "multiple results" in result.lower() or "programming" in result.lower()

    @patch("src.services.wiki_service.wikipedia.summary")
    def test_generic_error(self, mock_summary, wiki_service):
        mock_summary.side_effect = Exception("Network error")

        result = wiki_service.search("Mars")
        assert "unreachable" in result.lower() or "error" in result.lower()

    @patch("src.services.wiki_service.wikipedia.summary")
    def test_topic_stripped(self, mock_summary, wiki_service):
        mock_summary.return_value = MOCK_SUMMARY

        wiki_service.search("  Mars  ")
        mock_summary.assert_called_once_with("Mars", sentences=3, auto_suggest=False)
