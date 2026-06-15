# Python BMI Calculator

This is a **BMI (Body Mass Index) Calculator** built using Python and Tkinter as part of my **Oasis Infobyte Internship** (Task 2).  
It calculates your BMI based on weight and height, and shows your health category.

## What It Can Do

- **BMI Calculation** – Enter weight (kg) and height (cm) to get your BMI
- **Health Categories** – Shows if you are Underweight, Normal, Overweight, or Obese
- **Color-Coded Results** – Each category has its own color (blue, green, orange, red)
- **BMI Scale Bar** – Visual bar showing where your BMI falls on the scale
- **Health Tips** – Gives a brief health suggestion based on your BMI
- **History Panel** – Keeps track of all your past calculations
- **Input Validation** – Shows error if you enter invalid values
- **Reset Button** – Clears all fields to start fresh
- **Dark Theme GUI** – Clean, modern look matching other projects

## Technologies Used

- Python 3.8+
- `tkinter` – for the GUI window
- `datetime` – for timestamping history entries

## How to Run

**Step 1:** Clone this repo or download the files

```bash
git clone https://github.com/suraj4280-alt/OIBSIP-.git
cd OIBSIP-/Python_BMI_Calculator
```

**Step 2:** Run the program (no extra libraries needed!)

```bash
python bmi_calculator.py
```

> **Note:** This project uses only built-in Python libraries, so no `pip install` is needed.

## BMI Categories

| BMI Range | Category | Color | Health Tip |
|-----------|----------|-------|------------|
| Below 18.5 | Underweight 🔵 | Blue | Consider a nutrient-rich diet |
| 18.5 – 24.9 | Normal 🟢 | Green | Maintain your healthy lifestyle |
| 25.0 – 29.9 | Overweight 🟠 | Orange | Regular exercise and balanced diet |
| 30.0+ | Obese 🔴 | Red | Consult a healthcare provider |

## BMI Formula

```
BMI = weight (kg) / (height in meters)²
```

**Example:**
- Weight = 70 kg, Height = 175 cm
- Height in meters = 175 / 100 = 1.75
- BMI = 70 / (1.75)² = 70 / 3.0625 = **22.9 (Normal)**

## Project Structure

```
Python_BMI_Calculator/
├── bmi_calculator.py    # Main application file
└── README.md            # This file
```

## Author

Made by **Suraj** as part of **Oasis Infobyte Python Internship**

## License

This project is open source under the MIT License.
