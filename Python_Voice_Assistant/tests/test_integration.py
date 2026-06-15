"""
Integration tests for the Voice Assistant.
Tests the full pipeline: text → classify → handle → response.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.intent import IntentClassifier, IntentType
from src.command_handler import CommandHandler
from src.speaker import Speaker


class TestFullPipeline:
    """Integration tests for the complete command processing pipeline."""

    @pytest.fixture
    def pipeline(self, mock_speaker):
        classifier = IntentClassifier()
        handler = CommandHandler(mock_speaker)
        return classifier, handler

    def test_greeting_end_to_end(self, pipeline):
        classifier, handler = pipeline
        intent = classifier.classify("hello")
        response = handler.handle(intent)
        assert len(response) > 0
        assert "Atlas" in response

    def test_time_end_to_end(self, pipeline):
        classifier, handler = pipeline
        intent = classifier.classify("what time is it")
        response = handler.handle(intent)
        assert "time" in response.lower()

    def test_date_end_to_end(self, pipeline):
        classifier, handler = pipeline
        intent = classifier.classify("what is today's date")
        response = handler.handle(intent)
        assert "Today" in response

    @patch("src.services.weather_service.requests.get")
    def test_weather_end_to_end(self, mock_get, pipeline):
        classifier, handler = pipeline

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 22, "feels_like": 20, "humidity": 55},
            "weather": [{"description": "partly cloudy"}],
            "wind": {"speed": 2.5},
            "name": "Paris",
        }
        mock_get.return_value = mock_response

        intent = classifier.classify("weather in Paris")
        assert intent.intent_type == IntentType.WEATHER
        assert intent.params.get("city") == "Paris"

        response = handler.handle(intent)
        assert "Paris" in response

    @patch("src.services.wiki_service.wikipedia.summary")
    def test_wikipedia_end_to_end(self, mock_summary, pipeline):
        classifier, handler = pipeline
        mock_summary.return_value = "The Moon is Earth's only natural satellite."

        intent = classifier.classify("tell me about the Moon")
        assert intent.intent_type == IntentType.WIKIPEDIA

        response = handler.handle(intent)
        assert "Moon" in response

    @patch("src.command_handler.webbrowser.open")
    def test_open_web_end_to_end(self, mock_open, pipeline):
        classifier, handler = pipeline

        intent = classifier.classify("open youtube")
        assert intent.intent_type == IntentType.OPEN_WEB

        response = handler.handle(intent)
        mock_open.assert_called_once()
        assert "youtube" in response.lower()

    def test_exit_end_to_end(self, pipeline):
        classifier, handler = pipeline

        intent = classifier.classify("goodbye")
        assert intent.intent_type == IntentType.EXIT

        response = handler.handle(intent)
        assert handler.should_exit is True

    def test_unknown_end_to_end(self, pipeline):
        classifier, handler = pipeline

        intent = classifier.classify("asdfghjkl random")
        assert intent.intent_type == IntentType.UNKNOWN

        response = handler.handle(intent)
        assert (
            "sorry" in response.lower() or
            "didn't understand" in response.lower() or
            "couldn't find" in response.lower()
        )

    def test_multiple_commands_sequentially(self, pipeline):
        """Test that the pipeline handles multiple commands in sequence."""
        classifier, handler = pipeline

        commands = [
            ("hello", IntentType.GREETING),
            ("what time is it", IntentType.TIME),
            ("what is today's date", IntentType.DATE),
        ]

        for text, expected_type in commands:
            intent = classifier.classify(text)
            assert intent.intent_type == expected_type
            response = handler.handle(intent)
            assert len(response) > 0
