"""
Command dispatch and execution module for the Voice Assistant.

Routes classified Intent objects to the appropriate service handler
and returns formatted response strings. Implements the Facade pattern
to hide the complexity of the service layer from the orchestrator.

Design Pattern: Dispatch Table
    Uses a dictionary mapping IntentType → handler method for O(1) lookup
    and easy extensibility (add new commands by adding one entry).

Usage:
    handler = CommandHandler(speaker)
    response = handler.handle(intent)
"""

import logging
import webbrowser

from src.intent import Intent, IntentType
from src.speaker import Speaker
from src.services.time_service import TimeService
from src.services.weather_service import WeatherService
from src.services.wiki_service import WikiService
from src.config import ASSISTANT_NAME, WEBSITE_MAP

logger = logging.getLogger(__name__)


class CommandHandler:
    """
    Dispatches classified intents to service handlers and returns responses.

    Acts as a Facade that:
      1. Looks up the handler from a dispatch table.
      2. Calls the handler with intent parameters.
      3. Passes the response to the Speaker.
      4. Returns the response text for GUI display.
      5. Catches and wraps service-level exceptions.
    """

    def __init__(self, speaker: Speaker) -> None:
        """
        Initialize the command handler with all service instances.

        Args:
            speaker: Speaker instance for TTS output.
        """
        self._speaker = speaker
        self._time_service = TimeService()
        self._weather_service = WeatherService()
        self._wiki_service = WikiService()

        # Dispatch table: IntentType → handler method
        self._dispatch: dict = {
            IntentType.GREETING:  self._handle_greeting,
            IntentType.TIME:      self._handle_time,
            IntentType.DATE:      self._handle_date,
            IntentType.WIKIPEDIA: self._handle_wikipedia,
            IntentType.WEATHER:   self._handle_weather,
            IntentType.OPEN_WEB:  self._handle_open_web,
            IntentType.EXIT:      self._handle_exit,
            IntentType.UNKNOWN:   self._handle_unknown,
        }

        self._should_exit = False
        logger.info("CommandHandler initialized with %d handlers", len(self._dispatch))

    @property
    def should_exit(self) -> bool:
        """Check if the exit command has been triggered."""
        return self._should_exit

    def handle(self, intent: Intent) -> str:
        """
        Execute the action for the given intent.

        Looks up the handler from the dispatch table, executes it,
        speaks the response, and returns the response text.

        Args:
            intent: Classified Intent object from IntentClassifier.

        Returns:
            Response text string that was spoken and should be displayed.
        """
        handler = self._dispatch.get(intent.intent_type, self._handle_unknown)

        try:
            # Some handlers need params, some don't; UNKNOWN needs raw text
            if intent.intent_type == IntentType.UNKNOWN:
                response = handler(intent.raw_text)
            elif intent.params:
                response = handler(intent.params)
            else:
                response = handler()

            logger.info(
                "Handled %s -> response: %s",
                intent.intent_type.name,
                response[:80]
            )
            return response

        except ConnectionError as e:
            error_msg = str(e)
            logger.error("Connection error handling %s: %s", intent.intent_type.name, e)
            return error_msg

        except ValueError as e:
            error_msg = str(e)
            logger.error("Value error handling %s: %s", intent.intent_type.name, e)
            return error_msg

        except Exception as e:
            logger.error(
                "Unexpected error handling %s: %s",
                intent.intent_type.name, e,
                exc_info=True,
            )
            return "Sorry, something went wrong. Please try again."

    # ─────────────────────────────────────────────────────────
    # Individual Intent Handlers
    # ─────────────────────────────────────────────────────────

    def _handle_greeting(self) -> str:
        """Handle greeting intents with a time-appropriate response."""
        greeting = self._time_service.get_greeting_by_time()
        return f"{greeting}! I'm {ASSISTANT_NAME}. How can I help you today?"

    def _handle_time(self) -> str:
        """Handle time query intents."""
        return self._time_service.get_current_time()

    def _handle_date(self) -> str:
        """Handle date query intents."""
        return self._time_service.get_current_date()

    def _handle_wikipedia(self, params: dict = None) -> str:
        """
        Handle Wikipedia search intents.

        Args:
            params: Dict with optional 'topic' key.
        """
        params = params or {}
        topic = params.get("topic", "")
        if not topic:
            return "What would you like me to search on Wikipedia?"
        return self._wiki_service.search(topic)

    def _handle_weather(self, params: dict = None) -> str:
        """
        Handle weather query intents.

        Args:
            params: Dict with optional 'city' key.
        """
        params = params or {}
        city = params.get("city", "")
        if not city:
            return "Which city would you like the weather for?"

        try:
            return self._weather_service.get_weather(city)
        except ValueError as e:
            return str(e)
        except ConnectionError as e:
            return str(e)

    def _handle_open_web(self, params: dict = None) -> str:
        """
        Handle open website intents.

        Looks up the site name in the predefined WEBSITE_MAP.
        If found, opens it in the default browser.

        Args:
            params: Dict with optional 'site' key.
        """
        params = params or {}
        site = params.get("site", "").lower().strip()

        if not site:
            return "Which website would you like me to open?"

        # Check if the site name is in our map
        if site in WEBSITE_MAP:
            url = WEBSITE_MAP[site]
            webbrowser.open(url)
            logger.info("Opening website: %s -> %s", site, url)
            return f"Opening {site.title()} for you."

        # Check if any key partially matches
        for name, url in WEBSITE_MAP.items():
            if name in site or site in name:
                webbrowser.open(url)
                logger.info("Opening website (partial match): %s -> %s", site, url)
                return f"Opening {name.title()} for you."

        # Not found in our map
        available = ", ".join(sorted(WEBSITE_MAP.keys()))
        return (
            f"I don't have a URL for '{site}'. "
            f"Available sites: {available}"
        )

    def _handle_exit(self) -> str:
        """Handle exit/quit intents. Sets the should_exit flag."""
        self._should_exit = True
        logger.info("Exit command received.")
        return f"Goodbye! Have a great day. {ASSISTANT_NAME} signing off."

    def _handle_unknown(self, raw_text: str = "") -> str:
        """Handle unrecognized commands by falling back to Wikipedia search."""
        if raw_text:
            logger.info("Unknown command fallback: searching Wikipedia for '%s'", raw_text)
            try:
                # Query Wikipedia using our wiki service
                wiki_response = self._wiki_service.search(raw_text)
                # If it didn't find anything or failed, return the fallback message
                if "couldn't find" in wiki_response or "unreachable" in wiki_response:
                    return (
                        f"I couldn't find anything on Wikipedia for '{raw_text}'. "
                        "You can ask me about the time, date, weather, "
                        "search Wikipedia, or open websites."
                    )
                return wiki_response
            except Exception:
                pass

        return (
            "I'm sorry, I didn't understand that command. "
            "You can ask me about the time, date, weather, "
            "search Wikipedia, or open websites."
        )
