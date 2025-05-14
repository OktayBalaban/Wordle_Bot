import pyautogui
import time

def type_guess(guess: str):
    """
    Types the given Wordle guess using key presses (layout-agnostic),
    and presses Enter to submit it.
    """
    print(f"⌨️ Typing: {guess}")
    for ch in guess.upper():
        pyautogui.press(ch.lower())
        time.sleep(0.1)
    pyautogui.press("enter")
    print("✅ Guess typed and submitted.")