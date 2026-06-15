"""
Unit tests for the Weather Service module.
Tests API integration using mocked HTTP responses.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.services.weather_service import WeatherService


# Mock API response data
MOCK_WEATHER_RESPONSE = {
    "coord": {"lon": -0.1257, "lat": 51.5085},
    "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds"}],
    "main": {
        "temp": 18.5,
        "feels_like": 17.8,
        "humidity": 65,
        "pressure": 1013,
    },
    "wind": {"speed": 4.1, "deg": 250},
    "name": "London",
}


class TestWeatherServiceConfig:
    """Tests for WeatherService configuration."""

    def test_is_configured_with_key(self):
        svc = WeatherService(api_key="valid_key")
        assert svc.is_configured is True

    def test_not_configured_without_key(self):
        svc = WeatherService(api_key="")
        assert svc.is_configured is False

    def test_empty_city_returns_prompt(self, weather_service):
        result = weather_service.get_weather("")
        assert "specify" in result.lower()

    def test_no_api_key_returns_message(self):
        svc = WeatherService(api_key="")
        result = svc.get_weather("London")
        assert "not configured" in result.lower()


class TestWeatherServiceAPI:
    """Tests for weather API calls using mocked responses."""

    @patch("src.services.weather_service.requests.get")
    def test_valid_city_returns_weather(self, mock_get, weather_service):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_WEATHER_RESPONSE
        mock_get.return_value = mock_response

        result = weather_service.get_weather("London")

        assert "London" in result
        assert "18" in result
        assert "scattered clouds" in result
        assert "65" in result

    @patch("src.services.weather_service.requests.get")
    def test_city_not_found_raises_value_error(self, mock_get, weather_service):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="not found"):
            weather_service.get_weather("InvalidCityXYZ123")

    @patch("src.services.weather_service.requests.get")
    def test_invalid_api_key(self, mock_get, weather_service):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        result = weather_service.get_weather("London")
        assert "authentication" in result.lower()

    @patch("src.services.weather_service.requests.get")
    def test_network_error_raises_connection_error(self, mock_get, weather_service):
        mock_get.side_effect = __import__("requests").ConnectionError("Network down")

        with pytest.raises(ConnectionError):
            weather_service.get_weather("London")

    @patch("src.services.weather_service.requests.get")
    def test_timeout_returns_message(self, mock_get, weather_service):
        mock_get.side_effect = __import__("requests").Timeout("Timed out")

        result = weather_service.get_weather("London")
        assert "timed out" in result.lower()

    @patch("src.services.weather_service.requests.get")
    def test_response_includes_feels_like(self, mock_get, weather_service):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_WEATHER_RESPONSE
        mock_get.return_value = mock_response

        result = weather_service.get_weather("London")
        assert "feels like" in result.lower()


class TestWeatherServiceCache:
    """Tests for the caching mechanism."""

    @patch("src.services.weather_service.requests.get")
    def test_second_call_uses_cache(self, mock_get, weather_service):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_WEATHER_RESPONSE
        mock_get.return_value = mock_response

        # First call — hits API
        weather_service.get_weather("London")
        assert mock_get.call_count == 1

        # Second call — should use cache
        weather_service.get_weather("London")
        assert mock_get.call_count == 1  # Still 1, cache hit!

    @patch("src.services.weather_service.requests.get")
    def test_different_cities_not_cached(self, mock_get, weather_service):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_WEATHER_RESPONSE
        mock_get.return_value = mock_response

        weather_service.get_weather("London")
        weather_service.get_weather("Tokyo")
        assert mock_get.call_count == 2  # Two different cities
