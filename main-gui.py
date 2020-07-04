# This is the main module implementing the GUI for getting objects and text from image

import get_image_data as gimd
import PySimpleGUI as sg
import PIL
import io
import base64
import pyperclip

import os
CURRENT_DIR = os.getcwd()
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")

# import tkinter
THEME = "DarkGrey2"
IMG_SIZE = (500, 500)
IMG_BUTTON_SIZE = (19, 3)
RESULT_BUTTON_SIZE = (15, 2)
DISPLAY_TEXT, BRAILLE_DISPLAY_TEXT = gimd.text_to_braille("Please Select an Image and Press Detect.")
FONT = 'Helvetica 10 bold'


def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize(
            (int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


sg.theme(THEME)

image_layout = [[sg.Image(background_color="grey", size=IMG_SIZE, key="-IMAGE-", pad=(10, 10))],
                [sg.Input(key="-FILE-", enable_events=True, visible=False),
                 sg.FileBrowse("Select Image", size=IMG_BUTTON_SIZE, file_types=(
                     ("Image Files", "*.png;*.jpg"),), target="-FILE-"),
                 sg.Button("Capture Image", size=IMG_BUTTON_SIZE),
                 sg.Button("Detect", size=IMG_BUTTON_SIZE, key="-DETECT-", enable_events=True)]]

result_layout = [[sg.Text('Detection results')],
                 [sg.Text('Click a button to see the corresponding result')],
                 [sg.Button("Detected\nText", size=RESULT_BUTTON_SIZE, key="-DTEXT-", enable_events=True),
                  sg.Button("Detected\nObjects", size=RESULT_BUTTON_SIZE, key="-DOBJS-", enable_events=True)],
                 [sg.HorizontalSeparator(pad=(10, 10))],
                 [sg.Text("Detection in English\n(Pre-Processed for conversion to Braille)"),
                  sg.Button("Copy", size=(6, None), key="-CPFTEXT-", enable_events=True)],
                 [sg.Multiline(DISPLAY_TEXT, key='-FTEXT-', size=(None, 10))],
                 [sg.Text("Converted to Grade 1 Braille"),
                  sg.Button("Copy", size=(6, None), key="-CPBTEXT-", enable_events=True)],
                 [sg.Multiline(BRAILLE_DISPLAY_TEXT, key='-BTEXT-', size=(None, 10))],
                 [sg.Button('Exit', size=(8, 2))],
                 [sg.Text("Capstone Project | Made by CPG-16")]]

layout = [
    [
        sg.Column(image_layout, element_justification='center', size=(540, 580)),
        sg.VSeperator(),
        sg.Column(result_layout, size=(350, 610))
    ]
]

window = sg.Window('Image to Braille', layout, grab_anywhere=True, font=FONT)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == "-FILE-":
        try:
            img_path = values["-FILE-"]
            img_data = convert_to_bytes(img_path, IMG_SIZE)
            window['-IMAGE-'].update(data=img_data)
            ftext, btext = DISPLAY_TEXT, BRAILLE_DISPLAY_TEXT
            fobj_text, bobj_text = DISPLAY_TEXT, BRAILLE_DISPLAY_TEXT
            window['-FTEXT-'].update(ftext)
            window['-BTEXT-'].update(btext)
        except:
            pass

    if event == "-DETECT-":
        try:
            text, ftext, btext = gimd.get_text_from_image(img_path)
            img_path, objs = gimd.get_objects_from_image(img_path)
            fobj_text, bobj_text = gimd.text_to_braille('\n'.join(objs) or "No Objects Detected.")
            img_data = convert_to_bytes(img_path, IMG_SIZE)
            window['-IMAGE-'].update(data=img_data)
            window['-FTEXT-'].update(ftext)
            window['-BTEXT-'].update(btext)
            sg.popup_ok("Detection Complete!")
        except:
            sg.popup_ok("Please Select an Image first!", title="Error!")

    if event == "-DOBJS-":
        try:
            window['-FTEXT-'].update(fobj_text)
            window['-BTEXT-'].update(bobj_text)
        except:
            pass

    if event == "-DTEXT-":
        try:
            window['-FTEXT-'].update(ftext)
            window['-BTEXT-'].update(btext)
        except:
            pass

    if event == "-CPFTEXT-":
        pyperclip.copy(values["-FTEXT-"])

    if event == "-CPBTEXT-":
        pyperclip.copy(values["-BTEXT-"])



window.close()
