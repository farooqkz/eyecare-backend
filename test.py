import cv2 as cv
import numpy as np
import os

from computer_vision import get_pupil, extract_features_for_ml

root_dia = "/home/farooqkz/dia/"
root_control = "/home/farooqkz/con/"

def extract(root: str) -> str:
    i = 0

    out = ""
    for filename in os.listdir(root):
        if filename.endswith(("JPG", "JPEG", "jpg", "jpeg")):
            i += 1
            print(i)
            image = cv.imread(os.path.join(root, filename), cv.IMREAD_GRAYSCALE)
            height, width = image.shape
            width = int(width / 2)
            height = int(height / 2)
            image = cv.resize(image, (width, height))
            pupil = get_pupil(image, canny=60, close=6)
            if pupil is None:
                continue
            else:
                _, feats = extract_features_for_ml(image, pupil) 
                out += ",".join(str(x) for x in feats) + "\n"
    return out

with open("/home/farooqkz/dia.csv", "wt") as fp:
    fp.write(extract(root_dia))

with open("/home/farooqkz/control.csv", "wt") as fp:
    fp.write(extract(root_control))
