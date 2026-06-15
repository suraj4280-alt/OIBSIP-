"""
Intent Classification module for the Voice Assistant.

Maps user utterances to predefined intent categories using keyword matching.
Each classified intent includes the type, extracted parameters, confidence
score, and the original raw text.

Supported Intents:
    GREETING  — "hello", "hi", "hey", "good morning"
    TIME      — "what time", "current time", "clock"
    DATE      — "what date", "today's date", "what day"
    WIKIPEDIA — "tell me about", "who is", "what is", "search for"
    WEATHER   — "weather in", "temperature", "forecast"
    OPEN_WEB  — "open youtube", "launch google"
    EXIT      — "exit", "quit", "bye", "goodbye"
    UNKNOWN   — anything that doesn't match

Usage:
    classifier = IntentClassifier()
    intent = classifier.classify("What's the weather in Tokyo?")
    print(intent.intent_type)  # IntentType.WEATHER
    print(intent.params)       # {"city": "Tokyo"}
"""

import logging
import re
from enum import Enum, auto

logger = logging.getLogger(__name__)


class IntentType(Enum):
    """Enumeration of all supported intent categories."""
    GREETING  = auto()
    TIME      = auto()
    DATE      = auto()
    WIKIPEDIA = auto()
    WEATHER   = auto()
    OPEN_WEB  = auto()
    EXIT      = auto()
    UNKNOWN   = auto()


class Intent:
    """
    Represents a classified intent with extracted parameters.

    Attributes:
        intent_type: The IntentType category.
        params: Dictionary of extracted parameters (e.g., city, topic).
        confidence: Float 0.0–1.0 indicating match confidence.
        raw_text: The original user text that was classified.
    """

    def __init__(
        self,
        intent_type: IntentType,
        params: dict | None = None,
        confidence: float = 0.0,
        raw_text: str = "",
    ) -> None:
        self.intent_type = intent_type
        self.params = params if params is not None else {}
        self.confidence = confidence
        self.raw_text = raw_text

    def __repr__(self) -> str:
        return (
            f"Intent(type={self.intent_type.name}, "
            f"params={self.params}, "
            f"confidence={self.confidence:.2f})"
        )


class IntentClassifier:
    """
    Classifies user text into Intent objects using keyword matching.

    The classifier uses an ordered keyword map — the first match wins.
    More specific keywords are listed before generic ones to improve
    accuracy (e.g., "tell me about" before "tell").
    """

    # Ordered list of (IntentType, keywords) — first match wins.
    # Keywords are checked with "keyword in text", so more specific
    # phrases should come first within each intent.
    KEYWORD_MAP: list[tuple[IntentType, list[str]]] = [
        (IntentType.EXIT, [
            "exit", "quit", "bye", "goodbye", "good bye",
            "stop", "shut down", "shutdown", "close",
        ]),
        (IntentType.GREETING, [
            "good morning", "good afternoon", "good evening",
            "hello", "hi there", "hey there", "hi", "hey", "howdy",
        ]),
        (IntentType.WEATHER, [
            "weather in", "weather for", "weather at",
            "temperature in", "temperature for",
            "how hot in", "how cold in",
            "forecast for", "forecast in",
            "weather", "temperature", "forecast",
        ]),
        (IntentType.WIKIPEDIA, [
            "tell me about", "search for", "who is", "who was",
            "what is", "what are", "what was",
            "look up", "wikipedia", "define",
        ]),
        (IntentType.TIME, [
            "what is the time", "what time", "current time", "time now",
            "what's the time", "tell me the time",
            "time please", "time",
        ]),
        (IntentType.DATE, [
            "what is the date", "what's the date", "what date", "today's date",
            "current date", "what day", "which day",
            "date today", "date",
        ]),
        (IntentType.OPEN_WEB, [
            "open", "launch", "go to", "navigate to",
            "browse", "visit", "start",
        ]),
    ]

    def classify(self, text: str) -> Intent:
        """
        Classify the given text into an Intent.

        The text is normalized (lowercased, stripped) and then matched
        against the keyword map. Uses word-boundary matching and selects
        the longest matched keyword to ensure high specificity.

        Args:
            text: User's transcribed speech or typed command.

        Returns:
            Intent object with type, extracted params, and confidence.
        """
        if not text or not text.strip():
            return Intent(IntentType.UNKNOWN, confidence=0.0, raw_text="")

        normalized = self._normalize(text)

        best_keyword_len = -1
        best_intent_type = None
        best_keyword = None

        for intent_type, keywords in self.KEYWORD_MAP:
            for keyword in keywords:
                # Use word-boundary regex to avoid matching substrings of other words (e.g. 'hi' in 'machine')
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, normalized):
                    if len(keyword) > best_keyword_len:
                        best_keyword_len = len(keyword)
                        best_intent_type = intent_type
                        best_keyword = keyword

        if best_intent_type is not None:
            params = self._extract_params(best_intent_type, normalized, best_keyword)
            confidence = best_keyword_len / max(len(normalized), 1)
            intent = Intent(
                intent_type=best_intent_type,
                params=params,
                confidence=min(confidence, 1.0),
                raw_text=text,
            )
            logger.info("Classified: '%s' -> %s", text, intent)
            return intent

        logger.info("Classified: '%s' -> UNKNOWN", text)
        return Intent(IntentType.UNKNOWN, confidence=0.0, raw_text=text)

    def _normalize(self, text: str) -> str:
        """
        Normalize user text for classification.

        Args:
            text: Raw user text.

        Returns:
            Lowercased, stripped text.
        """
        return text.lower().strip()

    def _extract_params(
        self, intent_type: IntentType, text: str, matched_keyword: str
    ) -> dict:
        """
        Extract relevant parameters based on the intent type.

        Args:
            intent_type: The classified intent category.
            text: Normalized user text.
            matched_keyword: The keyword that triggered the match.

        Returns:
            Dictionary of extracted parameters.
        """
        params = {}

        if intent_type == IntentType.WEATHER:
            # Extract city name after location prepositions
            city = self._extract_after_phrases(text, [
                "weather in ", "weather for ", "weather at ",
                "temperature in ", "temperature for ",
                "how hot in ", "how cold in ",
                "forecast for ", "forecast in ",
            ])
            if city:
                params["city"] = city.strip().title()

        elif intent_type == IntentType.WIKIPEDIA:
            # Extract topic after trigger phrases
            topic = self._extract_after_phrases(text, [
                "tell me about ", "search for ", "who is ", "who was ",
                "what is ", "what are ", "what was ",
                "look up ", "define ",
            ])
            if topic:
                params["topic"] = topic.strip()

        elif intent_type == IntentType.OPEN_WEB:
            # Extract website name after trigger words
            site = self._extract_after_phrases(text, [
                "open ", "launch ", "go to ", "navigate to ",
                "browse ", "visit ", "start ",
            ])
            if site:
                params["site"] = site.strip().lower()

        return params

    def _extract_after_phrases(self, text: str, phrases: list[str]) -> str | None:
        """
        Extract text appearing after the first matching phrase.

        Args:
            text: The normalized user text.
            phrases: List of trigger phrases to search for.

        Returns:
            The text after the matched phrase, or None if no match.
        """
        for phrase in phrases:
            if phrase in text:
                # Get everything after the phrase
                _, _, remainder = text.partition(phrase)
                remainder = remainder.strip()
                if remainder:
                    return remainder
        return None
