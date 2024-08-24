import cv2 as cv
import numpy as np
import os

from computer_vision import get_iris, extract_features_for_ml

images: list[np.ndarray] = []

root = "/home/farooqkz/Diabetes/"

i = 0

for dirname in os.listdir(root):
    for filename in os.listdir(os.path.join(root, dirname)):
        if filename.endswith(("JPG", "JPEG", "jpg", "jpeg")):
            image = cv.imread(os.path.join(root, dirname, filename), cv.IMREAD_GRAYSCALE)
            width, height = image.shape
            width = int(width / 2)
            height = int(height / 2)
            image = cv.resize(image, (width, height))
            iris = get_iris(image, canny=75, close=6)
            if iris is None:
                continue
            cv.imwrite(f"/tmp/vo_{i}.jpg", iris[0])
            i += 1
