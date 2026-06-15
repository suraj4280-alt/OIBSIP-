"""
Unit tests for the Intent Classification module.

Tests all 8 intent types, parameter extraction, edge cases,
case insensitivity, and unknown input handling.
"""

import pytest
from src.intent import IntentClassifier, IntentType, Intent


class TestIntentType:
    """Tests for the IntentType enum."""

    def test_all_intents_exist(self):
        expected = [
            "GREETING", "TIME", "DATE", "WIKIPEDIA",
            "WEATHER", "OPEN_WEB", "EXIT", "UNKNOWN"
        ]
        actual = [i.name for i in IntentType]
        for name in expected:
            assert name in actual, f"Missing IntentType: {name}"

    def test_intent_values_unique(self):
        values = [i.value for i in IntentType]
        assert len(values) == len(set(values)), "IntentType values must be unique"


class TestIntentObject:
    """Tests for the Intent data class."""

    def test_default_values(self):
        intent = Intent(IntentType.UNKNOWN)
        assert intent.intent_type == IntentType.UNKNOWN
        assert intent.params == {}
        assert intent.confidence == 0.0
        assert intent.raw_text == ""

    def test_with_params(self):
        intent = Intent(IntentType.WEATHER, params={"city": "London"}, confidence=0.8)
        assert intent.params["city"] == "London"
        assert intent.confidence == 0.8

    def test_repr(self):
        intent = Intent(IntentType.GREETING, confidence=0.5)
        repr_str = repr(intent)
        assert "GREETING" in repr_str
        assert "0.50" in repr_str


class TestClassifyGreeting:
    """Tests for greeting intent classification."""

    @pytest.mark.parametrize("text", [
        "hello", "hi", "hey", "hi there", "hey there",
        "good morning", "good afternoon", "good evening",
        "Hello!", "HI THERE", "  hello  ",
    ])
    def test_greeting_variants(self, classifier, text):
        intent = classifier.classify(text)
        assert intent.intent_type == IntentType.GREETING

    def test_greeting_has_no_params(self, classifier):
        intent = classifier.classify("hello")
        assert intent.params == {}


class TestClassifyTime:
    """Tests for time query intent classification."""

    @pytest.mark.parametrize("text", [
        "what time is it",
        "current time",
        "time now",
        "what's the time",
        "tell me the time",
        "time please",
        "WHAT TIME IS IT",
    ])
    def test_time_variants(self, classifier, text):
        intent = classifier.classify(text)
        assert intent.intent_type == IntentType.TIME


class TestClassifyDate:
    """Tests for date query intent classification."""

    @pytest.mark.parametrize("text", [
        "what's the date",
        "today's date",
        "what day is it",
        "current date",
        "date today",
    ])
    def test_date_variants(self, classifier, text):
        intent = classifier.classify(text)
        assert intent.intent_type == IntentType.DATE


class TestClassifyWeather:
    """Tests for weather intent classification and parameter extraction."""

    @pytest.mark.parametrize("text,expected_city", [
        ("weather in London", "London"),
        ("weather in New York", "New York"),
        ("weather for Tokyo", "Tokyo"),
        ("what's the temperature in Paris", "Paris"),
        ("forecast for Mumbai", "Mumbai"),
    ])
    def test_weather_with_city(self, classifier, text, expected_city):
        intent = classifier.classify(text)
        assert intent.intent_type == IntentType.WEATHER
        assert intent.params.get("city") == expected_city

    def test_weather_without_city(self, classifier):
        intent = classifier.classify("weather")
        assert intent.intent_type == IntentType.WEATHER

    def test_weather_case_insensitive(self, classifier):
        intent = classifier.classify("WEATHER IN LONDON")
        assert intent.intent_type == IntentType.WEATHER


class TestClassifyWikipedia:
    """Tests for Wikipedia intent classification and parameter extraction."""

    @pytest.mark.parametrize("text,expected_topic", [
        ("tell me about Mars", "mars"),
        ("who is Albert Einstein", "albert einstein"),
        ("what is Python", "python"),
        ("search for machine learning", "machine learning"),
    ])
    def test_wikipedia_with_topic(self, classifier, text, expected_topic):
        intent = classifier.classify(text)
        assert intent.intent_type == IntentType.WIKIPEDIA
        assert intent.params.get("topic") == expected_topic

    def test_wikipedia_without_topic(self, classifier):
        intent = classifier.classify("tell me about")
        assert intent.intent_type == IntentType.WIKIPEDIA


class TestClassifyOpenWeb:
    """Tests for open website intent classification and parameter extraction."""

    @pytest.mark.parametrize("text,expected_site", [
        ("open youtube", "youtube"),
        ("launch google", "google"),
        ("go to github", "github"),
    ])
    def test_open_web_with_site(self, classifier, text, expected_site):
        intent = classifier.classify(text)
        assert intent.intent_type == IntentType.OPEN_WEB
        assert intent.params.get("site") == expected_site


class TestClassifyExit:
    """Tests for exit intent classification."""

    @pytest.mark.parametrize("text", [
        "exit", "quit", "bye", "goodbye",
        "stop", "shut down", "close",
    ])
    def test_exit_variants(self, classifier, text):
        intent = classifier.classify(text)
        assert intent.intent_type == IntentType.EXIT


class TestClassifyUnknown:
    """Tests for unknown/unrecognized input."""

    @pytest.mark.parametrize("text", [
        "asdfghjkl",
        "random nonsense here",
        "play some music",
        "12345",
    ])
    def test_unknown_input(self, classifier, text):
        intent = classifier.classify(text)
        assert intent.intent_type == IntentType.UNKNOWN

    def test_empty_string(self, classifier):
        intent = classifier.classify("")
        assert intent.intent_type == IntentType.UNKNOWN

    def test_none_handled(self, classifier):
        intent = classifier.classify(None)
        assert intent.intent_type == IntentType.UNKNOWN

    def test_whitespace_only(self, classifier):
        intent = classifier.classify("   ")
        assert intent.intent_type == IntentType.UNKNOWN


class TestClassifyConfidence:
    """Tests for confidence scoring."""

    def test_confidence_between_zero_and_one(self, classifier):
        intent = classifier.classify("hello")
        assert 0.0 <= intent.confidence <= 1.0

    def test_unknown_has_zero_confidence(self, classifier):
        intent = classifier.classify("asdfghjkl")
        assert intent.confidence == 0.0

    def test_longer_keyword_higher_confidence(self, classifier):
        short = classifier.classify("hi there buddy")
        long_ = classifier.classify("good morning")
        # "good morning" keyword is more specific
        assert long_.confidence >= short.confidence
