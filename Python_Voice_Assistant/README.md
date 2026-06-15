# Python Voice Assistant (Atlas)

This is a **Voice Assistant** built using Python as part of my **Oasis Infobyte Internship** (Task 1).  
It can listen to your voice, understand commands, and speak back the answers.

## What It Can Do

- **Voice Recognition** – Listens to your voice and converts it to text using Google Speech API
- **Text-to-Speech** – Speaks responses out loud using pyttsx3
- **Tell Time & Date** – Says the current time and date
- **Weather Updates** – Gets live weather info for any city (using OpenWeatherMap API)
- **Wikipedia Search** – Searches and reads out Wikipedia summaries
- **Open Websites** – Opens YouTube, Google, etc. in your browser
- **Text Input** – You can also type commands if mic isn't available
- **GUI Interface** – Has a nice dark-themed desktop window built with Tkinter

## Technologies Used

- Python 3.8+
- `speech_recognition` – for voice input
- `pyttsx3` – for voice output (text-to-speech)
- `wikipedia` – for searching Wikipedia
- `requests` – for weather API calls
- `tkinter` – for the GUI window
- `python-dotenv` – for loading API keys from `.env` file

## How to Run

**Step 1:** Clone this repo or download the files

```bash
git clone https://github.com/YOUR_USERNAME/OIBSIP.git
cd OIBSIP/Python_Voice_Assistant
```

**Step 2:** Install the required libraries

```bash
pip install -r requirements.txt
```

**Step 3:** Set up the Weather API key (optional)

```bash
copy .env.example .env
```

Then open `.env` file and add your OpenWeatherMap API key:

```
WEATHER_API_KEY=your_api_key_here
```

You can get a free API key from [openweathermap.org](https://openweathermap.org/api)

**Step 4:** Run the program

```bash
python -m src.main
```

## Voice Commands You Can Try

| Say This | What Happens |
|----------|-------------|
| "Hello" or "Hey" | Atlas greets you back |
| "What time is it?" | Tells the current time |
| "What is today's date?" | Tells today's date |
| "Weather in Delhi" | Shows weather for Delhi |
| "Tell me about Python" | Reads a Wikipedia summary |
| "Open YouTube" | Opens YouTube in browser |
| "Goodbye" or "Exit" | Closes the assistant |

## Project Structure

```
Python_Voice_Assistant/
├── src/
│   ├── main.py              # Main file - starts the app
│   ├── config.py             # All settings and configurations
│   ├── listener.py           # Handles microphone input
│   ├── speaker.py            # Handles voice output
│   ├── intent.py             # Understands what user is asking
│   ├── command_handler.py    # Runs the right command
│   ├── services/
│   │   ├── time_service.py   # Time and date functions
│   │   ├── weather_service.py# Weather API functions
│   │   └── wiki_service.py   # Wikipedia search functions
│   └── gui/
│       └── window.py         # GUI window (Tkinter)
├── tests/                    # Test files
├── requirements.txt          # Required Python libraries
├── .env.example              # Template for API keys
└── README.md                 # This file
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: pyaudio` | Run: `pip install pipwin && pipwin install pyaudio` |
| Microphone not working | Check your audio settings in Windows |
| Weather not working | Make sure you added your API key in `.env` file |
| GUI not opening | Check if tkinter is installed: `python -c "import tkinter"` |

## Author

Made by **[Your Name]** as part of **Oasis Infobyte Python Internship**

## License

This project is open source under the MIT License.
