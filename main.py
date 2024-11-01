import mouse
import keyboard
import time
import cv2
import pytesseract
import numpy as np
import random
from mss import mss, tools
import logging
import os
import threading
import datetime
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def save_screenshot(screenshot, filename):
    # Ensure the folder exists
    os.makedirs("screenshots", exist_ok=True)

    # Save the screenshot
    tools.to_png(screenshot.rgb, screenshot.size, output=f"./screenshots/{filename}.png")

def scale_rectangle(base_resolution, target_resolution, rect):
    """
    Scales a rectangle from a base resolution to a target resolution.

    Parameters:
    - base_resolution: tuple, (base_width, base_height)
    - target_resolution: tuple, (target_width, target_height)
    - rect: tuple, (top, left, width, height) in the base resolution

    Returns:
    - Scaled rectangle as (new_top, new_left, new_width, new_height)
    """
    base_width, base_height = base_resolution
    target_width, target_height = target_resolution

    # Calculate scaling factors
    scale_x = target_width / base_width
    scale_y = target_height / base_height

    # Scale the rectangle coordinates and dimensions
    top, left, width, height = rect
    new_top = int(top * scale_y)
    new_left = int(left * scale_x)
    new_width = int(width * scale_x)
    new_height = int(height * scale_y)

    return new_top, new_left, new_width, new_height

base_resolution = (2560, 1440)  # 2K
target_resolution = (1920, 1080)  # Full HD

rectangle = (487, 2210, 140, 70)
#rectangle = scale_rectangle(base_resolution, target_resolution, rectangle)

top, left, width, height = rectangle

# Set up screen capture region (e.g., x, y, width, height)
capture_region = {'top': top, 'left': left, 'width': width, 'height': height}

# Configure Tesseract to recognize digits only
custom_config = r'--oem 3 --psm 6 outputbase digits'

exit = False
scanAH = False

current_buy_price = 99999999999999
scan_delay = 1
buy = False

trait_name = input("Enter trait name: ")
price_to_buy = int(input("Enter max price: "))
scan_delay = float(input("Enter scan delay (seconds): "))

# Set up logging to both file and console to capture all messages
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG to capture all levels
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format with timestamp and level
    handlers=[
        logging.FileHandler(f"logs/{trait_name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

logging.info(f'[STARTUP] Setup with "{trait_name}" with maximum price to buy: {price_to_buy}')

def switchScanAH(value):
    global scanAH

    if scanAH == value:
        return

    scanAH = value
    if scanAH:
        logging.info("[SCAN] Started Scanning for items")
    else:

        logging.info("[SCAN] Stopped scanning for items")

def switchBuyAH(value):
    global buy

    if buy == value:
        return

    buy = value
    if buy:
        logging.info("[BUY] Started buy routine")
    else:
        logging.info("[BUY] Finished buy routine")

def on_key_event(event):
    global exit
    global scanAH
    global buy

    if event.name == "è":
        with mss() as sct:
            screenshot = sct.grab(capture_region)
            threading.Thread(target=save_screenshot, args=(screenshot, f"TEST_RECTANGLE")).start()
    if event.name == 'ì':
        exit = True
    if event.name == '8':
        switchScanAH(not scanAH)
        switchBuyAH(False)

keyboard.on_press(on_key_event)

def waitUntilToggleOrExit():
    global scanAH
    global exit
    global buy

    while ((not scanAH) and (not buy)):
        time.sleep(1)
        if exit:
            return False
    
    return not exit

def buyItem():
    global buy
    global current_buy_price
    global scanAH

    mouse.click()
    
    remaining_time_buffer = 3
    while remaining_time_buffer > 0:
        keyboard.press_and_release('y')
        remaining_time_buffer -= 0.3
        time.sleep(0.3)

    logging.info('[BUY] Bought at ' + str(current_buy_price))
    switchBuyAH(False)
    #sys.exit()

movement = ['w', 's', 'a', 'd']

def doActivity():
    first_direction = random.choice(movement)
    
    # Create a new list without the first direction
    remaining_directions = [direction for direction in movement if direction != first_direction]
    
    # Select the second direction from the remaining directions
    second_direction = random.choice(remaining_directions)

    keyboard.press_and_release('esc')
    keyboard.press(first_direction)
    keyboard.press(second_direction)

    time.sleep(1)

    keyboard.release(first_direction)
    keyboard.release(second_direction)

    time.sleep(2)

    if random.randint(1, 10) == 1:
        time.sleep(20)

def openAH():
    keyboard.press_and_release('l')
    time.sleep(4)
    return

lowest_price = 99999999999999

def refreshAH():
    global buy
    global current_buy_price
    global lowest_price

    with mss() as sct:
        screenshot = sct.grab(capture_region)

        # Convert to a format that OpenCV can work with
        img = np.array(screenshot)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply OCR to the grayscale image
        number_text = pytesseract.image_to_string(gray, config=custom_config)
        number_text = number_text.strip()
        logging.info(f"[PRICE] Price found: {number_text}")

        if number_text == '':
            price = 99999999999999
        else:
            price = int(number_text)

        if price < lowest_price:
            logging.info(f"[LOWEST] Lowest price was {number_text}")
            lowest_price = price

        if price <= price_to_buy:
            switchBuyAH(True)
            current_buy_price = price
            logging.info(f"[BUY] Item to be bought for {str(current_buy_price)}")
            threading.Thread(target=save_screenshot, args=(screenshot, f"{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_PRICE_{price}.png")).start()
            return

    keyboard.press_and_release('q')

time_elapsed = 0
next_activity_time = random.randint(5*60, 9*60)

while not exit:
    if not waitUntilToggleOrExit():
        break

    try:
        if time_elapsed >= next_activity_time:
            time_elapsed = 0
            next_activity_time = random.randint(4*60, 8*60)
            doActivity()
            openAH()

        refreshAH()

        if buy:
            buyItem()

        time.sleep(scan_delay)
        time_elapsed += scan_delay
    except Exception as e:
        time_elapsed = time_elapsed

keyboard.unhook_all()