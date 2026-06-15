"""
Weather information service module for the Voice Assistant.

Fetches current weather data from the OpenWeatherMap API and formats it
into natural language responses. Includes a simple TTL-based cache to
avoid redundant API calls for the same city within 5 minutes.

Usage:
    weather_svc = WeatherService(api_key="your_key")
    print(weather_svc.get_weather("London"))
    # "The weather in London is currently 18°C with scattered clouds.
    #  Humidity is 65% and wind speed is 4.1 m/s."
"""

import logging
from datetime import datetime, timedelta

import requests

from src.config import WEATHER_API_KEY, WEATHER_BASE_URL

logger = logging.getLogger(__name__)

# Cache TTL in seconds (5 minutes)
CACHE_TTL: int = 300


class WeatherService:
    """Provides weather query functionality via OpenWeatherMap API."""

    def __init__(self, api_key: str = WEATHER_API_KEY) -> None:
        """
        Initialize with the OpenWeatherMap API key.

        Args:
            api_key: Your OpenWeatherMap API key. Defaults to config value.
        """
        self._api_key = api_key
        self._base_url = WEATHER_BASE_URL
        self._cache: dict[str, tuple[datetime, str]] = {}

        if not self._api_key:
            logger.warning(
                "Weather API key is not set. "
                "Set WEATHER_API_KEY in your .env file."
            )

    @property
    def is_configured(self) -> bool:
        """Check if the API key is set."""
        return bool(self._api_key)

    def get_weather(self, city: str) -> str:
        """
        Fetch and return formatted weather for the given city.

        Results are cached for 5 minutes to reduce API calls.

        Args:
            city: City name to query weather for (case-insensitive).

        Returns:
            Formatted weather description string.

        Raises:
            ValueError: If the city is not found (HTTP 404).
            ConnectionError: If the API is unreachable.
        """
        if not city or not city.strip():
            return "Please specify a city name for the weather."

        if not self.is_configured:
            return ("Weather service is not configured. "
                    "Please set your WEATHER_API_KEY in the .env file.")

        city = city.strip()
        cache_key = city.lower()

        # Check cache
        cached = self._get_from_cache(cache_key)
        if cached:
            logger.info("Weather cache hit for '%s'", city)
            return cached

        # Fetch from API
        try:
            params = {
                "q": city,
                "appid": self._api_key,
                "units": "metric",
            }
            logger.info("Fetching weather for '%s'...", city)
            response = requests.get(
                self._base_url, params=params, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                result = self._parse_response(data)
                self._set_cache(cache_key, result)
                return result

            elif response.status_code == 404:
                logger.warning("City not found: '%s'", city)
                raise ValueError(f"City '{city}' not found.")

            elif response.status_code == 401:
                logger.error("Invalid API key")
                return "Weather service authentication failed. Check your API key."

            else:
                logger.error("Weather API error: HTTP %d", response.status_code)
                return f"Weather service returned an error (code {response.status_code})."

        except requests.ConnectionError:
            logger.error("Network error while fetching weather")
            raise ConnectionError(
                "Could not connect to the weather service. "
                "Please check your internet connection."
            )

        except requests.Timeout:
            logger.error("Weather API timeout")
            return "Weather service timed out. Please try again."

        except ValueError:
            raise  # Re-raise city-not-found errors

        except Exception as e:
            logger.error("Unexpected weather error: %s", e)
            return "An unexpected error occurred while fetching weather."

    def _parse_response(self, data: dict) -> str:
        """
        Parse the OpenWeatherMap JSON response into a human-readable string.

        Args:
            data: The parsed JSON response dictionary.

        Returns:
            Formatted weather description.
        """
        city_name = data.get("name", "Unknown")
        temp = data.get("main", {}).get("temp", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        description = data.get("weather", [{}])[0].get("description", "N/A")
        wind_speed = data.get("wind", {}).get("speed", "N/A")
        feels_like = data.get("main", {}).get("feels_like", "N/A")

        response = (
            f"The weather in {city_name} is currently "
            f"{temp}°C with {description}. "
            f"It feels like {feels_like}°C. "
            f"Humidity is {humidity}% and wind speed is {wind_speed} m/s."
        )
        logger.info("Weather response: %s", response[:80])
        return response

    def _get_from_cache(self, key: str) -> str | None:
        """
        Get a cached weather result if still valid.

        Args:
            key: Lowercased city name.

        Returns:
            Cached result string, or None if expired/missing.
        """
        if key in self._cache:
            cached_time, cached_result = self._cache[key]
            if datetime.now() - cached_time < timedelta(seconds=CACHE_TTL):
                return cached_result
            else:
                del self._cache[key]
        return None

    def _set_cache(self, key: str, value: str) -> None:
        """
        Store a weather result in the cache.

        Args:
            key: Lowercased city name.
            value: The formatted weather string.
        """
        self._cache[key] = (datetime.now(), value)
