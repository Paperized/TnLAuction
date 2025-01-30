Since I dont play it anymore I will share an auction bot I used to make good money.

# Throne & Liberty Auction House Bot  

## Overview  
This Python bot automates item purchases in *Throne and Liberty*'s auction house by scanning for the lowest price and buying if it meets the specified criteria. It's useful for flipping items (buy low, sell high) or purchasing items at a preferred price while away from the computer.  

## Features  
- **Automated Buying**: Scans auction house prices and purchases if the price is below the set threshold.  
- **Customizable**: Allows specifying the item, price, and quantity.  
- **Resolution Independent**: Works on any screen resolution.  
- **Logging & Screenshots**: Keeps a log of price detections and saves screenshots of purchases for reference.  
- **Background Operation**: Ideal for running overnight since it takes control of the mouse and keyboard.  

## Controls  
- **`8`** → Toggle the bot ON/OFF (starts/stops scanning and buying).  
- **`ì`** → Close the bot.  
- **`è`** → Take a screenshot of the price area (useful for debugging).

# Installation & Setup  

### Python Dependencies  
Install all required Python libraries with:  

```sh
pip install pyautogui keyboard opencv-python numpy mss pytesseract screeninfo
```

### Required Libraries  
- **pyautogui**: Mouse & keyboard automation  
- **keyboard**: Detect and simulate keyboard inputs.  
- **opencv-python**: Image processing for detecting text/numbers.  
- **numpy**: Needed for OpenCV operations.  
- **mss**: Fast screen capture (screenshots).
- **pytesseract**: Optical Character Recognition (OCR) for text extraction

### External Requirement: **Tesseract-OCR**  
The bot uses OCR (Optical Character Recognition) to read text from the game screen.  

#### 🔹 Windows Installation  
1. Download and install **Tesseract-OCR** from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).  
2. During installation, **note the installation path**.  
3. Add the Tesseract installation folder to your system **PATH**.  
4. Ensure the script points to the correct Tesseract path:  

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

# Run the bot
```sh
python bot.py
```

# Disclaimer  
Use this bot at your own risk. Automated tools may violate game terms of service. The creator is not responsible for any consequences resulting from its use.
