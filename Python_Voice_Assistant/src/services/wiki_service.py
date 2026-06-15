"""
Wikipedia search service module for the Voice Assistant.

Queries the Wikipedia API for article summaries using the `wikipedia`
Python library. Handles disambiguation (multiple results), missing pages,
and network errors gracefully.

Usage:
    wiki_svc = WikiService()
    print(wiki_svc.search("Albert Einstein"))
    # "Albert Einstein was a German-born theoretical physicist..."
"""

import logging

import wikipedia

from src.config import WIKI_SENTENCES, WIKI_LANGUAGE

logger = logging.getLogger(__name__)


class WikiService:
    """Provides Wikipedia search and summary functionality."""

    def __init__(
        self,
        sentences: int = WIKI_SENTENCES,
        language: str = WIKI_LANGUAGE,
    ) -> None:
        """
        Initialize the Wikipedia service.

        Args:
            sentences: Number of sentences to include in summaries (default 3).
            language: Wikipedia language code (default "en").
        """
        self._sentences = sentences
        self._language = language
        wikipedia.set_lang(self._language)
        # Set a custom user-agent to comply with Wikimedia API requirements and avoid blocking
        wikipedia.set_user_agent("AtlasVoiceAssistant/1.0 (contact: support@atlasassistant.local)")
        logger.info(
            "WikiService initialized (sentences=%d, lang=%s)",
            sentences, language
        )

    def search(self, topic: str) -> str:
        """
        Search Wikipedia and return an article summary.

        Handles three scenarios:
          1. Exact match found → returns summary
          2. Disambiguation → picks the first option and returns its summary
          3. No results → returns a friendly error message

        Args:
            topic: The search query / topic to look up.

        Returns:
            Summary text string, or an error message if lookup fails.
        """
        if not topic or not topic.strip():
            return "Please tell me what topic you'd like to know about."

        topic = topic.strip()
        logger.info("Wikipedia search: '%s'", topic)

        try:
            summary = wikipedia.summary(topic, sentences=self._sentences, auto_suggest=False)
            logger.info("Wikipedia result: %s...", summary[:80])
            return summary

        except wikipedia.exceptions.PageError:
            logger.warning("Wikipedia page not found: '%s'", topic)
            return f"I couldn't find a Wikipedia article on '{topic}'."

        except wikipedia.exceptions.DisambiguationError as e:
            # Multiple results found — try the first suggestion
            logger.info(
                "Wikipedia disambiguation for '%s'. Options: %s",
                topic, e.options[:5]
            )
            try:
                first_option = e.options[0]
                summary = wikipedia.summary(first_option, sentences=self._sentences, auto_suggest=False)
                return (
                    f"There were multiple results. "
                    f"Here's what I found for '{first_option}': {summary}"
                )
            except Exception:
                return (
                    f"I found multiple results for '{topic}' but couldn't "
                    f"get a clear answer. Try being more specific."
                )

        except Exception as e:
            logger.error("Wikipedia error: %s", e)
            return "Wikipedia is currently unreachable. Please try again later."
