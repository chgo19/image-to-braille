# This is the main module implementing the GUI for getting objects and text from image

import os
CURRENT_DIR = os.getcwd()
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")

# import tkinter
import PySimpleGUI as sg
import get_image_data as gimd