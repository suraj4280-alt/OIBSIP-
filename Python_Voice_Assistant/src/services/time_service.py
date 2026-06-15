"""
Time and Date service module for the Voice Assistant.

Provides formatted current time, date, and time-appropriate greetings
using Python's built-in datetime module. Fully offline — no network required.

Usage:
    time_svc = TimeService()
    print(time_svc.get_current_time())      # "The current time is 3:45 PM"
    print(time_svc.get_current_date())      # "Today is Wednesday, June 11, 2026"
    print(time_svc.get_greeting_by_time())  # "Good afternoon"
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TimeService:
    """Provides time and date query functionality."""

    @staticmethod
    def get_current_time(format_24h: bool = False) -> str:
        """
        Return the current local time as a formatted string.

        Args:
            format_24h: If True, use 24-hour format. Otherwise 12-hour AM/PM.

        Returns:
            Human-readable time string.
            Example: "The current time is 3:45 PM"
        """
        now = datetime.now()
        if format_24h:
            time_str = now.strftime("%H:%M")
        else:
            time_str = now.strftime("%I:%M %p").lstrip("0")

        response = f"The current time is {time_str}"
        logger.info("Time query: %s", response)
        return response

    @staticmethod
    def get_current_date(include_day: bool = True) -> str:
        """
        Return the current local date as a formatted string.

        Args:
            include_day: If True, include the day name (e.g., "Wednesday").

        Returns:
            Human-readable date string.
            Example: "Today is Wednesday, June 11, 2026"
        """
        now = datetime.now()
        if include_day:
            date_str = now.strftime("%A, %B %d, %Y")
        else:
            date_str = now.strftime("%B %d, %Y")

        response = f"Today is {date_str}"
        logger.info("Date query: %s", response)
        return response

    @staticmethod
    def get_greeting_by_time() -> str:
        """
        Return a time-appropriate greeting.

        Returns:
            "Good morning"   — 5:00 AM to 11:59 AM
            "Good afternoon" — 12:00 PM to 5:59 PM
            "Good evening"   — 6:00 PM to 4:59 AM
        """
        hour = datetime.now().hour

        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        logger.debug("Time-based greeting: %s (hour=%d)", greeting, hour)
        return greeting
