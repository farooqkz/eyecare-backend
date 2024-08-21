import cv2
import sys
from typing import Optional
import numpy as np
import os
from os.path import join

root = "/home/farooqkz/Downloads/Telegram Desktop/"

def extract_roi(file: str) -> Optional[tuple[np.ndarray]]:
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Could not read", file)
        return None
    width = len(img[0])
    height = len(img)
    min_radius = int(height * 0.4 * 0.8)
    max_radius = int(height * 0.4 * 1.2)
    print(f"Using {min_radius}, {max_radius} for {file}")
    irides = cv2.HoughCircles(
        img,
        cv2.HOUGH_GRADIENT,
        1,
        200,
        param1=40,
        param2=30,
        minRadius=min_radius,
        maxRadius=max_radius
    )
    if irides is None:
        print("No irides detected for ", file)
        return None
    irides = np.uint16(np.around(irides[0]))
    irides = filter(
        lambda i:
            abs(i[0] - width / 2) <= width / 8 and
            abs(i[1] - height / 2) <= height / 12,
        irides
    )
    def find_min(iris):
        iris_x, iris_y, iris_r = iris
        pixels = []
        for y, row in enumerate(img_t):
            pixels.extend(
                map(lambda t: t[1], filter(lambda t: (y-iris_y)**2 + (iris_x-t[0])**2 <= iris_r**2, enumerate(row)))
            )
        return sum(pixels)
    irides = list(irides)
    for iris_x, iris_y, iris_r in irides:
        cv2.circle(img_t, (iris_x, iris_y), iris_r, (255, 255, 255), 8)
    #iris_x, iris_y, iris_r = np.uint16(np.around(iris))
    edges = cv2.Canny(img, 20, 80)
    cv2.imshow("", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return
    start_y = iris_y - iris_r if iris_r < iris_y else 0
    start_x = iris_x - iris_r if iris_r < iris_x else 0
    img = img[
        start_x : iris_y + iris_r,
        start_y : iris_y + iris_r
    ]
 
    width = len(img)
    half_width = int(width / 2)

    img = img[half_width:width, 0:half_width]
    one_third_width = int(len(img) / 2.75)
    center = int(len(img) / 2)
    roi = img
    return roi


i = 0
for file in os.listdir(root):
    if not file.endswith(("JPG", )):
        continue
    extract_roi(join(root, file))
    i += 1
