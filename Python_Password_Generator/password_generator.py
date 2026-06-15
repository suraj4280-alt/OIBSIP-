"""
Random Password Generator — Oasis Infobyte Internship Task
===========================================================

A desktop application that generates secure random passwords
with a modern dark-themed GUI built using Python and Tkinter.

Features:
    - Adjustable password length (4-32 characters)
    - Checkboxes for character types (uppercase, lowercase, numbers, symbols)
    - Password strength indicator (Weak / Medium / Strong)
    - Copy to clipboard functionality
    - Clean, modern dark theme GUI

Author: Suraj
"""

# ──────────────────────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────────────────────
import random       # For generating random characters
import string       # For character sets (letters, digits, symbols)
import tkinter as tk                    # Main GUI library
from tkinter import messagebox, font    # Pop-up messages & custom fonts


# ──────────────────────────────────────────────────────────────
# Color Theme (Dark Modern Theme)
# ──────────────────────────────────────────────────────────────
COLORS = {
    "bg_dark":      "#1a1a2e",    # Main background (dark navy)
    "bg_card":      "#16213e",    # Card/panel background
    "bg_input":     "#0f3460",    # Input field background
    "accent":       "#e94560",    # Primary accent (red-pink)
    "accent_hover": "#ff6b6b",    # Accent hover state
    "text_white":   "#ffffff",    # White text
    "text_light":   "#b8c5d6",    # Light grey text
    "text_muted":   "#6c7a8d",    # Muted/dimmed text
    "success":      "#2ecc71",    # Green (strong password)
    "warning":      "#f39c12",    # Orange (medium password)
    "danger":       "#e74c3c",    # Red (weak password)
    "border":       "#2a3a5c",    # Border color
    "copy_btn":     "#0ea5e9",    # Copy button (blue)
    "copy_hover":   "#38bdf8",    # Copy button hover
}


# ──────────────────────────────────────────────────────────────
# Password Generator Logic
# ──────────────────────────────────────────────────────────────

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """
    Generate a random password based on selected character types.

    Args:
        length (int): Desired password length (4-32)
        use_upper (bool): Include uppercase letters (A-Z)
        use_lower (bool): Include lowercase letters (a-z)
        use_digits (bool): Include numbers (0-9)
        use_symbols (bool): Include special symbols (!@#$...)

    Returns:
        str: The generated random password

    Raises:
        ValueError: If no character type is selected
    """
    # Build the character pool based on user selections
    char_pool = ""

    if use_upper:
        char_pool += string.ascii_uppercase   # A B C ... Z
    if use_lower:
        char_pool += string.ascii_lowercase   # a b c ... z
    if use_digits:
        char_pool += string.digits            # 0 1 2 ... 9
    if use_symbols:
        char_pool += string.punctuation       # ! @ # $ % ...

    # If nothing is selected, raise an error
    if not char_pool:
        raise ValueError("Please select at least one character type!")

    # Ensure at least one character from each selected type is included
    # This guarantees the password meets all selected criteria
    password_chars = []

    if use_upper:
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password_chars.append(random.choice(string.digits))
    if use_symbols:
        password_chars.append(random.choice(string.punctuation))

    # Fill remaining length with random characters from the full pool
    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(random.choice(char_pool))

    # Shuffle to randomize the positions of guaranteed characters
    random.shuffle(password_chars)

    # Join list into a string and return
    return "".join(password_chars)


def evaluate_strength(password, num_types):
    """
    Evaluate password strength based on length and character variety.

    Strength Criteria:
        - Weak:   length < 8 OR only 1 character type
        - Medium: length 8-15 AND 2-3 character types
        - Strong: length >= 16 OR (length >= 12 AND 4 character types)

    Args:
        password (str): The generated password
        num_types (int): Number of character types selected (1-4)

    Returns:
        tuple: (strength_label, color_code)
    """
    length = len(password)

    # Strong: long password with good variety
    if length >= 16 or (length >= 12 and num_types >= 4):
        return "Strong 💪", COLORS["success"]

    # Medium: decent length with some variety
    elif length >= 8 and num_types >= 2:
        return "Medium ⚡", COLORS["warning"]

    # Weak: short or limited character types
    else:
        return "Weak ⚠️", COLORS["danger"]


# ──────────────────────────────────────────────────────────────
# GUI Application Class
# ──────────────────────────────────────────────────────────────

class PasswordGeneratorApp:
    """
    Main application class for the Password Generator GUI.

    Creates a Tkinter window with:
        - Title and header
        - Password length slider
        - Character type checkboxes
        - Generate button
        - Password display with copy button
        - Strength indicator bar
    """

    def __init__(self):
        """Initialize the main window and build all GUI elements."""

        # ── Create the main window ──
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("500x680")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg_dark"])

        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 250
        y = (self.root.winfo_screenheight() // 2) - 340
        self.root.geometry(f"500x680+{x}+{y}")

        # ── Tkinter Variables (store checkbox/slider values) ──
        self.length_var = tk.IntVar(value=12)       # Default length = 12
        self.upper_var = tk.BooleanVar(value=True)   # Uppercase ON by default
        self.lower_var = tk.BooleanVar(value=True)   # Lowercase ON by default
        self.digit_var = tk.BooleanVar(value=True)   # Numbers ON by default
        self.symbol_var = tk.BooleanVar(value=False)  # Symbols OFF by default

        # ── Build the GUI ──
        self._build_header()
        self._build_length_section()
        self._build_checkbox_section()
        self._build_generate_button()
        self._build_password_display()
        self._build_strength_indicator()

    # ──────────────────────────────────────────────────────
    # GUI Building Methods
    # ──────────────────────────────────────────────────────

    def _build_header(self):
        """Build the title/header section at the top."""

        header_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        header_frame.pack(fill="x", pady=(25, 5))

        # App icon/emoji
        tk.Label(
            header_frame,
            text="🔐",
            font=("Segoe UI Emoji", 36),
            bg=COLORS["bg_dark"],
        ).pack()

        # App title
        tk.Label(
            header_frame,
            text="Password Generator",
            font=("Segoe UI", 22, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_dark"],
        ).pack(pady=(5, 0))

        # Subtitle
        tk.Label(
            header_frame,
            text="Create strong, secure passwords instantly",
            font=("Segoe UI", 10),
            fg=COLORS["text_muted"],
            bg=COLORS["bg_dark"],
        ).pack(pady=(2, 0))

    def _build_length_section(self):
        """Build the password length slider section."""

        # Card-style container
        card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=25, pady=15)
        card.pack(fill="x", padx=25, pady=(15, 5))

        # Label showing current length value
        self.length_label = tk.Label(
            card,
            text="Password Length: 12",
            font=("Segoe UI", 11, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_card"],
        )
        self.length_label.pack(anchor="w")

        # Slider (Scale widget) for selecting length
        self.length_slider = tk.Scale(
            card,
            from_=4,                              # Minimum length
            to=32,                                # Maximum length
            orient="horizontal",                  # Horizontal slider
            variable=self.length_var,             # Linked to length_var
            command=self._on_length_change,       # Callback on change
            bg=COLORS["bg_card"],
            fg=COLORS["text_white"],
            troughcolor=COLORS["bg_input"],       # Track color
            highlightthickness=0,
            activebackground=COLORS["accent"],    # Active thumb color
            sliderrelief="flat",
            showvalue=False,                      # We show value in label
            length=400,
        )
        self.length_slider.pack(fill="x", pady=(5, 0))

        # Min/Max labels below slider
        range_frame = tk.Frame(card, bg=COLORS["bg_card"])
        range_frame.pack(fill="x")

        tk.Label(
            range_frame, text="4", font=("Segoe UI", 8),
            fg=COLORS["text_muted"], bg=COLORS["bg_card"],
        ).pack(side="left")

        tk.Label(
            range_frame, text="32", font=("Segoe UI", 8),
            fg=COLORS["text_muted"], bg=COLORS["bg_card"],
        ).pack(side="right")

    def _build_checkbox_section(self):
        """Build the character type checkboxes section."""

        card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=25, pady=15)
        card.pack(fill="x", padx=25, pady=5)

        # Section label
        tk.Label(
            card,
            text="Character Types",
            font=("Segoe UI", 11, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w", pady=(0, 8))

        # Define checkbox options: (label, variable, example)
        options = [
            ("ABC  Uppercase Letters", self.upper_var, "A-Z"),
            ("abc  Lowercase Letters", self.lower_var, "a-z"),
            ("123  Numbers", self.digit_var, "0-9"),
            ("#$&  Special Symbols", self.symbol_var, "!@#$%"),
        ]

        # Create each checkbox
        for label_text, var, example in options:
            row = tk.Frame(card, bg=COLORS["bg_card"])
            row.pack(fill="x", pady=3)

            cb = tk.Checkbutton(
                row,
                text=f"  {label_text}",
                variable=var,
                font=("Segoe UI", 10),
                fg=COLORS["text_light"],
                bg=COLORS["bg_card"],
                selectcolor=COLORS["bg_input"],     # Check box fill color
                activebackground=COLORS["bg_card"],
                activeforeground=COLORS["text_white"],
                highlightthickness=0,
                cursor="hand2",
            )
            cb.pack(side="left")

            # Example text on the right
            tk.Label(
                row, text=example, font=("Consolas", 9),
                fg=COLORS["text_muted"], bg=COLORS["bg_card"],
            ).pack(side="right")

    def _build_generate_button(self):
        """Build the Generate Password button."""

        self.gen_btn = tk.Button(
            self.root,
            text="⚡  Generate Password",
            font=("Segoe UI", 13, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["accent"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self._on_generate,           # Callback when clicked
        )
        self.gen_btn.pack(fill="x", padx=25, pady=(15, 5))

        # Hover effects for the button
        self.gen_btn.bind("<Enter>", lambda e: self.gen_btn.config(bg=COLORS["accent_hover"]))
        self.gen_btn.bind("<Leave>", lambda e: self.gen_btn.config(bg=COLORS["accent"]))

    def _build_password_display(self):
        """Build the password output display with copy button."""

        card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=20, pady=15)
        card.pack(fill="x", padx=25, pady=5)

        # Label
        tk.Label(
            card, text="Generated Password",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS["text_muted"], bg=COLORS["bg_card"],
        ).pack(anchor="w", pady=(0, 5))

        # Password display row (entry + copy button)
        display_row = tk.Frame(card, bg=COLORS["bg_card"])
        display_row.pack(fill="x")

        # Read-only entry field showing the generated password
        self.password_entry = tk.Entry(
            display_row,
            font=("Consolas", 14),                  # Monospace font
            fg=COLORS["accent"],
            bg=COLORS["bg_input"],
            insertbackground=COLORS["text_white"],
            relief="flat",
            readonlybackground=COLORS["bg_input"],  # Background when readonly
            justify="center",
            state="readonly",                        # User can't type in it
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8)

        # Copy to Clipboard button
        self.copy_btn = tk.Button(
            display_row,
            text=" 📋 Copy ",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["copy_btn"],
            activebackground=COLORS["copy_hover"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            cursor="hand2",
            command=self._on_copy,
        )
        self.copy_btn.pack(side="right", padx=(10, 0), ipady=6)

        # Hover effects for copy button
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg=COLORS["copy_hover"]))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg=COLORS["copy_btn"]))

    def _build_strength_indicator(self):
        """Build the password strength indicator bar."""

        card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=20, pady=12)
        card.pack(fill="x", padx=25, pady=(5, 20))

        # Strength label
        self.strength_label = tk.Label(
            card,
            text="Strength: —",
            font=("Segoe UI", 11, "bold"),
            fg=COLORS["text_muted"],
            bg=COLORS["bg_card"],
        )
        self.strength_label.pack(anchor="w", pady=(0, 5))

        # Strength bar background (grey track)
        bar_bg = tk.Frame(card, bg=COLORS["border"], height=8)
        bar_bg.pack(fill="x")
        bar_bg.pack_propagate(False)

        # Strength bar fill (colored portion)
        self.strength_bar = tk.Frame(bar_bg, bg=COLORS["text_muted"], height=8, width=0)
        self.strength_bar.pack(side="left", fill="y")

    # ──────────────────────────────────────────────────────
    # Event Handlers (Callbacks)
    # ──────────────────────────────────────────────────────

    def _on_length_change(self, value):
        """Called when the length slider value changes."""
        self.length_label.config(text=f"Password Length: {value}")

    def _on_generate(self):
        """
        Called when the Generate button is clicked.
        Validates input, generates password, and updates the display.
        """
        # Get current values from the GUI
        length = self.length_var.get()
        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digit_var.get()
        use_symbols = self.symbol_var.get()

        try:
            # Generate the password
            password = generate_password(
                length, use_upper, use_lower, use_digits, use_symbols
            )

            # Display the password in the entry field
            self.password_entry.config(state="normal")       # Unlock field
            self.password_entry.delete(0, tk.END)             # Clear old text
            self.password_entry.insert(0, password)            # Insert new
            self.password_entry.config(state="readonly")      # Lock again

            # Count how many character types are selected
            num_types = sum([use_upper, use_lower, use_digits, use_symbols])

            # Evaluate and display password strength
            strength_text, strength_color = evaluate_strength(password, num_types)
            self.strength_label.config(
                text=f"Strength: {strength_text}",
                fg=strength_color,
            )

            # Update the strength bar width and color
            # Bar width is proportional to strength
            if "Weak" in strength_text:
                bar_width = 0.33
            elif "Medium" in strength_text:
                bar_width = 0.66
            else:
                bar_width = 1.0

            self.strength_bar.config(bg=strength_color)
            # Use place() for precise width control (relative to parent)
            self.strength_bar.place(relwidth=bar_width, relheight=1.0)

        except ValueError as e:
            # Show error if no character type is selected
            messagebox.showwarning("No Character Type Selected", str(e))

    def _on_copy(self):
        """
        Called when the Copy button is clicked.
        Copies the generated password to the system clipboard.
        """
        # Get the current password from the entry field
        password = self.password_entry.get()

        if not password:
            messagebox.showinfo("Nothing to Copy", "Generate a password first!")
            return

        # Copy to clipboard using Tkinter's built-in method
        self.root.clipboard_clear()              # Clear existing clipboard
        self.root.clipboard_append(password)      # Add password to clipboard

        # Briefly change button text to show feedback
        original_text = self.copy_btn.cget("text")
        self.copy_btn.config(text=" ✅ Copied! ", bg=COLORS["success"])

        # Reset button text after 1.5 seconds
        self.root.after(
            1500,
            lambda: self.copy_btn.config(text=original_text, bg=COLORS["copy_btn"])
        )

    # ──────────────────────────────────────────────────────
    # Run the Application
    # ──────────────────────────────────────────────────────

    def run(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()


# ──────────────────────────────────────────────────────────────
# Entry Point — runs when you execute this file
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.run()
