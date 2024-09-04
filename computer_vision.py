"""
    Copyright (C) 2024 Eyecare Team

    All rights is reserved
"""

import math
from typing import Optional

import cv2 as cv
import numpy as np
import pyfeats
import sys

from ml import IrisFeatures

Circle = tuple[float, float, float]


def is_inside_image(circle: Circle, image_shape: tuple[int, int]) -> bool:
    if circle[0] - circle[2] < 0:
        return False
    if circle[1] - circle[2] < 0:
        return False
    if circle[0] + circle[2] > image_shape[0]:
        return False
    if circle[1] + circle[2] > image_shape[1]:
        return False
    return True

def get_pupil(image: np.ndarray, canny: int = 80, close: int = 20) -> Optional[Circle]:
    iris_y, iris_x, iris_r = (int(image.shape[0] / 2), int(image.shape[1] / 2), int(min(image.shape) / 2))
    min_radius_pupil = int(iris_r * 0.8)
    max_radius_pupil = int(iris_r * 0.2)

    pupils = cv.HoughCircles(
        image,
        cv.HOUGH_GRADIENT,
        1,
        2,
        param1 = canny,
        param2 = 5,
        minRadius = min_radius_pupil,
        maxRadius = max_radius_pupil
    )
    if pupils is None:
        print("No pupil detected", file=sys.stderr)
        return None

    pupils = np.around(pupils[0])

    pupils = filter(
        lambda pupil: abs(pupil[0] - image.shape[0]/2) <= image.shape[0] / 5,
        pupils
    )
    pupils = filter(
        lambda pupil: abs(pupil[1] - image.shape[1]/2) <= image.shape[1] / 5,
        pupils
    )
    pupils = filter(
        lambda pupil: is_inside_image(pupil, (image.shape[0], image.shape[1])),
        pupils
    )


    selected_pupil: Optional[Circle] = None
    selected_dist: float = 10000
    for pupil_x, pupil_y, pupil_r in pupils:
        dist = math.sqrt((pupil_x - iris_x)**2 + (pupil_y - iris_y)**2)
        if dist <= selected_dist:
            selected_pupil = (pupil_x, pupil_y, pupil_r)
            selected_dist = dist

    if selected_pupil is None:
        print("No pupil inside detected", file=sys.stderr)
        return None
    
    return selected_pupil



_7_oclock = (math.pi / 3) + math.pi
_8_oclock = (2 * math.pi / 3) + math.pi

def extract_features_for_ml(image: np.ndarray, pupil: Circle) -> tuple[np.ndarray, IrisFeatures]:
    pupil_x, pupil_y, pupil_r = pupil
    center_x = pupil_x
    center_y = pupil_y
    mask = np.zeros(image.shape, dtype=np.uint8)
    for y, row in enumerate(image):
        for x, _ in enumerate(row):
            distance = math.dist((center_x, center_y), (x, y))
            if distance < pupil_r:
                continue
            if distance > image.shape[0] / 2:
                continue
            if x == center_x:
                continue
            if y == center_y:
                continue
            angle = np.arctan2(y - center_y, x - center_x) * 180 / np.pi
            angle += 360
            angle %= 360
            if 210 <= angle <= 240:
                mask[y, x] = 255
    result = cv.bitwise_and(mask, image)
    return result, list(pyfeats.glcm_features(result)[0])
