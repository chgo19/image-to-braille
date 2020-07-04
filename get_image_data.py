# This is the module for getting image data in braille
# That is the objects and text present in the image

import os
CURRENT_DIR = os.getcwd()
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")
MEDIA_DIR = os.path.join(CURRENT_DIR, "media")

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

PATH_TO_CONFIG = os.path.join(ASSETS_DIR, "yolov3.cfg")
PATH_TO_WEIGHTS = os.path.join(ASSETS_DIR, "yolov3.weights")
PATH_TO_CLASSES = os.path.join(ASSETS_DIR, "yolov3.txt")

def filter_text(text: str):
    text = text.strip().upper()
    # returns filtered text
    return re.sub(FILTER, '', text)


def text_to_braille(text: str):
    text = filter_text(text)
    # returns filtered and translated text
    return text, text.translate(TRANSTAB)


# object detection hereafter untill specified.
def get_output_layers(net):

    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes, colors):

    label = str(classes[class_id])

    color = colors[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def get_objects_from_image(image_path, config=PATH_TO_CONFIG, weights=PATH_TO_WEIGHTS, classes_path=PATH_TO_CLASSES):

    image = cv2.imread(image_path)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet(weights, config)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4


    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    class_num = defaultdict(int)
    print("\n----------- Objects -----------")
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        class_num[classes[class_ids[i]]] += 1
        print(f"Class ID: {class_ids[i]}\tClass: {classes[class_ids[i]]}\tConfidence: {confidences[i]}")
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h), classes, colors)


    # displaying image
    # cv2.imshow("object detection", image)
    # cv2.waitKey()


    # writing image
    dimg_path = os.path.join(MEDIA_DIR, "detected-objects.jpg")
    cv2.imwrite(dimg_path, image)
    # cv2.destroyAllWindows()


    # making objects list for writing to file
    objects = []
    for i, n in class_num.items():
        objects.append(f"{n} {i}S".upper())
    print(objects)

    print()
    # return image with boxes
    return dimg_path, objects


def get_text_from_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    print("----------- Detected Text -----------")
    print(text +"\n")

    text = "\n".join([i for i in text.split("\n") if i])
    ftext, btext = text_to_braille(text)
    if not ftext:
        ftext, btext = text_to_braille("No Text Detected")

    print("----------- Filtered Text -----------")
    print(ftext +"\n")

    print("----------- Converted to Braille Text -----------")
    print(btext +"\n")

    return text, ftext, btext

def capture_image():
    img_name = "captured-image.png"
    img_path = os.path.join(MEDIA_DIR, img_name)
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame!")
            img_path = ''
            break

        cv2.imshow("Press SPACE to capture Image.", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Pressed ESCAPE, closing...")
            img_path = ''
            break

        elif k%256 == 32:
            # SPACE pressed
            cv2.imwrite(img_path, frame)
            print(f"{img_path} written!")
            break

    cam.release()

    cv2.destroyAllWindows()

    return img_path