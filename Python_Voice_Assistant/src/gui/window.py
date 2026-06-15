"""
Tkinter GUI module for the Voice Assistant.

Provides a modern dark-themed interface with:
  - Animated header with status indicator
  - Scrollable conversation log with colored messages
  - Text input field with send button
  - Voice listen button and clear button
  - Smooth status transitions and visual feedback

Design: Observer pattern — GUI subscribes to state changes via callbacks.

Usage:
    gui = AssistantGUI(on_listen_callback, on_text_input_callback)
    gui.run()
"""

import logging
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

from src.config import (
    WINDOW_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    THEME,
    FONT_FAMILY,
    FONT_FAMILY_MONO,
    FONT_SIZE_TITLE,
    FONT_SIZE_STATUS,
    FONT_SIZE_CHAT,
    FONT_SIZE_INPUT,
    FONT_SIZE_BUTTON,
    ASSISTANT_NAME,
)

logger = logging.getLogger(__name__)


class AssistantGUI:
    """
    Main GUI window for the Voice Assistant application.

    Provides a professional dark-themed interface with conversation log,
    voice/text input, and real-time status feedback.
    """

    def __init__(self, on_listen_callback=None, on_text_input_callback=None) -> None:
        """
        Initialize the GUI with event callbacks.

        Args:
            on_listen_callback: Function called when "Listen" button is clicked.
                                Should accept no arguments.
            on_text_input_callback: Function called when text is submitted.
                                   Should accept a single string argument.
        """
        self._on_listen = on_listen_callback
        self._on_text_input = on_text_input_callback

        # ── Create root window ──
        self._root = tk.Tk()
        self._root.title(WINDOW_TITLE)
        self._root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self._root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self._root.configure(bg=THEME["bg_primary"])
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Try to set window icon
        try:
            self._root.iconbitmap(default="")
        except Exception:
            pass

        # ── Build the interface ──
        self._create_widgets()
        self._apply_styles()

        # ── State ──
        self._is_listening = False
        self._pulse_active = False

        logger.info("GUI initialized (%dx%d)", WINDOW_WIDTH, WINDOW_HEIGHT)

    @property
    def root(self) -> tk.Tk:
        """Access the root Tk window (for threading with root.after)."""
        return self._root

    # ─────────────────────────────────────────────────────────
    # Widget Creation
    # ─────────────────────────────────────────────────────────

    def _create_widgets(self) -> None:
        """Build and layout all GUI widgets."""

        # ── HEADER BAR ──
        self._header_frame = tk.Frame(
            self._root, bg=THEME["bg_secondary"], pady=12, padx=15
        )
        self._header_frame.pack(fill="x", side="top")

        # Title (left side)
        self._title_label = tk.Label(
            self._header_frame,
            text=f"🎙  {ASSISTANT_NAME}",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            bg=THEME["bg_secondary"],
            fg=THEME["text_primary"],
        )
        self._title_label.pack(side="left")

        # Version tag
        self._version_label = tk.Label(
            self._header_frame,
            text="v1.0",
            font=(FONT_FAMILY, 9),
            bg=THEME["bg_secondary"],
            fg=THEME["text_secondary"],
        )
        self._version_label.pack(side="left", padx=(8, 0), pady=(6, 0))

        # Status indicator (right side)
        self._status_frame = tk.Frame(
            self._header_frame, bg=THEME["bg_secondary"]
        )
        self._status_frame.pack(side="right")

        self._status_dot = tk.Label(
            self._status_frame,
            text="●",
            font=(FONT_FAMILY, 14),
            bg=THEME["bg_secondary"],
            fg=THEME["status_idle"],
        )
        self._status_dot.pack(side="left")

        self._status_label = tk.Label(
            self._status_frame,
            text="Idle",
            font=(FONT_FAMILY, FONT_SIZE_STATUS),
            bg=THEME["bg_secondary"],
            fg=THEME["status_idle"],
        )
        self._status_label.pack(side="left", padx=(4, 0))

        # ── SEPARATOR ──
        separator = tk.Frame(self._root, bg=THEME["accent"], height=2)
        separator.pack(fill="x")

        # ── CONVERSATION LOG ──
        self._chat_frame = tk.Frame(self._root, bg=THEME["bg_primary"])
        self._chat_frame.pack(fill="both", expand=True, padx=12, pady=(8, 4))

        self._chat_log = ScrolledText(
            self._chat_frame,
            bg=THEME["bg_chat"],
            fg=THEME["text_primary"],
            font=(FONT_FAMILY_MONO, FONT_SIZE_CHAT),
            wrap="word",
            state="disabled",
            bd=0,
            relief="flat",
            padx=12,
            pady=10,
            insertbackground=THEME["text_primary"],
            selectbackground=THEME["accent"],
            selectforeground=THEME["text_primary"],
            highlightthickness=1,
            highlightbackground=THEME["accent"],
            highlightcolor=THEME["highlight"],
            cursor="arrow",
        )
        self._chat_log.pack(fill="both", expand=True)

        # Configure text tags for colored messages
        self._chat_log.tag_config(
            "user",
            foreground=THEME["text_user"],
            font=(FONT_FAMILY_MONO, FONT_SIZE_CHAT, "bold"),
        )
        self._chat_log.tag_config(
            "assistant",
            foreground=THEME["text_assistant"],
        )
        self._chat_log.tag_config(
            "error",
            foreground=THEME["text_error"],
        )
        self._chat_log.tag_config(
            "system",
            foreground=THEME["text_system"],
            font=(FONT_FAMILY_MONO, FONT_SIZE_CHAT - 1, "italic"),
        )
        self._chat_log.tag_config(
            "timestamp",
            foreground=THEME["text_secondary"],
            font=(FONT_FAMILY_MONO, FONT_SIZE_CHAT - 2),
        )

        # ── INPUT AREA ──
        self._input_frame = tk.Frame(
            self._root, bg=THEME["bg_primary"], pady=4, padx=12
        )
        self._input_frame.pack(fill="x", side="bottom")

        # Text entry field
        self._text_input = tk.Entry(
            self._input_frame,
            bg=THEME["bg_input"],
            fg=THEME["text_primary"],
            font=(FONT_FAMILY, FONT_SIZE_INPUT),
            insertbackground=THEME["text_primary"],
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=THEME["accent"],
            highlightcolor=THEME["highlight"],
        )
        self._text_input.pack(fill="x", expand=True, side="left", ipady=8, padx=(0, 8))
        self._text_input.bind("<Return>", self._on_send_click)

        # Placeholder text
        self._placeholder_active = True
        self._text_input.insert(0, "Type a command...")
        self._text_input.config(fg=THEME["text_secondary"])
        self._text_input.bind("<FocusIn>", self._on_entry_focus_in)
        self._text_input.bind("<FocusOut>", self._on_entry_focus_out)

        # Send button
        self._send_button = tk.Button(
            self._input_frame,
            text="Send",
            bg=THEME["btn_send"],
            fg="#ffffff",
            font=(FONT_FAMILY, FONT_SIZE_BUTTON, "bold"),
            activebackground=THEME["highlight"],
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            width=8,
            bd=0,
            command=self._on_send_click,
        )
        self._send_button.pack(side="right", ipady=4)

        # ── CONTROL BAR ──
        self._control_frame = tk.Frame(
            self._root, bg=THEME["bg_primary"], pady=10, padx=12
        )
        self._control_frame.pack(fill="x", side="bottom")

        # Listen button
        self._listen_button = tk.Button(
            self._control_frame,
            text="🎤  Listen",
            bg=THEME["highlight"],
            fg="#ffffff",
            font=(FONT_FAMILY, FONT_SIZE_BUTTON + 1, "bold"),
            activebackground=THEME["highlight_hover"],
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            width=14,
            bd=0,
            command=self._on_listen_click,
        )
        self._listen_button.pack(side="left", ipady=6, padx=(0, 8))

        # Clear button
        self._clear_button = tk.Button(
            self._control_frame,
            text="🗑  Clear",
            bg=THEME["btn_clear"],
            fg="#ffffff",
            font=(FONT_FAMILY, FONT_SIZE_BUTTON, "bold"),
            activebackground=THEME["accent"],
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            width=12,
            bd=0,
            command=self.clear_log,
        )
        self._clear_button.pack(side="left", ipady=6)

        # Keyboard shortcut info
        self._shortcut_label = tk.Label(
            self._control_frame,
            text="Enter ↵ to send  •  Ctrl+L to listen",
            font=(FONT_FAMILY, 9),
            bg=THEME["bg_primary"],
            fg=THEME["text_secondary"],
        )
        self._shortcut_label.pack(side="right")

        # ── KEYBOARD SHORTCUTS ──
        self._root.bind("<Control-l>", lambda e: self._on_listen_click())
        self._root.bind("<Control-L>", lambda e: self._on_listen_click())

    def _apply_styles(self) -> None:
        """Apply additional styling and hover effects to buttons."""
        # Listen button hover
        self._listen_button.bind(
            "<Enter>",
            lambda e: self._listen_button.config(bg=THEME["highlight_hover"]),
        )
        self._listen_button.bind(
            "<Leave>",
            lambda e: self._listen_button.config(
                bg=THEME["highlight"] if not self._is_listening else THEME["text_secondary"]
            ),
        )

        # Send button hover
        self._send_button.bind(
            "<Enter>",
            lambda e: self._send_button.config(bg=THEME["highlight"]),
        )
        self._send_button.bind(
            "<Leave>",
            lambda e: self._send_button.config(bg=THEME["btn_send"]),
        )

        # Clear button hover
        self._clear_button.bind(
            "<Enter>",
            lambda e: self._clear_button.config(bg="#1a4f8a"),
        )
        self._clear_button.bind(
            "<Leave>",
            lambda e: self._clear_button.config(bg=THEME["btn_clear"]),
        )

        # Style the scrollbar
        self._chat_log.vbar.config(
            bg=THEME["scrollbar"],
            troughcolor=THEME["bg_chat"],
            activebackground=THEME["accent"],
            width=10,
        )

    # ─────────────────────────────────────────────────────────
    # Public Methods (called from main.py / orchestrator)
    # ─────────────────────────────────────────────────────────

    def update_status(self, status: str, state: str = "idle") -> None:
        """
        Update the status indicator label and dot.

        Args:
            status: Status text (e.g., "Listening...", "Processing...").
            state: One of "idle", "listening", "processing", "speaking", "error".
        """
        color_key = f"status_{state}"
        color = THEME.get(color_key, THEME["status_idle"])

        self._status_dot.config(fg=color)
        self._status_label.config(text=status, fg=color)

        # Pulse animation for listening state
        if state == "listening" and not self._pulse_active:
            self._pulse_active = True
            self._pulse_status_dot()
        elif state != "listening":
            self._pulse_active = False

    def _pulse_status_dot(self) -> None:
        """Animate the status dot with a pulsing effect when listening."""
        if not self._pulse_active:
            self._status_dot.config(fg=THEME["status_idle"])
            return

        current = self._status_dot.cget("fg")
        next_color = (
            THEME["bg_secondary"]
            if current == THEME["status_listening"]
            else THEME["status_listening"]
        )
        self._status_dot.config(fg=next_color)
        self._root.after(600, self._pulse_status_dot)

    def append_message(self, sender: str, message: str, msg_type: str = "assistant") -> None:
        """
        Append a message to the conversation log.

        Args:
            sender: Display name of the message sender (e.g., "You", "Atlas").
            message: The message text content.
            msg_type: One of "user", "assistant", "error", "system".
        """
        self._chat_log.config(state="normal")

        # Timestamp
        timestamp = datetime.now().strftime("%I:%M %p")
        self._chat_log.insert("end", f"  {timestamp}\n", "timestamp")

        # Sender name and message
        self._chat_log.insert("end", f"  {sender}: ", msg_type)
        self._chat_log.insert("end", f"{message}\n\n", msg_type)

        self._chat_log.config(state="disabled")
        self._chat_log.see("end")  # Auto-scroll to bottom

    def clear_log(self) -> None:
        """Clear the conversation log display."""
        self._chat_log.config(state="normal")
        self._chat_log.delete("1.0", "end")
        self._chat_log.config(state="disabled")

        # Show welcome message after clearing
        self._show_welcome()
        logger.info("Conversation log cleared.")

    def set_listening_state(self, is_listening: bool) -> None:
        """
        Update UI to reflect listening/idle state.

        Args:
            is_listening: True when actively listening, False when idle.
        """
        self._is_listening = is_listening
        if is_listening:
            self._listen_button.config(
                text="🎤  Listening...",
                bg=THEME["text_secondary"],
                state="disabled",
            )
            self.update_status("Listening...", "listening")
        else:
            self._listen_button.config(
                text="🎤  Listen",
                bg=THEME["highlight"],
                state="normal",
            )
            self.update_status("Idle", "idle")

    def run(self) -> None:
        """Start the Tkinter main event loop."""
        self._show_welcome()
        logger.info("Starting GUI main loop.")
        self._root.mainloop()

    def close(self) -> None:
        """Destroy the GUI window."""
        try:
            self._root.quit()
            self._root.destroy()
        except Exception:
            pass

    # ─────────────────────────────────────────────────────────
    # Private Event Handlers
    # ─────────────────────────────────────────────────────────

    def _on_listen_click(self) -> None:
        """Handle Listen button click."""
        if self._is_listening:
            return
        if self._on_listen:
            self._on_listen()

    def _on_send_click(self, event=None) -> None:
        """Handle Send button click or Enter key press."""
        text = self._text_input.get().strip()

        # Ignore placeholder text
        if not text or text == "Type a command...":
            return

        self._text_input.delete(0, "end")

        if self._on_text_input:
            self._on_text_input(text)

    def _on_entry_focus_in(self, event=None) -> None:
        """Remove placeholder text when entry gains focus."""
        if self._placeholder_active:
            self._text_input.delete(0, "end")
            self._text_input.config(fg=THEME["text_primary"])
            self._placeholder_active = False

    def _on_entry_focus_out(self, event=None) -> None:
        """Restore placeholder text when entry loses focus and is empty."""
        if not self._text_input.get().strip():
            self._placeholder_active = True
            self._text_input.insert(0, "Type a command...")
            self._text_input.config(fg=THEME["text_secondary"])

    def _on_close(self) -> None:
        """Handle window close (X button)."""
        logger.info("Window close requested.")
        self.close()

    def _show_welcome(self) -> None:
        """Display the welcome message in the conversation log."""
        self._chat_log.config(state="normal")

        welcome = (
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Welcome to {ASSISTANT_NAME} — Voice Assistant\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"  🎤  Click 'Listen' or press Ctrl+L to speak\n"
            f"  ⌨   Type a command below and press Enter\n"
            f"  🌐  Try: \"Open YouTube\", \"Weather in London\"\n"
            f"  📖  Try: \"Tell me about Mars\"\n"
            f"  🕐  Try: \"What time is it?\"\n\n"
        )

        self._chat_log.insert("end", welcome, "system")
        self._chat_log.config(state="disabled")
