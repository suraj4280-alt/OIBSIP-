"""
Configuration constants and settings for the Voice Assistant.

This module centralizes all tunable parameters — API keys, UI constants,
speech settings, and website mappings — into a single importable module.
Implements the Singleton pattern naturally via Python module semantics.

Usage:
    from src.config import ASSISTANT_NAME, WEATHER_API_KEY
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─────────────────────────────────────────────────────────────
# Assistant Identity
# ─────────────────────────────────────────────────────────────
ASSISTANT_NAME: str = "Atlas"
VERSION: str = "1.0.0"

# ─────────────────────────────────────────────────────────────
# API Keys (loaded from .env for security)
# ─────────────────────────────────────────────────────────────
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
WEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"

# Microphone device index selection (loaded from .env)
_mic_index_raw = os.getenv("MICROPHONE_INDEX", "")
MICROPHONE_INDEX: int | None = int(_mic_index_raw) if _mic_index_raw.isdigit() else None

# ─────────────────────────────────────────────────────────────
# Speech Recognition Settings
# ─────────────────────────────────────────────────────────────
RECOGNITION_TIMEOUT: int = 5           # Seconds to wait for speech
PHRASE_TIME_LIMIT: int = 10            # Max seconds per phrase
RECOGNITION_LANGUAGE: str = "en-US"    # Recognition language
AMBIENT_NOISE_DURATION: float = 0.5    # Seconds to calibrate noise

# ─────────────────────────────────────────────────────────────
# Text-to-Speech Settings
# ─────────────────────────────────────────────────────────────
TTS_RATE: int = 175                    # Words per minute
TTS_VOLUME: float = 1.0               # Volume level (0.0 to 1.0)

# ─────────────────────────────────────────────────────────────
# Wikipedia Settings
# ─────────────────────────────────────────────────────────────
WIKI_SENTENCES: int = 3               # Summary sentence count
WIKI_LANGUAGE: str = "en"             # Wikipedia language

# ─────────────────────────────────────────────────────────────
# Website Mappings (name → URL)
# ─────────────────────────────────────────────────────────────
WEBSITE_MAP: dict = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "stackoverflow": "https://www.stackoverflow.com",
    "gmail": "https://mail.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "amazon": "https://www.amazon.com",
    "wikipedia": "https://www.wikipedia.org",
    "netflix": "https://www.netflix.com",
    "spotify": "https://www.spotify.com",
    "whatsapp": "https://web.whatsapp.com",
}

# ─────────────────────────────────────────────────────────────
# GUI Theme Settings
# ─────────────────────────────────────────────────────────────
WINDOW_TITLE: str = "🎙 Voice Assistant"
WINDOW_WIDTH: int = 900
WINDOW_HEIGHT: int = 650
WINDOW_MIN_WIDTH: int = 600
WINDOW_MIN_HEIGHT: int = 450

# Color Palette
THEME = {
    "bg_primary":       "#1a1a2e",     # Deep navy — main background
    "bg_secondary":     "#16213e",     # Dark blue — panels, header
    "bg_chat":          "#0d1117",     # Near-black — conversation log
    "bg_input":         "#16213e",     # Dark blue — input field
    "accent":           "#0f3460",     # Royal blue — buttons, borders
    "highlight":        "#e94560",     # Coral red — listen button, active
    "highlight_hover":  "#d63447",     # Darker coral — button hover
    "text_primary":     "#e0e0e0",     # Light gray — main text
    "text_secondary":   "#a0a0a0",     # Medium gray — subtle text
    "text_user":        "#00d2ff",     # Cyan — user messages
    "text_assistant":   "#00e676",     # Green — assistant messages
    "text_error":       "#ff5252",     # Red — error messages
    "text_system":      "#808080",     # Gray — system messages
    "status_idle":      "#808080",     # Gray — idle status
    "status_listening": "#00e676",     # Green — listening status
    "status_processing":"#ffc107",     # Amber — processing status
    "status_speaking":  "#2196f3",     # Blue — speaking status
    "status_error":     "#ff5252",     # Red — error status
    "btn_send":         "#0f3460",     # Royal blue — send button
    "btn_clear":        "#0f3460",     # Royal blue — clear button
    "scrollbar":        "#2a2a4a",     # Dark purple — scrollbar
}

# Typography
FONT_FAMILY: str = "Segoe UI"
FONT_FAMILY_MONO: str = "Consolas"
FONT_SIZE_TITLE: int = 18
FONT_SIZE_STATUS: int = 11
FONT_SIZE_CHAT: int = 12
FONT_SIZE_INPUT: int = 12
FONT_SIZE_BUTTON: int = 11

# ─────────────────────────────────────────────────────────────
# Logging Settings
# ─────────────────────────────────────────────────────────────
LOG_FILE: str = "voice_assistant.log"
LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_LEVEL: str = "INFO"
