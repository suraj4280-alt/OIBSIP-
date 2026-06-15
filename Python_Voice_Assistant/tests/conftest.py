"""
Shared pytest fixtures for the Voice Assistant test suite.
"""

import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Inject mock API key for tests so that services like WeatherService initialize correctly
import src.config
src.config.WEATHER_API_KEY = "test_api_key_12345"


@pytest.fixture
def mock_speaker():
    """Create a mocked Speaker that doesn't produce audio."""
    speaker = MagicMock()
    speaker.is_available = True
    speaker.speak = MagicMock()
    speaker.speak_and_wait = MagicMock()
    return speaker


@pytest.fixture
def classifier():
    """Create an IntentClassifier instance."""
    from src.intent import IntentClassifier
    return IntentClassifier()


@pytest.fixture
def time_service():
    """Create a TimeService instance."""
    from src.services.time_service import TimeService
    return TimeService()


@pytest.fixture
def weather_service():
    """Create a WeatherService with a test API key."""
    from src.services.weather_service import WeatherService
    return WeatherService(api_key="test_api_key_12345")


@pytest.fixture
def wiki_service():
    """Create a WikiService instance."""
    from src.services.wiki_service import WikiService
    return WikiService()


@pytest.fixture
def command_handler(mock_speaker):
    """Create a CommandHandler with a mocked Speaker."""
    from src.command_handler import CommandHandler
    return CommandHandler(mock_speaker)
