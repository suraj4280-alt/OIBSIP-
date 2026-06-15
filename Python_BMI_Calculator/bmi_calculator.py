"""
BMI Calculator — Oasis Infobyte Internship Task
=================================================

A desktop application that calculates Body Mass Index (BMI)
with a modern dark-themed GUI built using Python and Tkinter.

Features:
    - Input fields for weight (kg) and height (cm)
    - BMI calculation with category display
    - Color-coded BMI categories
    - Input validation with error messages
    - History panel showing past calculations
    - Reset button to clear all fields

BMI Formula: BMI = weight (kg) / (height in meters)^2

BMI Categories:
    - Below 18.5    → Underweight (Blue)
    - 18.5 - 24.9   → Normal (Green)
    - 25.0 - 29.9   → Overweight (Orange)
    - 30.0 and above → Obese (Red)

Author: Suraj
"""

# ──────────────────────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────────────────────
import tkinter as tk                    # Main GUI library
from tkinter import messagebox          # Pop-up error/info dialogs
from datetime import datetime           # For timestamping history entries


# ──────────────────────────────────────────────────────────────
# Color Theme (Dark Modern Theme — matches Password Generator)
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
    "border":       "#2a3a5c",    # Border color
    "reset_btn":    "#6c7a8d",    # Reset button color
    "reset_hover":  "#8a9bb5",    # Reset button hover

    # BMI Category Colors
    "underweight":  "#3498db",    # Blue
    "normal":       "#2ecc71",    # Green
    "overweight":   "#f39c12",    # Orange
    "obese":        "#e74c3c",    # Red
}


# ──────────────────────────────────────────────────────────────
# BMI Calculation Logic
# ──────────────────────────────────────────────────────────────

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI from weight and height.

    Formula: BMI = weight (kg) / (height in meters)^2

    Args:
        weight_kg (float): Weight in kilograms
        height_cm (float): Height in centimeters

    Returns:
        float: The calculated BMI value

    Raises:
        ValueError: If weight or height is zero or negative
    """
    # Validate inputs
    if weight_kg <= 0:
        raise ValueError("Weight must be a positive number!")
    if height_cm <= 0:
        raise ValueError("Height must be a positive number!")

    # Convert height from cm to meters (100 cm = 1 m)
    height_m = height_cm / 100

    # Apply the BMI formula
    bmi = weight_kg / (height_m ** 2)

    return round(bmi, 1)


def get_bmi_category(bmi):
    """
    Determine the BMI category based on standard WHO ranges.

    Categories:
        - Below 18.5    → Underweight
        - 18.5 - 24.9   → Normal weight
        - 25.0 - 29.9   → Overweight
        - 30.0 and above → Obese

    Args:
        bmi (float): The calculated BMI value

    Returns:
        tuple: (category_name, color_code, emoji)
    """
    if bmi < 18.5:
        return "Underweight", COLORS["underweight"], "🔵"
    elif bmi < 25.0:
        return "Normal", COLORS["normal"], "🟢"
    elif bmi < 30.0:
        return "Overweight", COLORS["overweight"], "🟠"
    else:
        return "Obese", COLORS["obese"], "🔴"


def get_health_tip(category):
    """
    Return a short health tip based on the BMI category.

    Args:
        category (str): The BMI category name

    Returns:
        str: A brief health suggestion
    """
    tips = {
        "Underweight": "Consider a nutrient-rich diet to reach a healthy weight.",
        "Normal": "Great job! Maintain your healthy lifestyle.",
        "Overweight": "Regular exercise and a balanced diet can help.",
        "Obese": "Please consult a healthcare provider for guidance.",
    }
    return tips.get(category, "")


# ──────────────────────────────────────────────────────────────
# GUI Application Class
# ──────────────────────────────────────────────────────────────

class BMICalculatorApp:
    """
    Main application class for the BMI Calculator GUI.

    Creates a Tkinter window with:
        - Title and header
        - Weight and height input fields
        - Calculate and Reset buttons
        - BMI result display with category
        - BMI scale indicator bar
        - History panel with past calculations
    """

    def __init__(self):
        """Initialize the main window and build all GUI elements."""

        # ── Create the main window ──
        self.root = tk.Tk()
        self.root.title("BMI Calculator")
        self.root.geometry("500x780")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg_dark"])

        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 250
        y = (self.root.winfo_screenheight() // 2) - 390
        self.root.geometry(f"500x780+{x}+{y}")

        # ── History list to store past calculations ──
        self.history = []

        # ── Build all GUI sections ──
        self._build_header()
        self._build_input_section()
        self._build_buttons()
        self._build_result_section()
        self._build_bmi_scale()
        self._build_history_section()

    # ──────────────────────────────────────────────────────
    # GUI Building Methods
    # ──────────────────────────────────────────────────────

    def _build_header(self):
        """Build the title/header section at the top."""

        header_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        header_frame.pack(fill="x", pady=(20, 5))

        # App icon/emoji
        tk.Label(
            header_frame,
            text="⚖️",
            font=("Segoe UI Emoji", 36),
            bg=COLORS["bg_dark"],
        ).pack()

        # App title
        tk.Label(
            header_frame,
            text="BMI Calculator",
            font=("Segoe UI", 22, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_dark"],
        ).pack(pady=(5, 0))

        # Subtitle
        tk.Label(
            header_frame,
            text="Check your Body Mass Index instantly",
            font=("Segoe UI", 10),
            fg=COLORS["text_muted"],
            bg=COLORS["bg_dark"],
        ).pack(pady=(2, 0))

    def _build_input_section(self):
        """Build the weight and height input fields."""

        card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=25, pady=20)
        card.pack(fill="x", padx=25, pady=(15, 5))

        # ── Weight Input ──
        tk.Label(
            card,
            text="Weight (kg)",
            font=("Segoe UI", 11, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w")

        # Weight entry field
        self.weight_entry = tk.Entry(
            card,
            font=("Segoe UI", 14),
            fg=COLORS["text_white"],
            bg=COLORS["bg_input"],
            insertbackground=COLORS["text_white"],  # Cursor color
            relief="flat",
            justify="center",
        )
        self.weight_entry.pack(fill="x", ipady=8, pady=(5, 15))

        # Placeholder text for weight
        self.weight_entry.insert(0, "e.g. 65")
        self.weight_entry.config(fg=COLORS["text_muted"])
        self.weight_entry.bind("<FocusIn>", lambda e: self._clear_placeholder(self.weight_entry, "e.g. 65"))
        self.weight_entry.bind("<FocusOut>", lambda e: self._add_placeholder(self.weight_entry, "e.g. 65"))

        # ── Height Input ──
        tk.Label(
            card,
            text="Height (cm)",
            font=("Segoe UI", 11, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w")

        # Height entry field
        self.height_entry = tk.Entry(
            card,
            font=("Segoe UI", 14),
            fg=COLORS["text_white"],
            bg=COLORS["bg_input"],
            insertbackground=COLORS["text_white"],
            relief="flat",
            justify="center",
        )
        self.height_entry.pack(fill="x", ipady=8, pady=(5, 0))

        # Placeholder text for height
        self.height_entry.insert(0, "e.g. 170")
        self.height_entry.config(fg=COLORS["text_muted"])
        self.height_entry.bind("<FocusIn>", lambda e: self._clear_placeholder(self.height_entry, "e.g. 170"))
        self.height_entry.bind("<FocusOut>", lambda e: self._add_placeholder(self.height_entry, "e.g. 170"))

    def _build_buttons(self):
        """Build the Calculate and Reset buttons."""

        btn_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        btn_frame.pack(fill="x", padx=25, pady=(10, 5))

        # ── Calculate Button ──
        self.calc_btn = tk.Button(
            btn_frame,
            text="⚡  Calculate BMI",
            font=("Segoe UI", 13, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["accent"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self._on_calculate,
        )
        self.calc_btn.pack(fill="x", side="left", expand=True, padx=(0, 5))

        # Hover effect
        self.calc_btn.bind("<Enter>", lambda e: self.calc_btn.config(bg=COLORS["accent_hover"]))
        self.calc_btn.bind("<Leave>", lambda e: self.calc_btn.config(bg=COLORS["accent"]))

        # ── Reset Button ──
        self.reset_btn = tk.Button(
            btn_frame,
            text="🔄 Reset",
            font=("Segoe UI", 11, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["reset_btn"],
            activebackground=COLORS["reset_hover"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self._on_reset,
        )
        self.reset_btn.pack(fill="x", side="right", expand=True, padx=(5, 0))

        # Hover effect
        self.reset_btn.bind("<Enter>", lambda e: self.reset_btn.config(bg=COLORS["reset_hover"]))
        self.reset_btn.bind("<Leave>", lambda e: self.reset_btn.config(bg=COLORS["reset_btn"]))

    def _build_result_section(self):
        """Build the BMI result display area."""

        self.result_card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=25, pady=15)
        self.result_card.pack(fill="x", padx=25, pady=5)

        # BMI Value (large number)
        self.bmi_value_label = tk.Label(
            self.result_card,
            text="—",
            font=("Segoe UI", 40, "bold"),
            fg=COLORS["text_muted"],
            bg=COLORS["bg_card"],
        )
        self.bmi_value_label.pack()

        # BMI Category label
        self.bmi_category_label = tk.Label(
            self.result_card,
            text="Enter your details above",
            font=("Segoe UI", 13, "bold"),
            fg=COLORS["text_muted"],
            bg=COLORS["bg_card"],
        )
        self.bmi_category_label.pack(pady=(0, 3))

        # Health tip label
        self.health_tip_label = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI", 9),
            fg=COLORS["text_muted"],
            bg=COLORS["bg_card"],
            wraplength=400,
        )
        self.health_tip_label.pack()

    def _build_bmi_scale(self):
        """Build the colored BMI scale bar showing all categories."""

        scale_card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=25, pady=10)
        scale_card.pack(fill="x", padx=25, pady=(0, 5))

        # Color bar with 4 segments
        bar_frame = tk.Frame(scale_card, bg=COLORS["bg_card"], height=12)
        bar_frame.pack(fill="x", pady=(0, 5))

        # Each segment represents a BMI category
        segments = [
            (COLORS["underweight"], 0.20),   # Underweight ~20% of bar
            (COLORS["normal"], 0.35),         # Normal ~35% of bar
            (COLORS["overweight"], 0.25),     # Overweight ~25% of bar
            (COLORS["obese"], 0.20),          # Obese ~20% of bar
        ]

        for color, weight in segments:
            seg = tk.Frame(bar_frame, bg=color, height=12)
            seg.pack(side="left", fill="y", expand=False)
            # Set width proportionally
            seg.config(width=int(400 * weight))

        # The pointer/indicator that shows where your BMI falls
        self.scale_pointer = tk.Label(
            scale_card,
            text="▲",
            font=("Segoe UI", 12),
            fg=COLORS["text_muted"],
            bg=COLORS["bg_card"],
        )
        # Don't pack yet — it gets placed dynamically after calculation

        # Category labels below the bar
        labels_frame = tk.Frame(scale_card, bg=COLORS["bg_card"])
        labels_frame.pack(fill="x")

        categories = [
            ("< 18.5", COLORS["underweight"]),
            ("18.5–24.9", COLORS["normal"]),
            ("25–29.9", COLORS["overweight"]),
            ("30+", COLORS["obese"]),
        ]

        for text, color in categories:
            tk.Label(
                labels_frame, text=text,
                font=("Segoe UI", 8),
                fg=color, bg=COLORS["bg_card"],
            ).pack(side="left", expand=True)

    def _build_history_section(self):
        """Build the history panel showing past calculations."""

        card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=20, pady=10)
        card.pack(fill="x", padx=25, pady=(5, 20))

        # Header row with title and clear button
        header_row = tk.Frame(card, bg=COLORS["bg_card"])
        header_row.pack(fill="x", pady=(0, 5))

        tk.Label(
            header_row,
            text="📋 History",
            font=("Segoe UI", 11, "bold"),
            fg=COLORS["text_white"],
            bg=COLORS["bg_card"],
        ).pack(side="left")

        # Clear history button
        clear_btn = tk.Button(
            header_row,
            text="Clear",
            font=("Segoe UI", 8),
            fg=COLORS["text_muted"],
            bg=COLORS["bg_card"],
            activebackground=COLORS["bg_card"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            cursor="hand2",
            command=self._clear_history,
        )
        clear_btn.pack(side="right")

        # Scrollable history list using a Listbox
        self.history_listbox = tk.Listbox(
            card,
            font=("Consolas", 9),
            fg=COLORS["text_light"],
            bg=COLORS["bg_input"],
            selectbackground=COLORS["border"],
            relief="flat",
            height=4,                          # Show 4 entries at a time
            highlightthickness=0,
            activestyle="none",
        )
        self.history_listbox.pack(fill="x")

        # Show a placeholder message when empty
        self.history_listbox.insert(0, "  No calculations yet...")

    # ──────────────────────────────────────────────────────
    # Placeholder Helpers (for input fields)
    # ──────────────────────────────────────────────────────

    def _clear_placeholder(self, entry, placeholder):
        """Remove placeholder text when the user clicks on the field."""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=COLORS["text_white"])

    def _add_placeholder(self, entry, placeholder):
        """Re-add placeholder text if the field is left empty."""
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg=COLORS["text_muted"])

    # ──────────────────────────────────────────────────────
    # Event Handlers (Callbacks)
    # ──────────────────────────────────────────────────────

    def _on_calculate(self):
        """
        Called when the Calculate button is clicked.
        Validates input, calculates BMI, and updates the display.
        """
        # Get raw input from entry fields
        weight_text = self.weight_entry.get().strip()
        height_text = self.height_entry.get().strip()

        # Ignore placeholder text
        if weight_text == "e.g. 65":
            weight_text = ""
        if height_text == "e.g. 170":
            height_text = ""

        # ── Input Validation ──

        # Check if fields are empty
        if not weight_text or not height_text:
            messagebox.showwarning(
                "Missing Input",
                "Please enter both weight and height!"
            )
            return

        # Check if inputs are valid numbers
        try:
            weight = float(weight_text)
            height = float(height_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers for weight and height!"
            )
            return

        # Check for zero or negative values
        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be positive numbers!"
            )
            return

        # Check for unrealistic values
        if weight > 500:
            messagebox.showerror("Invalid Input", "Weight seems too high! Enter weight in kg.")
            return
        if height > 300:
            messagebox.showerror("Invalid Input", "Height seems too high! Enter height in cm.")
            return

        # ── Calculate BMI ──
        try:
            bmi = calculate_bmi(weight, height)
            category, color, emoji = get_bmi_category(bmi)
            tip = get_health_tip(category)

            # ── Update Result Display ──
            self.bmi_value_label.config(text=str(bmi), fg=color)
            self.bmi_category_label.config(
                text=f"{emoji}  {category}",
                fg=color,
            )
            self.health_tip_label.config(text=tip, fg=COLORS["text_light"])

            # ── Update Scale Pointer ──
            self._update_scale_pointer(bmi)

            # ── Add to History ──
            timestamp = datetime.now().strftime("%I:%M %p")
            entry = f"  {timestamp}  |  {weight}kg, {height}cm  →  BMI {bmi} ({category})"
            self.history.append(entry)

            # Update history listbox
            if self.history_listbox.get(0) == "  No calculations yet...":
                self.history_listbox.delete(0)

            self.history_listbox.insert(tk.END, entry)
            self.history_listbox.see(tk.END)  # Auto-scroll to latest

        except ValueError as e:
            messagebox.showerror("Calculation Error", str(e))

    def _on_reset(self):
        """
        Called when the Reset button is clicked.
        Clears all input fields and resets the result display.
        """
        # Clear weight field and add placeholder
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, "e.g. 65")
        self.weight_entry.config(fg=COLORS["text_muted"])

        # Clear height field and add placeholder
        self.height_entry.delete(0, tk.END)
        self.height_entry.insert(0, "e.g. 170")
        self.height_entry.config(fg=COLORS["text_muted"])

        # Reset result display
        self.bmi_value_label.config(text="—", fg=COLORS["text_muted"])
        self.bmi_category_label.config(
            text="Enter your details above",
            fg=COLORS["text_muted"],
        )
        self.health_tip_label.config(text="")

        # Hide scale pointer
        self.scale_pointer.place_forget()

    def _update_scale_pointer(self, bmi):
        """
        Position the pointer arrow on the BMI scale bar.

        Maps the BMI value to a position on the colored bar.
        BMI range 10-40 is mapped to the full width of the bar.

        Args:
            bmi (float): The calculated BMI value
        """
        # Clamp BMI to display range (10 to 40)
        clamped_bmi = max(10, min(40, bmi))

        # Calculate relative position (0.0 to 1.0)
        # BMI 10 = left edge, BMI 40 = right edge
        position = (clamped_bmi - 10) / (40 - 10)

        # Get the category color for the pointer
        _, color, _ = get_bmi_category(bmi)
        self.scale_pointer.config(fg=color)

        # Place the pointer using relative x position
        self.scale_pointer.place(relx=position, anchor="n")

    def _clear_history(self):
        """Clear all entries from the history list."""
        self.history.clear()
        self.history_listbox.delete(0, tk.END)
        self.history_listbox.insert(0, "  No calculations yet...")

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
    app = BMICalculatorApp()
    app.run()
