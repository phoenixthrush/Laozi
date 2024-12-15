import pyautogui
import tempfile
import os


def get_screenshot():
    temp_dir = tempfile.gettempdir()
    screenshot_path = os.path.join(temp_dir, "screenshot.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    return screenshot_path
