# Python Random Password Generator

This is a **Random Password Generator** built using Python and Tkinter as part of my **Oasis Infobyte Internship** (Task 3).  
It generates secure random passwords with a modern dark-themed GUI.

## What It Can Do

- **Custom Length** – Choose password length from 4 to 32 characters using a slider
- **Character Options** – Select which types of characters to include:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Special symbols (!@#$%...)
- **Strength Indicator** – Shows if your password is Weak, Medium, or Strong
- **Copy to Clipboard** – One-click copy with visual feedback
- **Input Validation** – Warns you if no character type is selected
- **Dark Theme GUI** – Clean, modern look built with Tkinter

## Technologies Used

- Python 3.8+
- `tkinter` – for the GUI window
- `random` – for generating random characters
- `string` – for character sets (letters, digits, symbols)

## How to Run

**Step 1:** Clone this repo or download the files

```bash
git clone https://github.com/suraj4280-alt/OIBSIP-.git
cd OIBSIP-/Python_Password_Generator
```

**Step 2:** Run the program (no extra libraries needed!)

```bash
python password_generator.py
```

> **Note:** This project uses only built-in Python libraries, so no `pip install` is needed.

## How It Works

1. Adjust the **slider** to set your desired password length
2. Check/uncheck the **character type** boxes
3. Click **Generate Password**
4. View the password and its **strength rating**
5. Click **Copy** to copy it to your clipboard

## Password Strength Rules

| Strength | Criteria |
|----------|----------|
| **Weak** ⚠️ | Length < 8 OR only 1 character type |
| **Medium** ⚡ | Length 8-15 AND 2-3 character types |
| **Strong** 💪 | Length ≥ 16 OR (length ≥ 12 AND all 4 types) |

## Screenshot

The app has a dark-themed interface with:
- Password length slider (4-32)
- Character type checkboxes
- Generate button with hover effects
- Password display with copy button
- Color-coded strength bar (red/orange/green)

## Project Structure

```
Python_Password_Generator/
├── password_generator.py    # Main application file
└── README.md                # This file
```

## Author

Made by **Suraj** as part of **Oasis Infobyte Python Internship**

## License

This project is open source under the MIT License.
