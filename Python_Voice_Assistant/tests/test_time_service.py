"""
Unit tests for the Time Service module.
"""

import pytest
from unittest.mock import patch
from datetime import datetime
from src.services.time_service import TimeService


class TestGetCurrentTime:
    """Tests for get_current_time()."""

    def test_returns_string(self, time_service):
        result = time_service.get_current_time()
        assert isinstance(result, str)

    def test_contains_time_prefix(self, time_service):
        result = time_service.get_current_time()
        assert "The current time is" in result

    def test_12h_format_contains_am_or_pm(self, time_service):
        result = time_service.get_current_time(format_24h=False)
        assert "AM" in result or "PM" in result

    def test_24h_format_no_am_pm(self, time_service):
        result = time_service.get_current_time(format_24h=True)
        assert "AM" not in result and "PM" not in result


class TestGetCurrentDate:
    """Tests for get_current_date()."""

    def test_returns_string(self, time_service):
        result = time_service.get_current_date()
        assert isinstance(result, str)

    def test_contains_today_prefix(self, time_service):
        result = time_service.get_current_date()
        assert "Today is" in result

    def test_includes_day_name(self, time_service):
        result = time_service.get_current_date(include_day=True)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]
        assert any(day in result for day in days)

    def test_includes_year(self, time_service):
        result = time_service.get_current_date()
        current_year = str(datetime.now().year)
        assert current_year in result


class TestGetGreetingByTime:
    """Tests for get_greeting_by_time()."""

    @patch("src.services.time_service.datetime")
    def test_morning_greeting(self, mock_dt):
        mock_dt.now.return_value = datetime(2026, 6, 11, 9, 0, 0)
        result = TimeService.get_greeting_by_time()
        assert result == "Good morning"

    @patch("src.services.time_service.datetime")
    def test_afternoon_greeting(self, mock_dt):
        mock_dt.now.return_value = datetime(2026, 6, 11, 14, 0, 0)
        result = TimeService.get_greeting_by_time()
        assert result == "Good afternoon"

    @patch("src.services.time_service.datetime")
    def test_evening_greeting(self, mock_dt):
        mock_dt.now.return_value = datetime(2026, 6, 11, 20, 0, 0)
        result = TimeService.get_greeting_by_time()
        assert result == "Good evening"

    @patch("src.services.time_service.datetime")
    def test_late_night_greeting(self, mock_dt):
        mock_dt.now.return_value = datetime(2026, 6, 11, 2, 0, 0)
        result = TimeService.get_greeting_by_time()
        assert result == "Good evening"

    @patch("src.services.time_service.datetime")
    def test_boundary_noon(self, mock_dt):
        mock_dt.now.return_value = datetime(2026, 6, 11, 12, 0, 0)
        result = TimeService.get_greeting_by_time()
        assert result == "Good afternoon"

    @patch("src.services.time_service.datetime")
    def test_boundary_6pm(self, mock_dt):
        mock_dt.now.return_value = datetime(2026, 6, 11, 18, 0, 0)
        result = TimeService.get_greeting_by_time()
        assert result == "Good evening"
