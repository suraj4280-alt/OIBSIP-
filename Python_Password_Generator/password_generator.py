# ============================================
# Random Password Generator - Oasis Infobyte Internship
# Author: Suraj
# ============================================
# This program generates random passwords
# based on the user's selected options.
# It uses Tkinter for the GUI.
# ============================================

import random
import string
import tkinter as tk
from tkinter import messagebox

# --- Colors for the app (dark theme) ---
BG_COLOR = "#1a1a2e"         # dark background
CARD_COLOR = "#16213e"       # card background
INPUT_COLOR = "#0f3460"      # input field bg
ACCENT_COLOR = "#e94560"     # main button color
WHITE = "#ffffff"
LIGHT_TEXT = "#b8c5d6"
MUTED_TEXT = "#6c7a8d"
COPY_BTN = "#0ea5e9"         # copy button color

# strength colors
GREEN = "#2ecc71"    # strong
ORANGE = "#f39c12"   # medium
RED_COLOR = "#e74c3c"       # weak


# --- Function to generate password ---
def generate_password(length, uppercase, lowercase, digits, symbols):
    """
    Creates a random password based on selected options.
    Makes sure at least one character from each selected type is included.
    """
    # build the character pool
    pool = ""
    if uppercase:
        pool += string.ascii_uppercase   # A-Z
    if lowercase:
        pool += string.ascii_lowercase   # a-z
    if digits:
        pool += string.digits            # 0-9
    if symbols:
        pool += string.punctuation       # !@#$%...

    # check if pool is empty
    if not pool:
        raise ValueError("Select at least one character type!")

    # make sure at least one of each selected type is in the password
    password = []
    if uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if digits:
        password.append(random.choice(string.digits))
    if symbols:
        password.append(random.choice(string.punctuation))

    # fill the rest with random characters from pool
    for i in range(length - len(password)):
        password.append(random.choice(pool))

    # shuffle so the guaranteed characters aren't always at the start
    random.shuffle(password)

    return "".join(password)


# --- Function to check password strength ---
def check_strength(password, num_types):
    """
    Checks how strong the password is based on length and variety.
    Returns: (label, color)
    """
    length = len(password)

    if length >= 16 or (length >= 12 and num_types >= 4):
        return "Strong 💪", GREEN
    elif length >= 8 and num_types >= 2:
        return "Medium ⚡", ORANGE
    else:
        return "Weak ⚠️", RED_COLOR


# =============================================
# Main Application Class
# =============================================

class PasswordGenerator:
    def __init__(self):
        # --- Create main window ---
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("500x680")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        # center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 250
        y = (self.root.winfo_screenheight() // 2) - 340
        self.root.geometry(f"500x680+{x}+{y}")

        # --- Variables to store checkbox values ---
        self.length_var = tk.IntVar(value=12)       # default length = 12
        self.upper_var = tk.BooleanVar(value=True)   # uppercase ON
        self.lower_var = tk.BooleanVar(value=True)   # lowercase ON
        self.digit_var = tk.BooleanVar(value=True)   # numbers ON
        self.symbol_var = tk.BooleanVar(value=False)  # symbols OFF

        # --- Build all sections ---
        self.create_header()
        self.create_length_slider()
        self.create_checkboxes()
        self.create_generate_button()
        self.create_password_display()
        self.create_strength_bar()

    # --- Header Section ---
    def create_header(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(fill="x", pady=(25, 5))

        tk.Label(frame, text="🔐", font=("Segoe UI Emoji", 36),
                 bg=BG_COLOR).pack()

        tk.Label(frame, text="Password Generator",
                 font=("Segoe UI", 22, "bold"),
                 fg=WHITE, bg=BG_COLOR).pack(pady=(5, 0))

        tk.Label(frame, text="Create strong, secure passwords instantly",
                 font=("Segoe UI", 10),
                 fg=MUTED_TEXT, bg=BG_COLOR).pack(pady=(2, 0))

    # --- Length Slider ---
    def create_length_slider(self):
        card = tk.Frame(self.root, bg=CARD_COLOR, padx=25, pady=15)
        card.pack(fill="x", padx=25, pady=(15, 5))

        # label showing current length
        self.length_label = tk.Label(card, text="Password Length: 12",
                                     font=("Segoe UI", 11, "bold"),
                                     fg=WHITE, bg=CARD_COLOR)
        self.length_label.pack(anchor="w")

        # slider widget
        self.slider = tk.Scale(card, from_=4, to=32,
                               orient="horizontal",
                               variable=self.length_var,
                               command=self.update_length_label,
                               bg=CARD_COLOR, fg=WHITE,
                               troughcolor=INPUT_COLOR,
                               highlightthickness=0,
                               activebackground=ACCENT_COLOR,
                               sliderrelief="flat",
                               showvalue=False, length=400)
        self.slider.pack(fill="x", pady=(5, 0))

        # min/max labels
        range_frame = tk.Frame(card, bg=CARD_COLOR)
        range_frame.pack(fill="x")
        tk.Label(range_frame, text="4", font=("Segoe UI", 8),
                 fg=MUTED_TEXT, bg=CARD_COLOR).pack(side="left")
        tk.Label(range_frame, text="32", font=("Segoe UI", 8),
                 fg=MUTED_TEXT, bg=CARD_COLOR).pack(side="right")

    # --- Checkboxes ---
    def create_checkboxes(self):
        card = tk.Frame(self.root, bg=CARD_COLOR, padx=25, pady=15)
        card.pack(fill="x", padx=25, pady=5)

        tk.Label(card, text="Character Types",
                 font=("Segoe UI", 11, "bold"),
                 fg=WHITE, bg=CARD_COLOR).pack(anchor="w", pady=(0, 8))

        # list of options: (label, variable, example)
        options = [
            ("ABC  Uppercase Letters", self.upper_var, "A-Z"),
            ("abc  Lowercase Letters", self.lower_var, "a-z"),
            ("123  Numbers", self.digit_var, "0-9"),
            ("#$&  Special Symbols", self.symbol_var, "!@#$%"),
        ]

        for label, var, example in options:
            row = tk.Frame(card, bg=CARD_COLOR)
            row.pack(fill="x", pady=3)

            tk.Checkbutton(row, text=f"  {label}", variable=var,
                           font=("Segoe UI", 10), fg=LIGHT_TEXT,
                           bg=CARD_COLOR, selectcolor=INPUT_COLOR,
                           activebackground=CARD_COLOR,
                           activeforeground=WHITE,
                           highlightthickness=0,
                           cursor="hand2").pack(side="left")

            tk.Label(row, text=example, font=("Consolas", 9),
                     fg=MUTED_TEXT, bg=CARD_COLOR).pack(side="right")

    # --- Generate Button ---
    def create_generate_button(self):
        self.gen_btn = tk.Button(self.root,
                                 text="⚡  Generate Password",
                                 font=("Segoe UI", 13, "bold"),
                                 fg=WHITE, bg=ACCENT_COLOR,
                                 activebackground="#ff6b6b",
                                 activeforeground=WHITE,
                                 relief="flat", cursor="hand2",
                                 pady=10, command=self.generate)
        self.gen_btn.pack(fill="x", padx=25, pady=(15, 5))
        self.gen_btn.bind("<Enter>", lambda e: self.gen_btn.config(bg="#ff6b6b"))
        self.gen_btn.bind("<Leave>", lambda e: self.gen_btn.config(bg=ACCENT_COLOR))

    # --- Password Display ---
    def create_password_display(self):
        card = tk.Frame(self.root, bg=CARD_COLOR, padx=20, pady=15)
        card.pack(fill="x", padx=25, pady=5)

        tk.Label(card, text="Generated Password",
                 font=("Segoe UI", 10, "bold"),
                 fg=MUTED_TEXT, bg=CARD_COLOR).pack(anchor="w", pady=(0, 5))

        row = tk.Frame(card, bg=CARD_COLOR)
        row.pack(fill="x")

        # password text field (read only)
        self.password_field = tk.Entry(row, font=("Consolas", 14),
                                       fg=ACCENT_COLOR, bg=INPUT_COLOR,
                                       insertbackground=WHITE,
                                       relief="flat",
                                       readonlybackground=INPUT_COLOR,
                                       justify="center", state="readonly")
        self.password_field.pack(side="left", fill="x", expand=True, ipady=8)

        # copy button
        self.copy_btn = tk.Button(row, text=" 📋 Copy ",
                                  font=("Segoe UI", 10, "bold"),
                                  fg=WHITE, bg=COPY_BTN,
                                  activebackground="#38bdf8",
                                  activeforeground=WHITE,
                                  relief="flat", cursor="hand2",
                                  command=self.copy_password)
        self.copy_btn.pack(side="right", padx=(10, 0), ipady=6)
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg="#38bdf8"))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg=COPY_BTN))

    # --- Strength Bar ---
    def create_strength_bar(self):
        card = tk.Frame(self.root, bg=CARD_COLOR, padx=20, pady=12)
        card.pack(fill="x", padx=25, pady=(5, 20))

        self.strength_label = tk.Label(card, text="Strength: —",
                                       font=("Segoe UI", 11, "bold"),
                                       fg=MUTED_TEXT, bg=CARD_COLOR)
        self.strength_label.pack(anchor="w", pady=(0, 5))

        # grey background bar
        bar_bg = tk.Frame(card, bg="#2a3a5c", height=8)
        bar_bg.pack(fill="x")
        bar_bg.pack_propagate(False)

        # colored fill bar
        self.strength_fill = tk.Frame(bar_bg, bg=MUTED_TEXT, height=8, width=0)
        self.strength_fill.pack(side="left", fill="y")

    # --- Update length label when slider moves ---
    def update_length_label(self, value):
        self.length_label.config(text=f"Password Length: {value}")

    # =============================================
    # GENERATE BUTTON - main logic
    # =============================================
    def generate(self):
        length = self.length_var.get()
        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digit_var.get()
        use_symbols = self.symbol_var.get()

        try:
            # generate the password
            password = generate_password(length, use_upper, use_lower,
                                         use_digits, use_symbols)

            # show it in the text field
            self.password_field.config(state="normal")
            self.password_field.delete(0, tk.END)
            self.password_field.insert(0, password)
            self.password_field.config(state="readonly")

            # check strength
            num_types = sum([use_upper, use_lower, use_digits, use_symbols])
            strength_text, strength_color = check_strength(password, num_types)

            self.strength_label.config(text=f"Strength: {strength_text}",
                                       fg=strength_color)

            # update bar width
            if "Weak" in strength_text:
                bar_width = 0.33
            elif "Medium" in strength_text:
                bar_width = 0.66
            else:
                bar_width = 1.0

            self.strength_fill.config(bg=strength_color)
            self.strength_fill.place(relwidth=bar_width, relheight=1.0)

        except ValueError as e:
            messagebox.showwarning("Error", str(e))

    # =============================================
    # COPY BUTTON - copy to clipboard
    # =============================================
    def copy_password(self):
        password = self.password_field.get()

        if not password:
            messagebox.showinfo("Nothing to Copy", "Generate a password first!")
            return

        # copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(password)

        # show "Copied!" feedback
        self.copy_btn.config(text=" ✅ Copied! ", bg=GREEN)
        self.root.after(1500, lambda: self.copy_btn.config(text=" 📋 Copy ", bg=COPY_BTN))

    # --- Run the app ---
    def run(self):
        self.root.mainloop()


# =============================================
# Run the program
# =============================================
if __name__ == "__main__":
    app = PasswordGenerator()
    app.run()
