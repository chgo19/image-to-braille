# Image to Braille

Download yolov3 weights from https://pjreddie.com/media/files/yolov3.weights and place it in assets folder.

### python requirements:
```sh
pip install opencv-python numpy Pillow pyperclip PySimpleGUI pytesseract
```

You also need to download and install tesseract-ocr and change a line of code present in get_image_data.py to point to its installation.
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

Capstone Project Made by CPG-16.
