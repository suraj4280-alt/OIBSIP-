"""
Text-to-Speech module for the Voice Assistant.

Converts text responses to audible speech using the pyttsx3 library.
Uses a dedicated background thread with a fresh pyttsx3 engine created
for each speech request to avoid SAPI5 COM issues on Windows.
"""

import logging
import threading
import queue

import pyttsx3

from src.config import TTS_RATE, TTS_VOLUME

logger = logging.getLogger(__name__)


class Speaker:
    """Handles text-to-speech synthesis via a dedicated background thread."""

    def __init__(self, rate: int = TTS_RATE, volume: float = TTS_VOLUME) -> None:
        """
        Initialize the speaker with a background worker thread.

        Args:
            rate: Speech speed in words per minute (default from config).
            volume: Output volume from 0.0 to 1.0 (default from config).
        """
        self._rate = rate
        self._volume = volume
        self._queue: queue.Queue = queue.Queue()
        self._running = True

        # Start the background worker thread
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()
        logger.info("Speaker thread started successfully (rate=%d, volume=%.1f).", rate, volume)

    def _worker(self) -> None:
        """
        Background worker thread that processes speech requests.
        Creates a fresh pyttsx3 engine for each speech request and
        properly manages COM initialization on Windows to avoid
        SAPI5 silent failures.
        """
        import sys

        while self._running:
            try:
                item = self._queue.get(timeout=1)
            except queue.Empty:
                continue

            if item is None:
                # Shutdown signal
                break

            text, done_event = item
            engine = None
            try:
                # On Windows, initialize COM for this thread on each call
                if sys.platform == "win32":
                    import pythoncom
                    pythoncom.CoInitialize()

                # Create a fresh engine
                engine = pyttsx3.init()
                engine.setProperty("rate", self._rate)
                engine.setProperty("volume", self._volume)

                logger.info("TTS engine speaking: %s", text[:80])
                engine.say(text)
                engine.runAndWait()
                logger.info("TTS engine finished speaking.")
            except Exception as e:
                logger.error("TTS engine error: %s", e)
            finally:
                # Fully clean up the engine to release COM references
                if engine is not None:
                    try:
                        engine.stop()
                    except Exception:
                        pass
                    del engine

                # Uninitialize COM on Windows
                if sys.platform == "win32":
                    try:
                        pythoncom.CoUninitialize()
                    except Exception:
                        pass

                if done_event is not None:
                    done_event.set()

    @property
    def is_available(self) -> bool:
        """Check if the speaker thread is alive."""
        return self._thread is not None and self._thread.is_alive()

    def speak(self, text: str) -> None:
        """
        Convert text to speech asynchronously (does not block).

        Args:
            text: The text content to synthesize and speak.
        """
        if not text or not text.strip():
            return

        if not self.is_available:
            logger.warning("Speaker thread unavailable. Cannot speak: %s", text)
            return

        logger.info("Speaking (async): %s", text[:80])
        self._queue.put((text, None))

    def speak_and_wait(self, text: str) -> None:
        """
        Convert text to speech and block until speaking is complete.

        Args:
            text: The text content to synthesize and speak.
        """
        if not text or not text.strip():
            return

        if not self.is_available:
            logger.warning("Speaker thread unavailable. Cannot speak: %s", text)
            return

        logger.info("Speaking (blocking): %s", text[:80])
        done_event = threading.Event()
        self._queue.put((text, done_event))

        # Wait for speech to complete (with timeout)
        if not done_event.wait(timeout=120):
            logger.warning("Speech timed out after 120s for: %s", text[:80])

    def set_rate(self, rate: int) -> None:
        """Change the speech speed."""
        self._rate = rate
        logger.info("TTS rate changed to %d", rate)

    def set_volume(self, volume: float) -> None:
        """Change the output volume."""
        self._volume = max(0.0, min(1.0, volume))
        logger.info("TTS volume changed to %.1f", self._volume)

    def close(self) -> None:
        """Shut down the background speaker thread."""
        self._running = False
        self._queue.put(None)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3)
