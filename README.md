# Wordle Bot

This project is an **AI-powered Wordle solver** that interacts with a Wordle game in a web browser. It uses **vision-based state extraction** and a **language model-driven guessing strategy** to automatically play and solve the puzzle in real time.

## Features

- **Multimodal agent**: Combines screen reading (via computer vision) and intelligent guessing (via Gemini LLM).
- **Keyboard automation**: Types guesses directly into the browser using `pyautogui`.
- **Word state analysis**: Parses the game board and updates internal state with color-coded feedback.
- **Auto-play mode**: Runs the game autonomously until solved or attempts are exhausted.
- **Modular design**: Easy to extend or plug in a different language model.

## Requirements

- Python 3.8+
- `pyautogui`
- `Pillow`
- `gradio`
- A valid **Gemini API key**

## LLM Setup (Gemini)

This project uses LLMs from Google by default.

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).
2. Create a `.env` file in the root directory with:

GEMINI_API_KEY=your_gemini_api_key_here

3. The LLM logic is defined in `llm.py`, which wraps Gemini calls.

> ⚠️ If you wish to use another LLM provider, replace the `ask_gemini()` function in `llm.py` with your own implementation. You can define your own `ask_llm()` function with the same interface.

## Getting Started

1. Clone this repository.
2. Set your keyboard layout to English.
3. Open [Wordle](https://www.nytimes.com/games/wordle/index.html) in your browser.
4. Define your `.env` file with a valid Gemini API key.
5. Run the main script:

python test_run.py

6. Click on the browser while wordle is open so the bot can interact with the browser
