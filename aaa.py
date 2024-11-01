import cv2
import pytesseract
import numpy as np
from mss import mss
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up screen capture region (e.g., x, y, width, height)
capture_region = {'top': 487, 'left': 2210, 'width': 140, 'height': 70}

# Configure Tesseract to recognize digits only
custom_config = r'--oem 3 --psm 6 outputbase digits'

# Start screen capture
with mss() as sct:
    while True:
        # Capture the specified region
        screenshot = sct.grab(capture_region)
        
        # Convert to a format that OpenCV can work with
        img = np.array(screenshot)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply OCR to the grayscale image
        number_text = pytesseract.image_to_string(gray, config=custom_config)
        
        print("Detected text:", number_text.strip())  # Strip extra whitespace/newlines

        # Display the captured portion (optional, for debugging)
        cv2.imshow('Screen Capture', gray)
        
        # Exit on pressing 'q'
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        time.sleep(0.1)  # Adjust for real-time needs

cv2.destroyAllWindows()