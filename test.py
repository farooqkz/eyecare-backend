import cv2 as cv
import numpy as np
import os

from computer_vision import get_pupil, extract_features_for_ml

images: list[np.ndarray] = []

root = "/home/farooqkz/dia/"

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

print(out)
