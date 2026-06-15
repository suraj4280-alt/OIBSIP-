"""
Application entry point and orchestrator for the Voice Assistant.

Wires all components together:
  Listener → IntentClassifier → CommandHandler → Speaker → GUI

Manages the application lifecycle, threading model, and coordinates
the voice processing pipeline. All blocking I/O (listening, speaking)
runs in daemon threads to keep the GUI responsive.

Usage:
    python -m src.main
"""

import logging
import sys
import threading

from src.config import ASSISTANT_NAME, LOG_FILE, LOG_FORMAT, LOG_LEVEL
from src.listener import Listener
from src.speaker import Speaker
from src.intent import IntentClassifier
from src.command_handler import CommandHandler
from src.gui.window import AssistantGUI

# ─────────────────────────────────────────────────────────────
# Configure Logging
# ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class VoiceAssistant:
    """
    Top-level orchestrator binding all subsystems together.

    Architecture:
        Main Thread:   Tkinter GUI event loop
        Worker Thread: Listen → Classify → Handle → Speak (per command)

    Communication:
        Worker → Main:  via root.after(0, callback) for thread-safe GUI updates
    """

    def __init__(self) -> None:
        """Initialize all components and wire them together."""
        logger.info("=" * 60)
        logger.info("Initializing %s v1.0.0", ASSISTANT_NAME)
        logger.info("=" * 60)

        # ── Core Components ──
        self._speaker = Speaker()
        self._listener = Listener()
        self._classifier = IntentClassifier()
        self._handler = CommandHandler(self._speaker)

        # ── GUI (callbacks wired to our methods) ──
        self._gui = AssistantGUI(
            on_listen_callback=self._on_listen_click,
            on_text_input_callback=self._on_text_input,
        )

        logger.info("All components initialized successfully.")

    def start(self) -> None:
        """
        Launch the Voice Assistant application.

        Speaks a welcome greeting and starts the Tkinter main loop.
        This method blocks until the window is closed.
        """
        logger.info("Starting %s...", ASSISTANT_NAME)

        # Welcome greeting
        from src.services.time_service import TimeService
        greeting = TimeService.get_greeting_by_time()
        welcome_msg = f"{greeting}! I'm {ASSISTANT_NAME}, your voice assistant. How can I help you?"

        self._gui.append_message(ASSISTANT_NAME, welcome_msg, "assistant")
        self._speaker.speak(welcome_msg)

        # Calibrate ambient noise once on startup in a separate background thread
        threading.Thread(target=self._listener.calibrate, args=(1.0,), daemon=True).start()

        # Start the GUI main loop (blocks here)
        self._gui.run()

    def _on_listen_click(self) -> None:
        """
        Handle the Listen button click event.

        Launches the voice processing pipeline in a background thread
        to keep the GUI responsive.
        """
        thread = threading.Thread(target=self._voice_pipeline, daemon=True)
        thread.start()

    def _on_text_input(self, text: str) -> None:
        """
        Handle text input from the entry field.

        Args:
            text: The user's typed command.
        """
        thread = threading.Thread(
            target=self._text_pipeline, args=(text,), daemon=True
        )
        thread.start()

    def _voice_pipeline(self) -> None:
        """
        Full voice processing pipeline (runs in worker thread):
          1. Update GUI → Listening
          2. Capture audio → text
          3. Classify intent
          4. Execute command
          5. Speak response
          6. Update GUI → Idle
        """
        try:
            # Step 1: Update GUI to listening state
            self._gui.root.after(0, lambda: self._gui.set_listening_state(True))

            # Step 2: Listen for speech
            text = self._listener.listen()

            if text == "":
                # Silence / timeout — exit silently without saying anything
                logger.info("Silence detected. Exiting listening state silently.")
                self._gui.root.after(0, lambda: self._gui.set_listening_state(False))
                return

            if text is None:
                # Speech not recognized
                self._gui.root.after(0, lambda: self._gui.update_status(
                    "Not recognized", "error"
                ))
                error_msg = "Sorry, I didn't catch that. Could you please repeat?"
                self._gui.root.after(0, lambda: self._gui.append_message(
                    ASSISTANT_NAME, error_msg, "error"
                ))
                self._speaker.speak_and_wait(error_msg)
                self._gui.root.after(0, lambda: self._gui.set_listening_state(False))
                return

            # Step 3: Display user's speech
            self._gui.root.after(0, lambda t=text: self._gui.append_message(
                "You", t, "user"
            ))

            # Step 4: Process the command
            self._process_command(text)

        except ConnectionError as e:
            error_msg = str(e)
            self._gui.root.after(0, lambda: self._gui.append_message(
                ASSISTANT_NAME, error_msg, "error"
            ))
            self._gui.root.after(0, lambda: self._gui.update_status("Error", "error"))

        except Exception as e:
            logger.error("Voice pipeline error: %s", e, exc_info=True)
            self._gui.root.after(0, lambda: self._gui.append_message(
                ASSISTANT_NAME, "An unexpected error occurred.", "error"
            ))

        finally:
            self._gui.root.after(0, lambda: self._gui.set_listening_state(False))

    def _text_pipeline(self, text: str) -> None:
        """
        Text input processing pipeline (runs in worker thread):
          1. Display user's text
          2. Classify intent
          3. Execute command
          4. Speak response

        Args:
            text: The user's typed command.
        """
        try:
            # Display user's text
            self._gui.root.after(0, lambda: self._gui.append_message(
                "You", text, "user"
            ))

            # Process the command
            self._process_command(text)

        except Exception as e:
            logger.error("Text pipeline error: %s", e, exc_info=True)
            self._gui.root.after(0, lambda: self._gui.append_message(
                ASSISTANT_NAME, "An unexpected error occurred.", "error"
            ))

    def _process_command(self, text: str) -> None:
        """
        Shared command processing logic (used by both voice and text pipelines).

        Steps:
          1. Update status → Processing
          2. Classify the intent
          3. Execute via CommandHandler
          4. Display response
          5. Speak response
          6. Check for exit
          7. Update status → Idle

        Args:
            text: The user's command text (from speech or typing).
        """
        # Status → Processing
        self._gui.root.after(0, lambda: self._gui.update_status(
            "Processing...", "processing"
        ))

        # Classify intent
        intent = self._classifier.classify(text)
        logger.info("Intent: %s", intent)

        # Execute command
        response = self._handler.handle(intent)

        # Display response
        self._gui.root.after(0, lambda r=response: self._gui.append_message(
            ASSISTANT_NAME, r, "assistant"
        ))

        # Speak response
        self._gui.root.after(0, lambda: self._gui.update_status(
            "Speaking...", "speaking"
        ))
        self._speaker.speak_and_wait(response)

        # Check for exit
        if self._handler.should_exit:
            logger.info("Exit command received. Shutting down.")
            self._gui.root.after(1000, self._shutdown)
            return

        # Status → Idle
        self._gui.root.after(0, lambda: self._gui.update_status("Idle", "idle"))

    def _shutdown(self) -> None:
        """Clean up resources and exit the application."""
        logger.info("Shutting down %s...", ASSISTANT_NAME)
        self._gui.close()
        # Close the background speaker process
        try:
            self._speaker.close()
        except Exception as e:
            logger.error("Error closing speaker process: %s", e)
        logger.info("%s shut down complete.", ASSISTANT_NAME)


def main() -> None:
    """Application entry point."""
    import multiprocessing
    multiprocessing.freeze_support()
    try:
        assistant = VoiceAssistant()
        assistant.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    except Exception as e:
        logger.critical("Fatal error: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
