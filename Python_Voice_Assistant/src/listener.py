"""
Speech-to-Text module for the Voice Assistant.

Captures audio from the system microphone and converts it to text
using Google's free Speech Recognition API via the SpeechRecognition library.

The Listener handles:
  - Ambient noise calibration
  - Configurable timeout and phrase limits
  - Graceful error handling for all failure modes

Usage:
    listener = Listener()
    text = listener.listen()  # Returns transcribed text or None
"""

import logging
import speech_recognition as sr

from src.config import (
    RECOGNITION_TIMEOUT,
    PHRASE_TIME_LIMIT,
    RECOGNITION_LANGUAGE,
    AMBIENT_NOISE_DURATION,
    MICROPHONE_INDEX,
)

logger = logging.getLogger(__name__)


class Listener:
    """Handles microphone input and speech recognition."""

    def __init__(self) -> None:
        """Initialize the speech recognizer and microphone."""
        self._recognizer = sr.Recognizer()
        self._language = RECOGNITION_LANGUAGE
        self._timeout = RECOGNITION_TIMEOUT
        self._phrase_limit = PHRASE_TIME_LIMIT
        self._device_index = MICROPHONE_INDEX
        self._is_listening = False

        # Check if microphone is available and list them all
        try:
            mics = sr.Microphone.list_microphone_names()
            self._mic_available = len(mics) > 0
            if self._mic_available:
                logger.info("Listener initialized. Microphones found: %d", len(mics))
                for i, name in enumerate(mics):
                    logger.info("  Index %d: %s", i, name)
                if self._device_index is not None:
                    logger.info("Using configured microphone index: %d", self._device_index)
                else:
                    logger.info("Using default system microphone")
            else:
                logger.warning("No microphone detected!")
        except Exception as e:
            self._mic_available = False
            logger.error("Microphone check failed: %s", e)

    @property
    def is_listening(self) -> bool:
        """Check if the listener is currently capturing audio."""
        return self._is_listening

    @property
    def is_available(self) -> bool:
        """Check if a microphone is available."""
        return self._mic_available

    def listen(self) -> str | None:
        """
        Capture audio from the microphone and convert to text.

        Blocks until speech is detected, recognized, or an error occurs.

        Returns:
            Transcribed text string (lowercased), or None if recognition fails.

        Raises:
            ConnectionError: If the Google Speech API is unreachable.
        """
        if not self._mic_available:
            logger.error("Cannot listen: no microphone available.")
            return None

        self._is_listening = True

        try:
            with sr.Microphone(device_index=self._device_index) as source:
                # Listen for audio
                logger.info("Listening for speech...")
                audio = self._recognizer.listen(
                    source,
                    timeout=self._timeout,
                    phrase_time_limit=self._phrase_limit,
                )

                # Recognize speech using Google's free API
                logger.debug("Sending audio to Google Speech API...")
                text = self._recognizer.recognize_google(
                    audio, language=self._language
                )

                text = text.strip()
                logger.info("Recognized: '%s'", text)
                return text

        except sr.UnknownValueError:
            logger.warning("Speech was unintelligible.")
            return None

        except sr.WaitTimeoutError:
            logger.warning("No speech detected (timeout after %ds).", self._timeout)
            return ""

        except sr.RequestError as e:
            logger.error("Google Speech API unreachable: %s", e)
            raise ConnectionError(
                "Speech recognition service is unavailable. "
                "Please check your internet connection."
            ) from e

        except OSError as e:
            logger.error("Microphone error: %s", e)
            self._mic_available = False
            return None

        except Exception as e:
            logger.error("Unexpected listener error: %s", e)
            return None

        finally:
            self._is_listening = False

    def calibrate(self, duration: float = 1.0) -> None:
        """
        Calibrate the recognizer for ambient noise.

        Call this once before the first listen() for better accuracy.

        Args:
            duration: Seconds of silence to sample (default 1.0).
        """
        if not self._mic_available:
            return

        try:
            with sr.Microphone(device_index=self._device_index) as source:
                logger.info("Calibrating ambient noise (%.1fs) using device index %s...", duration, self._device_index)
                self._recognizer.adjust_for_ambient_noise(source, duration=duration)
                logger.info("Calibration complete. Energy threshold: %f", self._recognizer.energy_threshold)
        except Exception as e:
            logger.error("Calibration failed: %s", e)
