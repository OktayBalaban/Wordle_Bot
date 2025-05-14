import pyautogui
import time
from PIL import Image

def capture_wordle_board(region: tuple = None) -> Image.Image:
    screenshot = pyautogui.screenshot(region=region)
    print("📸 Screenshot captured.")
    return screenshot