# This is the module for getting image data in braille
# That is the objects and text present in the image

import re
import cv2

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import numpy as np
from PIL import Image
from collections import defaultdict

ASCII_WIKI = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
BRAILLE_WIKI = "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿"
TRANSTAB = str.maketrans(ASCII_WIKI, BRAILLE_WIKI)
FILTER = r"[^ A-Za-z0-9.\n]+"

def filter_text(text: str):
    text = text.strip().upper()
    return re.sub(FILTER, '', text)


def text_to_braille(text: str):
    text = filter_text(text)
    return text.translate(TRANSTAB)
