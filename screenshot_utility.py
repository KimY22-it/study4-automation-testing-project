import os
from datetime import datetime


def take_screenshot(driver, name="screenshot"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(base_dir, "screenshots")
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(folder, f"{name}_{timestamp}.png")
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")
