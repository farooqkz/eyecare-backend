import math
from typing import Optional

import cv2 as cv
import numpy as np
import pyfeats

from ml import IrisFeatures

Circle = tuple[float, float, float]
Iris = tuple[np.ndarray, Circle, Circle]


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

def get_iris(image: np.ndarray, param1: int = 200, param2: int = 20) -> Optional[Iris]:
    width, height = image.shape
    param = min(width, height)

    min_radius_iris = int(param * 0.3 * 0.5)
    max_radius_iris = int(param * 0.3 * 3.0)
    irides = cv.HoughCircles(
        image,
        cv.HOUGH_GRADIENT,
        1,
        100,
        param1 = param1,
        param2 = 1,
        minRadius = min_radius_iris,
        maxRadius = max_radius_iris
    )
    if irides is None:
        return None
    irides = np.around(irides[0])

    min_radius_pupil = int(min_radius_iris * 0.2 * 0.5)
    max_radius_pupil = int(min_radius_iris * 0.2 * 4.5)

    pupils = cv.HoughCircles(
        image,
        cv.HOUGH_GRADIENT,
        2,
        100,
        param1 = param1,
        param2 = 10,
        minRadius = min_radius_pupil,
        maxRadius = max_radius_pupil
    )
    if pupils is None:
        return None

    pupils = np.around(pupils[0])

    irides = list(filter(
        lambda iris: is_inside_image(iris, (image.shape[0], image.shape[1])),
        irides
    ))
    pupils = list(filter(
        lambda pupil: is_inside_image(pupil, (image.shape[0], image.shape[1])),
        pupils
    ))

    print(pupils, "\n\n", irides)

    selected_iris: Optional[Circle] = None
    selected_pupil: Optional[Circle] = None
    for iris_x, iris_y, iris_r in irides:
        for pupil_x, pupil_y, pupil_r in pupils:
            dist = math.sqrt((pupil_x - iris_x)**2 + (pupil_y - iris_y)**2)
            if dist <= param2:
                selected_pupil = (pupil_x, pupil_y, pupil_r)
                selected_iris = (iris_x, iris_y, iris_r)
                break

    if selected_iris is None or selected_pupil is None:
        return None
    
    center_x = selected_iris[0]
    center_y = selected_iris[1]
    length = selected_iris[2]
    x_upper = int(min(image.shape[0], center_x + length))
    y_upper = int(min(image.shape[1], center_y + length))
    x_lower = int(max(0, center_x - length))
    y_lower = int(max(0, center_y - length))
    image = image[
        y_lower : y_upper,
        x_lower : x_upper
    ]

    return image, selected_iris, selected_pupil


def extract_features_for_ml(iris_data: Iris) -> tuple[np.ndarray, IrisFeatures]:
    image, iris, pupil = iris_data
    iris_x, iris_y, iris_r = iris
    _pupil_x, _pupil_y, pupil_r = pupil
    diff_r = int(abs(iris_r - pupil_r))
    iris_perimeter = 2 * np.pi * iris_r
    pupil_perimeter = 2 * np.pi * pupil_r
    average_perimeter = int((iris_perimeter + pupil_perimeter) / 2)
    unwrapped_image = np.zeros([int(average_perimeter / 12), diff_r])
    center_x = iris_x
    center_y = iris_y
    for y, row in enumerate(image):
        for x, value in enumerate(row):
            distance = math.dist((center_x, center_y), (x, y))
            if distance < pupil_r:
                continue
            if x >= center_x:
                continue
            if y <= center_y:
                continue
            angle = math.atan(abs(y - center_y) / abs(x - center_x))
            clock = angle * math.pi / 12
            if clock <= 7:
                continue
            if clock >= 8:
                continue
            x = int(distance * math.cos(angle))
            y = int(distance * math.sin(angle))
            unwrapped_image[x, y] = value
    return unwrapped_image, list(pyfeats.glcm_features(unwrapped_image)[0])
