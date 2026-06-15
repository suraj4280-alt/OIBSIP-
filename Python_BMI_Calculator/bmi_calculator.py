# ============================================
# BMI Calculator - Oasis Infobyte Internship
# Author: Suraj
# ============================================
# This program calculates Body Mass Index (BMI)
# using weight and height entered by the user.
# It uses Tkinter for the GUI.
# ============================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# --- Colors for the app (dark theme) ---
BG_COLOR = "#1a1a2e"         # dark background
CARD_COLOR = "#16213e"       # card background
INPUT_COLOR = "#0f3460"      # input field bg
ACCENT_COLOR = "#e94560"     # main button color
WHITE = "#ffffff"
LIGHT_TEXT = "#b8c5d6"
MUTED_TEXT = "#6c7a8d"

# BMI category colors
BLUE = "#3498db"     # underweight
GREEN = "#2ecc71"    # normal
ORANGE = "#f39c12"   # overweight
RED = "#e74c3c"      # obese


# --- Function to calculate BMI ---
def calculate_bmi(weight, height_cm):
    """
    Calculate BMI using the formula:
    BMI = weight(kg) / height(m)^2
    """
    height_m = height_cm / 100          # convert cm to meters
    bmi = weight / (height_m ** 2)      # apply formula
    return round(bmi, 1)                # round to 1 decimal


# --- Function to get BMI category ---
def get_category(bmi):
    """
    Returns the category, color, and emoji based on BMI value.
    - Below 18.5 = Underweight
    - 18.5 to 24.9 = Normal
    - 25 to 29.9 = Overweight
    - 30 and above = Obese
    """
    if bmi < 18.5:
        return "Underweight", BLUE, "🔵"
    elif bmi < 25:
        return "Normal", GREEN, "🟢"
    elif bmi < 30:
        return "Overweight", ORANGE, "🟠"
    else:
        return "Obese", RED, "🔴"


# --- Health tips based on category ---
def get_tip(category):
    if category == "Underweight":
        return "Try eating a nutrient-rich diet to gain healthy weight."
    elif category == "Normal":
        return "Great! Keep up your healthy lifestyle."
    elif category == "Overweight":
        return "Try regular exercise and a balanced diet."
    else:
        return "Please consult a doctor for proper guidance."


# =============================================
# Main Application Class
# =============================================

class BMICalculator:
    def __init__(self):
        # --- Create main window ---
        self.root = tk.Tk()
        self.root.title("BMI Calculator")
        self.root.geometry("500x780")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        # center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 250
        y = (self.root.winfo_screenheight() // 2) - 390
        self.root.geometry(f"500x780+{x}+{y}")

        # list to store history
        self.history = []

        # --- Build all sections ---
        self.create_header()
        self.create_inputs()
        self.create_buttons()
        self.create_result_area()
        self.create_bmi_scale()
        self.create_history_panel()

    # --- Header Section ---
    def create_header(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(fill="x", pady=(20, 5))

        # emoji icon
        tk.Label(frame, text="⚖️", font=("Segoe UI Emoji", 36),
                 bg=BG_COLOR).pack()

        # title
        tk.Label(frame, text="BMI Calculator",
                 font=("Segoe UI", 22, "bold"),
                 fg=WHITE, bg=BG_COLOR).pack(pady=(5, 0))

        # subtitle
        tk.Label(frame, text="Check your Body Mass Index instantly",
                 font=("Segoe UI", 10),
                 fg=MUTED_TEXT, bg=BG_COLOR).pack(pady=(2, 0))

    # --- Input Fields ---
    def create_inputs(self):
        card = tk.Frame(self.root, bg=CARD_COLOR, padx=25, pady=20)
        card.pack(fill="x", padx=25, pady=(15, 5))

        # Weight label
        tk.Label(card, text="Weight (kg)",
                 font=("Segoe UI", 11, "bold"),
                 fg=WHITE, bg=CARD_COLOR).pack(anchor="w")

        # Weight input box
        self.weight_input = tk.Entry(card, font=("Segoe UI", 14),
                                     fg=WHITE, bg=INPUT_COLOR,
                                     insertbackground=WHITE,
                                     relief="flat", justify="center")
        self.weight_input.pack(fill="x", ipady=8, pady=(5, 15))

        # placeholder for weight
        self.weight_input.insert(0, "e.g. 65")
        self.weight_input.config(fg=MUTED_TEXT)
        self.weight_input.bind("<FocusIn>", lambda e: self.clear_placeholder(self.weight_input, "e.g. 65"))
        self.weight_input.bind("<FocusOut>", lambda e: self.set_placeholder(self.weight_input, "e.g. 65"))

        # Height label
        tk.Label(card, text="Height (cm)",
                 font=("Segoe UI", 11, "bold"),
                 fg=WHITE, bg=CARD_COLOR).pack(anchor="w")

        # Height input box
        self.height_input = tk.Entry(card, font=("Segoe UI", 14),
                                     fg=WHITE, bg=INPUT_COLOR,
                                     insertbackground=WHITE,
                                     relief="flat", justify="center")
        self.height_input.pack(fill="x", ipady=8, pady=(5, 0))

        # placeholder for height
        self.height_input.insert(0, "e.g. 170")
        self.height_input.config(fg=MUTED_TEXT)
        self.height_input.bind("<FocusIn>", lambda e: self.clear_placeholder(self.height_input, "e.g. 170"))
        self.height_input.bind("<FocusOut>", lambda e: self.set_placeholder(self.height_input, "e.g. 170"))

    # --- Buttons ---
    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(fill="x", padx=25, pady=(10, 5))

        # Calculate button
        self.calc_btn = tk.Button(btn_frame, text="⚡  Calculate BMI",
                                  font=("Segoe UI", 13, "bold"),
                                  fg=WHITE, bg=ACCENT_COLOR,
                                  activebackground="#ff6b6b",
                                  activeforeground=WHITE,
                                  relief="flat", cursor="hand2",
                                  pady=10, command=self.calculate)
        self.calc_btn.pack(fill="x", side="left", expand=True, padx=(0, 5))
        self.calc_btn.bind("<Enter>", lambda e: self.calc_btn.config(bg="#ff6b6b"))
        self.calc_btn.bind("<Leave>", lambda e: self.calc_btn.config(bg=ACCENT_COLOR))

        # Reset button
        self.reset_btn = tk.Button(btn_frame, text="🔄 Reset",
                                   font=("Segoe UI", 11, "bold"),
                                   fg=WHITE, bg=MUTED_TEXT,
                                   activebackground="#8a9bb5",
                                   activeforeground=WHITE,
                                   relief="flat", cursor="hand2",
                                   pady=10, command=self.reset)
        self.reset_btn.pack(fill="x", side="right", expand=True, padx=(5, 0))
        self.reset_btn.bind("<Enter>", lambda e: self.reset_btn.config(bg="#8a9bb5"))
        self.reset_btn.bind("<Leave>", lambda e: self.reset_btn.config(bg=MUTED_TEXT))

    # --- Result Display ---
    def create_result_area(self):
        card = tk.Frame(self.root, bg=CARD_COLOR, padx=25, pady=15)
        card.pack(fill="x", padx=25, pady=5)

        # big BMI number
        self.bmi_label = tk.Label(card, text="—",
                                  font=("Segoe UI", 40, "bold"),
                                  fg=MUTED_TEXT, bg=CARD_COLOR)
        self.bmi_label.pack()

        # category text
        self.category_label = tk.Label(card, text="Enter your details above",
                                       font=("Segoe UI", 13, "bold"),
                                       fg=MUTED_TEXT, bg=CARD_COLOR)
        self.category_label.pack(pady=(0, 3))

        # health tip
        self.tip_label = tk.Label(card, text="",
                                  font=("Segoe UI", 9),
                                  fg=MUTED_TEXT, bg=CARD_COLOR,
                                  wraplength=400)
        self.tip_label.pack()

    # --- BMI Scale Bar ---
    def create_bmi_scale(self):
        card = tk.Frame(self.root, bg=CARD_COLOR, padx=25, pady=10)
        card.pack(fill="x", padx=25, pady=(0, 5))

        # color bar with 4 segments
        bar = tk.Frame(card, bg=CARD_COLOR, height=12)
        bar.pack(fill="x", pady=(0, 5))

        # each color = one category
        colors = [(BLUE, 80), (GREEN, 140), (ORANGE, 100), (RED, 80)]
        for color, width in colors:
            tk.Frame(bar, bg=color, height=12, width=width).pack(side="left", fill="y")

        # pointer arrow (shows your BMI position)
        self.pointer = tk.Label(card, text="▲", font=("Segoe UI", 12),
                                fg=MUTED_TEXT, bg=CARD_COLOR)

        # labels under the bar
        labels = tk.Frame(card, bg=CARD_COLOR)
        labels.pack(fill="x")
        for text, color in [("< 18.5", BLUE), ("18.5–24.9", GREEN),
                            ("25–29.9", ORANGE), ("30+", RED)]:
            tk.Label(labels, text=text, font=("Segoe UI", 8),
                     fg=color, bg=CARD_COLOR).pack(side="left", expand=True)

    # --- History Panel ---
    def create_history_panel(self):
        card = tk.Frame(self.root, bg=CARD_COLOR, padx=20, pady=10)
        card.pack(fill="x", padx=25, pady=(5, 20))

        # header with clear button
        header = tk.Frame(card, bg=CARD_COLOR)
        header.pack(fill="x", pady=(0, 5))

        tk.Label(header, text="📋 History",
                 font=("Segoe UI", 11, "bold"),
                 fg=WHITE, bg=CARD_COLOR).pack(side="left")

        tk.Button(header, text="Clear", font=("Segoe UI", 8),
                  fg=MUTED_TEXT, bg=CARD_COLOR,
                  relief="flat", cursor="hand2",
                  command=self.clear_history).pack(side="right")

        # history list
        self.history_list = tk.Listbox(card, font=("Consolas", 9),
                                       fg=LIGHT_TEXT, bg=INPUT_COLOR,
                                       selectbackground="#2a3a5c",
                                       relief="flat", height=4,
                                       highlightthickness=0)
        self.history_list.pack(fill="x")
        self.history_list.insert(0, "  No calculations yet...")

    # --- Helper: clear placeholder ---
    def clear_placeholder(self, entry, text):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg=WHITE)

    # --- Helper: set placeholder ---
    def set_placeholder(self, entry, text):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg=MUTED_TEXT)

    # =============================================
    # CALCULATE BUTTON - main logic
    # =============================================
    def calculate(self):
        # get values from input fields
        weight_text = self.weight_input.get().strip()
        height_text = self.height_input.get().strip()

        # ignore placeholder text
        if weight_text == "e.g. 65":
            weight_text = ""
        if height_text == "e.g. 170":
            height_text = ""

        # check if fields are empty
        if not weight_text or not height_text:
            messagebox.showwarning("Missing Input", "Please enter both weight and height!")
            return

        # check if inputs are valid numbers
        try:
            weight = float(weight_text)
            height = float(height_text)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers!")
            return

        # check for negative or zero values
        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid Input", "Values must be positive numbers!")
            return

        # check for unrealistic values
        if weight > 500:
            messagebox.showerror("Invalid Input", "Weight too high! Enter in kg.")
            return
        if height > 300:
            messagebox.showerror("Invalid Input", "Height too high! Enter in cm.")
            return

        # --- do the calculation ---
        bmi = calculate_bmi(weight, height)
        category, color, emoji = get_category(bmi)
        tip = get_tip(category)

        # update the result display
        self.bmi_label.config(text=str(bmi), fg=color)
        self.category_label.config(text=f"{emoji}  {category}", fg=color)
        self.tip_label.config(text=tip, fg=LIGHT_TEXT)

        # move the pointer on the scale bar
        clamped = max(10, min(40, bmi))
        position = (clamped - 10) / 30   # 0.0 to 1.0
        self.pointer.config(fg=color)
        self.pointer.place(relx=position, anchor="n")

        # add to history
        time_now = datetime.now().strftime("%I:%M %p")
        entry = f"  {time_now}  |  {weight}kg, {height}cm  →  BMI {bmi} ({category})"
        self.history.append(entry)

        if self.history_list.get(0) == "  No calculations yet...":
            self.history_list.delete(0)

        self.history_list.insert(tk.END, entry)
        self.history_list.see(tk.END)

    # =============================================
    # RESET BUTTON - clear everything
    # =============================================
    def reset(self):
        # clear weight field
        self.weight_input.delete(0, tk.END)
        self.weight_input.insert(0, "e.g. 65")
        self.weight_input.config(fg=MUTED_TEXT)

        # clear height field
        self.height_input.delete(0, tk.END)
        self.height_input.insert(0, "e.g. 170")
        self.height_input.config(fg=MUTED_TEXT)

        # reset result
        self.bmi_label.config(text="—", fg=MUTED_TEXT)
        self.category_label.config(text="Enter your details above", fg=MUTED_TEXT)
        self.tip_label.config(text="")
        self.pointer.place_forget()

    # --- Clear history ---
    def clear_history(self):
        self.history.clear()
        self.history_list.delete(0, tk.END)
        self.history_list.insert(0, "  No calculations yet...")

    # --- Run the app ---
    def run(self):
        self.root.mainloop()


# =============================================
# Run the program
# =============================================
if __name__ == "__main__":
    app = BMICalculator()
    app.run()
