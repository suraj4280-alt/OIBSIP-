"""
Unit tests for the Command Handler module.
Tests intent dispatch, service integration, and error handling.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.intent import Intent, IntentType
from src.command_handler import CommandHandler


class TestCommandHandlerDispatch:
    """Tests for intent dispatch routing."""

    def test_greeting_response(self, command_handler):
        intent = Intent(IntentType.GREETING)
        response = command_handler.handle(intent)
        assert len(response) > 0
        assert "Atlas" in response

    def test_time_response(self, command_handler):
        intent = Intent(IntentType.TIME)
        response = command_handler.handle(intent)
        assert "time" in response.lower()

    def test_date_response(self, command_handler):
        intent = Intent(IntentType.DATE)
        response = command_handler.handle(intent)
        assert "Today" in response or "today" in response

    def test_unknown_response(self, command_handler):
        intent = Intent(IntentType.UNKNOWN)
        response = command_handler.handle(intent)
        assert "didn't understand" in response.lower() or "sorry" in response.lower()

    def test_exit_sets_flag(self, command_handler):
        assert command_handler.should_exit is False
        intent = Intent(IntentType.EXIT)
        response = command_handler.handle(intent)
        assert command_handler.should_exit is True
        assert "goodbye" in response.lower() or "bye" in response.lower()


class TestCommandHandlerWeather:
    """Tests for weather command handling."""

    @patch("src.services.weather_service.requests.get")
    def test_weather_with_city(self, mock_get, command_handler):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 25, "feels_like": 23, "humidity": 50},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 3.0},
            "name": "Tokyo",
        }
        mock_get.return_value = mock_response

        intent = Intent(IntentType.WEATHER, params={"city": "Tokyo"})
        response = command_handler.handle(intent)
        assert "Tokyo" in response or "25" in response

    def test_weather_without_city(self, command_handler):
        intent = Intent(IntentType.WEATHER, params={})
        response = command_handler.handle(intent)
        assert "which city" in response.lower()


class TestCommandHandlerWikipedia:
    """Tests for Wikipedia command handling."""

    @patch("src.services.wiki_service.wikipedia.summary")
    def test_wikipedia_with_topic(self, mock_summary, command_handler):
        mock_summary.return_value = "Mars is the fourth planet from the Sun."

        intent = Intent(IntentType.WIKIPEDIA, params={"topic": "Mars"})
        response = command_handler.handle(intent)
        assert "Mars" in response

    def test_wikipedia_without_topic(self, command_handler):
        intent = Intent(IntentType.WIKIPEDIA, params={})
        response = command_handler.handle(intent)
        assert "what" in response.lower() or "search" in response.lower()


class TestCommandHandlerOpenWeb:
    """Tests for open website command handling."""

    @patch("src.command_handler.webbrowser.open")
    def test_known_website(self, mock_open, command_handler):
        intent = Intent(IntentType.OPEN_WEB, params={"site": "youtube"})
        response = command_handler.handle(intent)
        mock_open.assert_called_once()
        assert "youtube" in response.lower()

    def test_unknown_website(self, command_handler):
        intent = Intent(IntentType.OPEN_WEB, params={"site": "nonexistentsite"})
        response = command_handler.handle(intent)
        assert "don't have" in response.lower() or "available" in response.lower()

    def test_no_site_specified(self, command_handler):
        intent = Intent(IntentType.OPEN_WEB, params={})
        response = command_handler.handle(intent)
        assert "which website" in response.lower()


class TestCommandHandlerErrors:
    """Tests for error handling in command dispatch."""

    def test_handles_unexpected_errors(self, command_handler):
        """Handler should not crash on unexpected errors."""
        intent = Intent(IntentType.GREETING)

        # Monkey-patch to force an error
        original_handler = command_handler._dispatch[IntentType.GREETING]
        def raise_error(*args, **kwargs):
            raise RuntimeError("test")
        command_handler._dispatch[IntentType.GREETING] = raise_error

        response = command_handler.handle(intent)
        assert "sorry" in response.lower() or "wrong" in response.lower()

        # Restore
        command_handler._dispatch[IntentType.GREETING] = original_handler
