import cv2 as cv
import numpy as np
from typing import Optional

Circle = tuple[float, float, float]

def get_iris(image: numpy.ndarray) -> Optional[tuple[numpy.ndarray, tuple[Circle, Circle]]]:
    min_radius = 480 * 0.8 * 0.9
    max_radius = 480 * 0.8 * 1.1
    irides = cv.HoughCircles(
        image,
        cv.HOUGH_GRADIENT,
        1,
        100,
        param1 = 40,
        param2 = 20,
        minRadius = min_radius,
        maxRadius = max_radius
    )

    if irides is None:
        return None

    min_radius_p = min_radius * 0.6 * 0.9
    max_radius_p = min_radius * 0.6 * 1.1

    pupils = cv.HoughCircles(
        image,
        cv.HOUGH_GRADIENT,
        1,
        100,
        param1 = 40,
        param2 = 20,
        minRadius = min_radius_p,
        maxRadius = max_radius_p
    )
 
    selected_iris = None
    selected_pupil = None
    for iris_x, iris_y, iris_r in irides[0]:
        for pupil_x, pupil_y, pupil_r in pupils[0]:
            if math.sqrt((pupil_x - iris_x)**2 + (pupil_y - iris_y)**2) <= 10:
                selected_pupil = (pupil_x, pupil_y, pupil_r)
                selected_iris = (iris_x, iris_y, iris_r)
                break
